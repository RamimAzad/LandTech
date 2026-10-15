"""
Rule-Based Anomaly Detection Engine for JomiGuard.
Implements explainable land transaction inconsistency checks:
1. Conflicting Double-Selling & Area Over-sale
2. Area Discrepancies (Registration Deed vs. Mutation Record)
3. Buyer vs. Applicant Identity Mismatches
4. Chronological / Temporal Paradoxes
5. Phantom Deed References
6. Broken Chain-of-Title / Non-Owner Sales
"""

from datetime import datetime
from typing import Dict, List, Tuple, Any
import pandas as pd

from core.models import AnomalyAlert, SeverityLevel, TriageStatus
from core.db import get_all_plots, get_all_deeds, get_all_mutations, save_alerts, DEFAULT_DB_PATH


# Thresholds
AREA_TOLERANCE_DECIMALS = 0.02
AREA_TOLERANCE_PCT = 0.5  # 0.5%


def detect_double_selling(
    plots_df: pd.DataFrame,
    deeds_df: pd.DataFrame
) -> List[AnomalyAlert]:
    """
    Detects:
    1. Direct Double-Selling: Same seller selling to multiple distinct buyers without reacquiring.
    2. Fractional Over-Selling: A seller transferring more land than they legitimately own/hold on record.
    """
    alerts: List[AnomalyAlert] = []
    plots_map = plots_df.set_index("plot_id").to_dict(orient="index")
    
    for plot_id, group in deeds_df.groupby("plot_id"):
        plot = plots_map.get(plot_id)
        if not plot:
            continue
            
        plot_total_area = float(plot["total_area_decimals"])
        initial_owner_nid = str(plot["initial_owner_nid"]).strip()
        sorted_deeds = group.sort_values("registration_date").to_dict(orient="records")
        
        # Track holding balance per owner over time
        # Initially, the initial recorded owner holds plot_total_area
        owner_balances: Dict[str, float] = {initial_owner_nid: plot_total_area}
        seller_sales_history: Dict[str, List[Dict[str, Any]]] = {}
        
        for deed in sorted_deeds:
            s_nid = str(deed["seller_nid"]).strip()
            b_nid = str(deed["buyer_nid"]).strip()
            transferred = float(deed["transferred_area_decimals"])
            deed_no = str(deed["deed_no"])
            reg_date = str(deed["registration_date"])
            
            seller_sales_history.setdefault(s_nid, []).append(deed)
            available_balance = owner_balances.get(s_nid, 0.0)
            
            # Check 1: Direct Double-Selling
            # If seller already sold their full holding or sold this plot previously
            prior_sales = seller_sales_history[s_nid][:-1]  # Sales before this deed
            if prior_sales:
                # If seller sold to a different buyer
                prev_deed = prior_sales[-1]
                if prev_deed["buyer_nid"] != b_nid:
                    # Check if seller had reacquired land between prev_deed and current deed
                    # If available_balance is insufficient or zero, this is a conflicting double sale!
                    if available_balance < (transferred - AREA_TOLERANCE_DECIMALS):
                        alert_id = f"ALT-DOUBLE-{plot_id}-{prev_deed['deed_no']}-{deed_no}"
                        trigger_fields = {
                            "plot_id": plot_id,
                            "seller_name": deed["seller_name"],
                            "seller_nid": s_nid,
                            "deed_1_no": prev_deed["deed_no"],
                            "deed_1_date": prev_deed["registration_date"],
                            "deed_1_buyer": prev_deed["buyer_name"],
                            "deed_1_area_decimals": float(prev_deed["transferred_area_decimals"]),
                            "deed_2_no": deed_no,
                            "deed_2_date": reg_date,
                            "deed_2_buyer": deed["buyer_name"],
                            "deed_2_area_decimals": transferred,
                        }
                        evidence = {
                            "conflict_type": "Conflicting Double-Sale by Same Seller",
                            "first_deed": prev_deed,
                            "second_deed": deed,
                            "days_between_sales": (
                                datetime.strptime(reg_date, "%Y-%m-%d") -
                                datetime.strptime(prev_deed["registration_date"], "%Y-%m-%d")
                            ).days
                        }
                        explanation = (
                            f"Seller '{deed['seller_name']}' (NID: {s_nid}) previously executed deed {prev_deed['deed_no']} "
                            f"transferring {prev_deed['transferred_area_decimals']} decimals to '{prev_deed['buyer_name']}' on {prev_deed['registration_date']}, "
                            f"and subsequently executed deed {deed_no} transferring {transferred} decimals to '{deed['buyer_name']}' "
                            f"on {reg_date} without sufficient remaining title balance."
                        )
                        alerts.append(AnomalyAlert(
                            alert_id=alert_id,
                            rule_id="RULE_DOUBLE_SALE",
                            rule_name="Conflicting Double-Selling Detected",
                            plot_id=plot_id,
                            severity=SeverityLevel.CRITICAL.value,
                            title=f"Repeated Sale Conflict: {deed['seller_name']} sold Plot {plot_id} twice",
                            explanation=explanation,
                            trigger_fields=trigger_fields,
                            evidence=evidence,
                        ))
                        
            # Check 2: Fractional / Cumulative Over-Selling
            # If transferred area exceeds seller's available balance (and wasn't already caught above)
            if transferred > (available_balance + AREA_TOLERANCE_DECIMALS):
                excess = round(transferred - available_balance, 2)
                alert_id = f"ALT-OVERSALE-{plot_id}-{deed_no}"
                if not any(a.alert_id == f"ALT-DOUBLE-{plot_id}-{deed_no}" or (hasattr(a, 'trigger_fields') and a.trigger_fields.get('deed_2_no') == deed_no) for a in alerts):
                    trigger_fields = {
                        "plot_id": plot_id,
                        "deed_no": deed_no,
                        "seller_name": deed["seller_name"],
                        "seller_nid": s_nid,
                        "available_balance_decimals": round(available_balance, 2),
                        "transferred_area_decimals": transferred,
                        "excess_area_decimals": excess,
                    }
                    evidence = {
                        "deed_record": deed,
                        "seller_recorded_balance": round(available_balance, 2),
                        "attempted_transfer": transferred
                    }
                    explanation = (
                        f"Deed {deed_no} by seller '{deed['seller_name']}' attempts to transfer {transferred:.2f} decimals, "
                        f"exceeding their verified available plot balance of {available_balance:.2f} decimals by {excess:.2f} decimals."
                    )
                    alerts.append(AnomalyAlert(
                        alert_id=alert_id,
                        rule_id="RULE_DOUBLE_SALE",
                        rule_name="Cumulative Land Over-Selling",
                        plot_id=plot_id,
                        severity=SeverityLevel.CRITICAL.value,
                        title=f"Over-Sale: Deed {deed_no} transfers {transferred:.2f} dec (Exceeds Balance by {excess:.2f} dec)",
                        explanation=explanation,
                        trigger_fields=trigger_fields,
                        evidence=evidence,
                    ))

            # Update balances: seller loses transferred area, buyer gains transferred area
            owner_balances[s_nid] = max(0.0, available_balance - transferred)
            owner_balances[b_nid] = owner_balances.get(b_nid, 0.0) + transferred

    return alerts


