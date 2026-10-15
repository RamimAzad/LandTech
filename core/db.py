"""
Database Access Layer for JomiGuard.
Handles SQLite operations, transactional queries, anomaly injections, and alert persistence.
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
import pandas as pd

from core.models import AnomalyAlert, TriageStatus, SeverityLevel


DEFAULT_DB_PATH = "jomiguard.db"


def get_connection(db_path: str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """Returns a connection to SQLite with row factory enabled."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db_if_needed(db_path: str = DEFAULT_DB_PATH, schema_path: str = "data/schema.sql") -> None:
    """Ensures database exists and schema is loaded."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Check if plots table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='plots'")
    if not cursor.fetchone():
        from data.generator import seed_database
        seed_database(db_path, schema_path)
    conn.close()


def get_all_plots(db_path: str = DEFAULT_DB_PATH) -> pd.DataFrame:
    """Retrieves all registered plots."""
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query("SELECT * FROM plots ORDER BY plot_id", conn)


def get_all_deeds(db_path: str = DEFAULT_DB_PATH) -> pd.DataFrame:
    """Retrieves all registered sale deeds."""
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query("SELECT * FROM deeds ORDER BY registration_date DESC", conn)


def get_all_mutations(db_path: str = DEFAULT_DB_PATH) -> pd.DataFrame:
    """Retrieves all land mutation (Namjari) records."""
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query("SELECT * FROM mutations ORDER BY mutation_date DESC", conn)


def get_all_alerts(
    db_path: str = DEFAULT_DB_PATH,
    severity: Optional[str] = None,
    triage_status: Optional[str] = None
) -> pd.DataFrame:
    """Retrieves anomaly alerts with optional filters."""
    query = "SELECT * FROM alerts WHERE 1=1"
    params = []
    
    if severity and severity != "ALL":
        query += " AND severity = ?"
        params.append(severity)
        
    if triage_status and triage_status != "ALL":
        query += " AND triage_status = ?"
        params.append(triage_status)
        
    query += " ORDER BY CASE severity WHEN 'CRITICAL' THEN 1 WHEN 'HIGH' THEN 2 WHEN 'MEDIUM' THEN 3 ELSE 4 END, created_at DESC"
    
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(query, conn, params=params)


def get_plot_details(plot_id: str, db_path: str = DEFAULT_DB_PATH) -> Optional[Dict[str, Any]]:
    """Retrieves full details for a single plot."""
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM plots WHERE plot_id = ?", (plot_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def get_plot_transactions(plot_id: str, db_path: str = DEFAULT_DB_PATH) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Retrieves all deeds and mutations associated with a plot."""
    with sqlite3.connect(db_path) as conn:
        deeds_df = pd.read_sql_query(
            "SELECT * FROM deeds WHERE plot_id = ? ORDER BY registration_date ASC",
            conn,
            params=(plot_id,)
        )
        mutations_df = pd.read_sql_query(
            "SELECT * FROM mutations WHERE plot_id = ? ORDER BY mutation_date ASC",
            conn,
            params=(plot_id,)
        )
        return deeds_df, mutations_df


def search_plots(query_text: str, db_path: str = DEFAULT_DB_PATH) -> pd.DataFrame:
    """
    Search plots by plot_id, dag_no, khatian_no, owner_name, mouza, or party NID.
    """
    cleaned = f"%{query_text.strip()}%"
    sql = """
    SELECT DISTINCT p.* FROM plots p
    LEFT JOIN deeds d ON p.plot_id = d.plot_id
    LEFT JOIN mutations m ON p.plot_id = m.plot_id
    WHERE p.plot_id LIKE ? 
       OR p.dag_no LIKE ? 
       OR p.khatian_no LIKE ? 
       OR p.mouza LIKE ? 
       OR p.initial_owner_name LIKE ? 
       OR p.initial_owner_nid LIKE ?
       OR d.deed_no LIKE ?
       OR d.seller_name LIKE ?
       OR d.buyer_name LIKE ?
       OR m.applicant_name LIKE ?
       OR m.mutation_case_no LIKE ?
    ORDER BY p.plot_id
    """
    params = [cleaned] * 11
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(sql, conn, params=params)


def save_alerts(alerts: List[AnomalyAlert], db_path: str = DEFAULT_DB_PATH) -> int:
    """
    Persists detected alerts into the alerts table.
    Preserves existing triage_status and reviewer_notes if an alert already exists.
    """
    conn = get_connection(db_path)
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for alert in alerts:
        # Check if alert already exists
        cursor.execute("SELECT triage_status, reviewer_notes FROM alerts WHERE alert_id = ?", (alert.alert_id,))
        existing = cursor.fetchone()
        
        if existing:
            triage_status = existing["triage_status"]
            reviewer_notes = existing["reviewer_notes"]
            cursor.execute("""
                UPDATE alerts SET
                    rule_id = ?,
                    rule_name = ?,
                    plot_id = ?,
                    severity = ?,
                    title = ?,
                    explanation = ?,
                    trigger_fields_json = ?,
                    evidence_json = ?,
                    updated_at = ?
                WHERE alert_id = ?
            """, (
                alert.rule_id,
                alert.rule_name,
                alert.plot_id,
                alert.severity,
                alert.title,
                alert.explanation,
                alert.trigger_fields_json(),
                alert.evidence_json(),
                now_str,
                alert.alert_id
            ))
        else:
            cursor.execute("""
                INSERT INTO alerts (
                    alert_id, rule_id, rule_name, plot_id, severity, title, explanation,
                    trigger_fields_json, evidence_json, triage_status, reviewer_notes,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                alert.alert_id,
                alert.rule_id,
                alert.rule_name,
                alert.plot_id,
                alert.severity,
                alert.title,
                alert.explanation,
                alert.trigger_fields_json(),
                alert.evidence_json(),
                alert.triage_status,
                alert.reviewer_notes,
                now_str,
                now_str
            ))
            
    conn.commit()
    conn.close()
    return len(alerts)


def update_alert_triage(
    alert_id: str,
    new_status: str,
    reviewer_notes: str,
    db_path: str = DEFAULT_DB_PATH
) -> bool:
    """Updates the triage status and review notes for an alert."""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE alerts SET
                triage_status = ?,
                reviewer_notes = ?,
                updated_at = ?
            WHERE alert_id = ?
        """, (new_status, reviewer_notes, now_str, alert_id))
        conn.commit()
        return cursor.rowcount > 0


