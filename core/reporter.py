"""
Report Generation Module for JomiGuard.
Generates structured downloadable reports in CSV, Markdown, and Printable HTML formats.
"""

from datetime import datetime
import json
from typing import Dict, List, Any
import pandas as pd


_FIELD_LABELS = {
    "deed_no": "Deed No",
    "plot_id": "Plot ID",
    "registration_date": "Registration Date",
    "seller_nid": "Seller NID",
    "seller_name": "Seller Name",
    "buyer_nid": "Buyer NID",
    "buyer_name": "Buyer Name",
    "transferred_area_decimals": "Transferred Area (dec)",
    "deed_value_bdt": "Deed Value (BDT)",
    "sub_registry_office": "Sub-Registry Office",
    "status": "Status",
    "created_at": "Recorded At",
    "name": "Name",
    "nid": "NID",
    "mutation_case_no": "Mutation Case No",
    "mutation_date": "Mutation Date",
    "applicant_name": "Applicant Name",
    "applicant_nid": "Applicant NID",
    "mutated_area_decimals": "Mutated Area (dec)",
    "new_khatian_no": "New Khatian No",
    "ac_land_office": "AC Land Office",
    "deed_registration_date": "Deed Registration Date",
    "days_preceding_deed": "Days Preceding Deed",
    "seller_recorded_balance": "Seller Recorded Balance (dec)",
    "attempted_transfer": "Attempted Transfer (dec)",
    "deed_buyer_name": "Deed Buyer Name",
    "deed_buyer_nid": "Deed Buyer NID",
    "mutation_applicant_name": "Mutation Applicant Name",
    "mutation_applicant_nid": "Mutation Applicant NID",
    "name_match": "Name Match",
    "nid_match": "NID Match",
    "deed_transferred_area_decimals": "Deed Transferred Area (dec)",
    "mutation_approved_area_decimals": "Mutation Approved Area (dec)",
    "available_balance_decimals": "Available Balance (dec)",
    "excess_area_decimals": "Excess Area (dec)",
    "discrepancy_decimals": "Discrepancy (dec)",
    "discrepancy_percentage": "Discrepancy (%)",
    "anomaly_type": "Anomaly Type",
    "cited_deed_no": "Cited Deed No",
    "deed_1_no": "First Deed No",
    "deed_1_date": "First Deed Date",
    "deed_1_buyer": "First Deed Buyer",
    "deed_1_area_decimals": "First Deed Area (dec)",
    "deed_2_no": "Second Deed No",
    "deed_2_date": "Second Deed Date",
    "deed_2_buyer": "Second Deed Buyer",
    "deed_2_area_decimals": "Second Deed Area (dec)",
    "plot_initial_owner": "Plot Initial Owner",
    "plot_initial_owner_nid": "Plot Initial Owner NID",
    "inversion_days": "Chronological Inversion (days)",
    "days_between_sales": "Days Between Sales",
}


def _format_trigger_value(value: Any) -> str:
    """Render a trigger field value as clean, table-safe text."""
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if isinstance(value, float) and not value.is_integer():
            return f"{value:,.2f}"
        return f"{int(value):,}"
    return str(value).replace("|", "\\|").replace("\n", " ")


def _format_trigger_table(trigger_fields: Dict[str, Any]) -> str:
    """Build a clean Markdown table for the triggered fields (no raw JSON)."""
    if not trigger_fields:
        return "_No trigger fields were recorded for this alert._\n"

    lines = ["| Triggered Field | Value |", "| :--- | :--- |"]
    for key, value in trigger_fields.items():
        label = _FIELD_LABELS.get(key, str(key).replace("_", " ").title())
        lines.append(f"| {label} | `{_format_trigger_value(value)}` |")
    return "\n".join(lines) + "\n"


def export_alerts_to_csv(alerts_df: pd.DataFrame) -> str:
    """Converts alerts dataframe to CSV string for download."""
    if alerts_df.empty:
        return "alert_id,rule_id,rule_name,plot_id,severity,title,explanation,triage_status,reviewer_notes,created_at\n"
        
    export_df = alerts_df[[
        "alert_id", "rule_id", "rule_name", "plot_id", "severity",
        "title", "explanation", "triage_status", "reviewer_notes", "created_at"
    ]].copy()
    
    return export_df.to_csv(index=False)