def detect_registration_mutation_inconsistencies(
    plots_df: pd.DataFrame,
    deeds_df: pd.DataFrame,
    mutations_df: pd.DataFrame
) -> List[AnomalyAlert]:
    """
    Flags inconsistencies between sample registration and mutation records:
    - Area discrepancies (mutated area != deed area)
    - Identity mismatches (mutation applicant != deed buyer)
    - Chronological paradoxes (mutation approved before deed registration date)
    - Phantom deed references (mutation references non-existent deed)
    """
    alerts: List[AnomalyAlert] = []
    deeds_map = deeds_df.set_index("deed_no").to_dict(orient="index")
    
    for _, mut in mutations_df.iterrows():
        mut_case_no = str(mut["mutation_case_no"])
        cited_deed_no = str(mut["deed_no"])
        plot_id = str(mut["plot_id"])
        mut_area = float(mut["mutated_area_decimals"])
        mut_date_str = str(mut["mutation_date"])
        app_nid = str(mut["applicant_nid"]).strip()
        app_name = str(mut["applicant_name"]).strip()
        
        # Check: Phantom Deed Reference
        if cited_deed_no not in deeds_map:
            alert_id = f"ALT-PHANTOM-{mut_case_no}"
            trigger_fields = {
                "mutation_case_no": mut_case_no,
                "cited_deed_no": cited_deed_no,
                "mutation_date": mut_date_str,
                "applicant_name": app_name,
                "applicant_nid": app_nid,
                "mutated_area_decimals": mut_area,
            }
            evidence = {
                "mutation_record": mut.to_dict(),
                "registry_lookup_result": "Deed number not found in Sub-Registry Office repository"
            }
            explanation = (
                f"Mutation record {mut_case_no} approved {mut_area} decimals citing deed "
                f"'{cited_deed_no}', but no matching registration record exists in the deed repository. "
                f"This indicates a potential phantom mutation."
            )
            alerts.append(AnomalyAlert(
                alert_id=alert_id,
                rule_id="RULE_PHANTOM_MUTATION",
                rule_name="Phantom Deed Reference in Mutation",
                plot_id=plot_id,
                severity=SeverityLevel.CRITICAL.value,
                title=f"Phantom Deed Citation: {cited_deed_no} Not Found in Registry",
                explanation=explanation,
                trigger_fields=trigger_fields,
                evidence=evidence,
            ))
            continue
            
        deed = deeds_map[cited_deed_no]
        deed_area = float(deed["transferred_area_decimals"])
        deed_date_str = str(deed["registration_date"])
        buyer_nid = str(deed["buyer_nid"]).strip()
        buyer_name = str(deed["buyer_name"]).strip()
        
        # Check: Area Discrepancy
        diff_area = round(mut_area - deed_area, 2)
        diff_pct = round((abs(diff_area) / deed_area) * 100, 1) if deed_area > 0 else 0
        
        if abs(diff_area) > AREA_TOLERANCE_DECIMALS and diff_pct > AREA_TOLERANCE_PCT:
            direction = "INFLATION" if diff_area > 0 else "DEFICIT"
            alert_id = f"ALT-AREA-{mut_case_no}-{cited_deed_no}"
            trigger_fields = {
                "deed_no": cited_deed_no,
                "mutation_case_no": mut_case_no,
                "deed_transferred_area_decimals": deed_area,
                "mutation_approved_area_decimals": mut_area,
                "discrepancy_decimals": diff_area,
                "discrepancy_percentage": diff_pct,
                "anomaly_type": direction
            }
            evidence = {
                "deed_record": deed,
                "mutation_record": mut.to_dict(),
                "variance": f"{diff_area:+.2f} decimals ({diff_pct}%)"
            }
            explanation = (
                f"Mutation {mut_case_no} approved {mut_area:.2f} decimals, but referenced deed "
                f"{cited_deed_no} transferred {deed_area:.2f} decimals. "
                f"Discrepancy of {diff_area:+.2f} decimals ({diff_pct}% {direction.lower()}) detected "
                f"between registration and revenue records."
            )
            alerts.append(AnomalyAlert(
                alert_id=alert_id,
                rule_id="RULE_AREA_MISMATCH",
                rule_name="Area Discrepancy: Registration vs. Mutation",
                plot_id=plot_id,
                severity=SeverityLevel.HIGH.value,
                title=f"Area Mismatch: Mutated {mut_area:.2f} dec vs Deed {deed_area:.2f} dec",
                explanation=explanation,
                trigger_fields=trigger_fields,
                evidence=evidence,
            ))
            
        # Check: Identity Mismatch
        if app_nid != buyer_nid or app_name.lower() != buyer_name.lower():
            alert_id = f"ALT-ID-{mut_case_no}-{cited_deed_no}"
            trigger_fields = {
                "deed_no": cited_deed_no,
                "deed_buyer_name": buyer_name,
                "deed_buyer_nid": buyer_nid,
                "mutation_case_no": mut_case_no,
                "mutation_applicant_name": app_name,
                "mutation_applicant_nid": app_nid,
                "name_match": app_name.lower() == buyer_name.lower(),
                "nid_match": app_nid == buyer_nid
            }
            evidence = {
                "deed_party": {"name": buyer_name, "nid": buyer_nid},
                "mutation_party": {"name": app_name, "nid": app_nid}
            }
            explanation = (
                f"Deed {cited_deed_no} was registered to buyer '{buyer_name}' (NID: {buyer_nid}), "
                f"but mutation {mut_case_no} was granted to applicant '{app_name}' (NID: {app_nid}). "
                f"Applicant identity does not match the registered deed of sale."
            )
            alerts.append(AnomalyAlert(
                alert_id=alert_id,
                rule_id="RULE_IDENTITY_MISMATCH",
                rule_name="Party Identity Mismatch (Buyer vs. Applicant)",
                plot_id=plot_id,
                severity=SeverityLevel.HIGH.value,
                title=f"Identity Conflict: Deed Buyer '{buyer_name}' vs Applicant '{app_name}'",
                explanation=explanation,
                trigger_fields=trigger_fields,
                evidence=evidence,
            ))
            
        # Check: Chronological / Temporal Conflict
        try:
            m_dt = datetime.strptime(mut_date_str, "%Y-%m-%d")
            d_dt = datetime.strptime(deed_date_str, "%Y-%m-%d")
            if m_dt < d_dt:
                delta_days = (d_dt - m_dt).days
                alert_id = f"ALT-TIME-{mut_case_no}-{cited_deed_no}"
                trigger_fields = {
                    "deed_no": cited_deed_no,
                    "deed_registration_date": deed_date_str,
                    "mutation_case_no": mut_case_no,
                    "mutation_date": mut_date_str,
                    "inversion_days": delta_days
                }
                evidence = {
                    "deed_registration_date": deed_date_str,
                    "mutation_date": mut_date_str,
                    "days_preceding_deed": delta_days
                }
                explanation = (
                    f"Mutation {mut_case_no} has an approval date of {mut_date_str}, which is "
                    f"{delta_days} days PRIOR to the registered deed's execution date ({deed_date_str}). "
                    f"Chronologically impossible under standard revenue and registration laws."
                )
                alerts.append(AnomalyAlert(
                    alert_id=alert_id,
                    rule_id="RULE_TEMPORAL_CONFLICT",
                    rule_name="Chronological Paradox in Land Records",
                    plot_id=plot_id,
                    severity=SeverityLevel.HIGH.value,
                    title=f"Temporal Conflict: Mutation dated {delta_days} days before Deed",
                    explanation=explanation,
                    trigger_fields=trigger_fields,
                    evidence=evidence,
                ))
        except ValueError:
            pass

    return alerts