# -------------------------------------------------------------
# Demo / Anomaly Injection Utilities
# -------------------------------------------------------------

def inject_duplicate_sale(
    plot_id: str,
    seller_nid: str,
    seller_name: str,
    buyer_nid: str,
    buyer_name: str,
    transferred_area: float,
    deed_value: float,
    reg_date: str,
    db_path: str = DEFAULT_DB_PATH
) -> str:
    """Injects a conflicting double-sale deed."""
    deed_no = f"INJ-DUP-{int(datetime.now().timestamp())}"
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO deeds (
                deed_no, plot_id, registration_date, seller_nid, seller_name,
                buyer_nid, buyer_name, transferred_area_decimals, deed_value_bdt,
                sub_registry_office, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            deed_no, plot_id, reg_date, seller_nid, seller_name,
            buyer_nid, buyer_name, transferred_area, deed_value,
            "Central Sub-Registry Office", "Active"
        ))
        conn.commit()
    return deed_no


def inject_area_mismatch(
    deed_no: str,
    inflated_area: float,
    db_path: str = DEFAULT_DB_PATH
) -> str:
    """Injects or updates a mutation with inflated area."""
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM deeds WHERE deed_no = ?", (deed_no,))
        deed = cursor.fetchone()
        if not deed:
            raise ValueError(f"Deed {deed_no} not found")
            
        case_no = f"INJ-MUT-{int(datetime.now().timestamp())}"
        cursor.execute("""
            INSERT INTO mutations (
                mutation_case_no, deed_no, plot_id, mutation_date, applicant_nid,
                applicant_name, mutated_area_decimals, new_khatian_no, ac_land_office, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            case_no, deed_no, deed["plot_id"], datetime.now().strftime("%Y-%m-%d"),
            deed["buyer_nid"], deed["buyer_name"], inflated_area,
            f"DP-INJ-{int(datetime.now().timestamp()) % 10000}",
            "AC Land Office Sandbox", "Approved"
        ))
        conn.commit()
    return case_no


def inject_identity_mismatch(
    deed_no: str,
    impostor_name: str,
    impostor_nid: str,
    db_path: str = DEFAULT_DB_PATH
) -> str:
    """Injects a mutation with mismatched applicant identity."""
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM deeds WHERE deed_no = ?", (deed_no,))
        deed = cursor.fetchone()
        if not deed:
            raise ValueError(f"Deed {deed_no} not found")
            
        case_no = f"INJ-ID-{int(datetime.now().timestamp())}"
        cursor.execute("""
            INSERT INTO mutations (
                mutation_case_no, deed_no, plot_id, mutation_date, applicant_nid,
                applicant_name, mutated_area_decimals, new_khatian_no, ac_land_office, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            case_no, deed_no, deed["plot_id"], datetime.now().strftime("%Y-%m-%d"),
            impostor_nid, impostor_name, deed["transferred_area_decimals"],
            f"DP-ID-{int(datetime.now().timestamp()) % 10000}",
            "AC Land Office Sandbox", "Approved"
        ))
        conn.commit()
    return case_no


def inject_temporal_paradox(
    deed_no: str,
    db_path: str = DEFAULT_DB_PATH
) -> str:
    """Injects a mutation that has an approval date earlier than deed registration date."""
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM deeds WHERE deed_no = ?", (deed_no,))
        deed = cursor.fetchone()
        if not deed:
            raise ValueError(f"Deed {deed_no} not found")
            
        # Parse deed registration date and subtract 90 days
        deed_date = datetime.strptime(deed["registration_date"], "%Y-%m-%d")
        paradox_date = (deed_date - pd.Timedelta(days=90)).strftime("%Y-%m-%d")
        
        case_no = f"INJ-TIME-{int(datetime.now().timestamp())}"
        cursor.execute("""
            INSERT INTO mutations (
                mutation_case_no, deed_no, plot_id, mutation_date, applicant_nid,
                applicant_name, mutated_area_decimals, new_khatian_no, ac_land_office, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            case_no, deed_no, deed["plot_id"], paradox_date,
            deed["buyer_nid"], deed["buyer_name"], deed["transferred_area_decimals"],
            f"DP-TIME-{int(datetime.now().timestamp()) % 10000}",
            "AC Land Office Sandbox", "Approved"
        ))
        conn.commit()
    return case_no
