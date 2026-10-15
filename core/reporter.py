"""
Report Generation Module for JomiGuard.
Generates structured downloadable reports in CSV, Markdown, and Printable HTML formats.
"""

from datetime import datetime
import json
from typing import Dict, List, Any
import pandas as pd


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
```json
{json.dumps(trigger_fields, indent=2, ensure_ascii=False)}
```

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