def detect_broken_chain_of_title(
    plots_df: pd.DataFrame,
    deeds_df: pd.DataFrame,
    mutations_df: pd.DataFrame
) -> List[AnomalyAlert]:
    """
    Detects sales where the seller has no prior verified ownership on record
    (neither initial recorded owner nor verified prior buyer in an approved transaction).
    """
    alerts: List[AnomalyAlert] = []
    plots_map = plots_df.set_index("plot_id").to_dict(orient="index")
    
    for plot_id, group in deeds_df.groupby("plot_id"):
        plot = plots_map.get(plot_id)
        if not plot:
            continue
            
        initial_owner_nid = str(plot["initial_owner_nid"]).strip()
        sorted_deeds = group.sort_values("registration_date").to_dict(orient="records")
        
        # Track verified owners over time
        verified_owners = {initial_owner_nid}
        
        for deed in sorted_deeds:
            s_nid = str(deed["seller_nid"]).strip()
            b_nid = str(deed["buyer_nid"]).strip()
            deed_no = str(deed["deed_no"])
            
            if s_nid not in verified_owners:
                alert_id = f"ALT-CHAIN-{plot_id}-{deed_no}"
                trigger_fields = {
                    "plot_id": plot_id,
                    "deed_no": deed_no,
                    "seller_name": deed["seller_name"],
                    "seller_nid": s_nid,
                    "plot_initial_owner": plot["initial_owner_name"],
                    "plot_initial_owner_nid": initial_owner_nid,
                }
                evidence = {
                    "deed_record": deed,
                    "verified_owners_at_execution": list(verified_owners)
                }
                explanation = (
                    f"Seller '{deed['seller_name']}' (NID: {s_nid}) executed deed {deed_no} for "
                    f"Plot {plot_id}, but does not appear as an initial owner or prior buyer in the "
                    f"chain of title. Possible unverified transfer or identity appropriation."
                )
                alerts.append(AnomalyAlert(
                    alert_id=alert_id,
                    rule_id="RULE_BROKEN_CHAIN",
                    rule_name="Unverified / Broken Chain of Title",
                    plot_id=plot_id,
                    severity=SeverityLevel.MEDIUM.value,
                    title=f"Broken Chain of Title: Seller {deed['seller_name']} has no prior record",
                    explanation=explanation,
                    trigger_fields=trigger_fields,
                    evidence=evidence,
                ))
                
            # Add buyer to verified list for subsequent sales
            verified_owners.add(b_nid)
            
    return alerts