def generate_markdown_audit_report(
    alerts_df: pd.DataFrame,
    summary_metrics: Dict[str, Any]
) -> str:
    """
    Generates a formal, printable Markdown land record investigation report.
    """
    now_str = datetime.now().strftime("%d %B %Y, %I:%M %p")
    report_id = f"JOMIGUARD-AUDIT-{int(datetime.now().timestamp())}"
    
    sev = summary_metrics.get("severity_counts", {})
    critical_cnt = sev.get("CRITICAL", 0)
    high_cnt = sev.get("HIGH", 0)
    med_cnt = sev.get("MEDIUM", 0)
    low_cnt = sev.get("LOW", 0)
    
    total_alerts = summary_metrics.get("total_alerts_found", len(alerts_df))
    plots_cnt = summary_metrics.get("total_plots_analyzed", 0)
    deeds_cnt = summary_metrics.get("total_deeds_analyzed", 0)
    mutations_cnt = summary_metrics.get("total_mutations_analyzed", 0)
    
    md = f"""# JomiGuard — Land Record Anomaly Investigation Report
**Report ID:** `{report_id}`  
**Generated On:** {now_str}  
**System:** JomiGuard Automated Land Record Anomaly & Inconsistency Detection Engine  

---

> ### ⚠️ Regulatory & Administrative Disclaimer
> **IMPORTANT:** An alert flagged by JomiGuard indicates a *potential transactional inconsistency, procedural discrepancy, or record mismatch*, **not confirmed criminal fraud**. Repeated identifiers, delayed updates, or differing areas may have legitimate administrative explanations (such as co-owner inheritance partitions, boundary recalculations, or pending court rectifications) and strictly require human review by authorized Land Revenue and Sub-Registry Officers.

---

## 1. Executive Audit Summary

| Metric | Inspected Count |
| :--- | :--- |
| **Total Land Plots Screened** | {plots_cnt} |
| **Total Registered Deeds Audited** | {deeds_cnt} |
| **Total Land Mutations (Namjari) Screened** | {mutations_cnt} |
| **Total Flagged Inconsistencies** | **{total_alerts}** |
| — Critical Severity (e.g., Double Selling, Phantom Deeds) | **{critical_cnt}** |
| — High Severity (e.g., Area Discrepancy, Identity Mismatch) | **{high_cnt}** |
| — Medium Severity (e.g., Unverified Chain of Title) | **{med_cnt}** |
| — Low Severity | **{low_cnt}** |

---

## 2. Inconsistencies by Category

"""
    rule_counts = summary_metrics.get("rule_counts", {})
    if rule_counts:
        md += "| Rule Category | Flagged Cases |\n| :--- | :--- |\n"
        for rule_name, cnt in rule_counts.items():
            md += f"| {rule_name} | **{cnt}** |\n"
        md += "\n---\n"

    md += """## 3. Detailed Case Dossiers & Explainable Indicators

"""

    if alerts_df.empty:
        md += "_No inconsistencies or anomalies detected in the current record ledger._\n"
    else:
        for idx, row in alerts_df.iterrows():
            aid = row["alert_id"]
            pid = row["plot_id"]
            sev_val = row["severity"]
            title = row["title"]
            rule_name = row["rule_name"]
            explanation = row["explanation"]
            status = row.get("triage_status", "Pending Review")
            notes = row.get("reviewer_notes", "None")
            
            trigger_fields = {}
            if "trigger_fields_json" in row and row["trigger_fields_json"]:
                try:
                    trigger_fields = json.loads(row["trigger_fields_json"])
                except Exception:
                    pass

            md += f"""### Case {idx+1}: [{sev_val}] {title}
- **Alert ID:** `{aid}`
- **Plot Identifier:** `{pid}`
- **Category:** {rule_name}
- **Current Triage Status:** `{status}`
- **Auditor Notes:** _{notes if notes else 'No notes entered'}_

**Explainable Rationale:**  
{explanation}

**Specific Trigger Fields:**

{_format_trigger_table(trigger_fields)}

**Recommended Human Investigation Action:**
1. Summon Sub-Registry Office Volume Register Book for cited Deed(s).
2. Cross-verify AC Land Mutation Case Record and Khatian Ledger.
3. Verify Biometric NID records of both Seller and Buyer parties.
4. Record official administrative determination.

---
"""

    md += """
## 4. Auditor Sign-Off & Verification

| Role | Officer Name & Designation | Signature | Date |
| :--- | :--- | :--- | :--- |
| **Investigating Land Officer** | _____________________________ | __________________ | ____ / ____ / 20___ |
| **Sub-Registrar / AC Land** | _____________________________ | __________________ | ____ / ____ / 20___ |

_Report electronically compiled by JomiGuard Anomaly Detection Suite._
"""
    return md