def run_detection(db_path: str = DEFAULT_DB_PATH) -> Tuple[List[AnomalyAlert], Dict[str, Any]]:
    """
    Executes the full suite of anomaly detection rules across the SQLite database.
    Persists all generated alerts and returns (alerts_list, summary_metrics).
    """
    plots_df = get_all_plots(db_path)
    deeds_df = get_all_deeds(db_path)
    mutations_df = get_all_mutations(db_path)
    
    all_alerts: List[AnomalyAlert] = []
    
    # 1. Double Selling & Area Over-sale
    all_alerts.extend(detect_double_selling(plots_df, deeds_df))
    
    # 2. Registration vs Mutation Discrepancies
    all_alerts.extend(detect_registration_mutation_inconsistencies(plots_df, deeds_df, mutations_df))
    
    # 3. Chain of Title Integrity
    all_alerts.extend(detect_broken_chain_of_title(plots_df, deeds_df, mutations_df))
    
    # Persist to database
    save_alerts(all_alerts, db_path)
    
    # Summary Metrics
    severity_counts = {
        SeverityLevel.CRITICAL.value: sum(1 for a in all_alerts if a.severity == SeverityLevel.CRITICAL.value),
        SeverityLevel.HIGH.value: sum(1 for a in all_alerts if a.severity == SeverityLevel.HIGH.value),
        SeverityLevel.MEDIUM.value: sum(1 for a in all_alerts if a.severity == SeverityLevel.MEDIUM.value),
        SeverityLevel.LOW.value: sum(1 for a in all_alerts if a.severity == SeverityLevel.LOW.value),
    }
    
    rule_counts = {}
    for a in all_alerts:
        rule_counts[a.rule_name] = rule_counts.get(a.rule_name, 0) + 1
        
    summary = {
        "total_plots_analyzed": len(plots_df),
        "total_deeds_analyzed": len(deeds_df),
        "total_mutations_analyzed": len(mutations_df),
        "total_alerts_found": len(all_alerts),
        "severity_counts": severity_counts,
        "rule_counts": rule_counts,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return all_alerts, summary
