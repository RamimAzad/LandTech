"""
JomiGuard — Land Fraud & Double-Selling Alert System
Streamlit Dashboard Application
"""

import html
import json
from datetime import datetime
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from core.models import SeverityLevel, TriageStatus
from core.db import (
    init_db_if_needed,
    get_all_plots,
    get_all_deeds,
    get_all_mutations,
    get_all_alerts,
    get_plot_details,
    get_plot_transactions,
    search_plots,
    update_alert_triage,
    inject_duplicate_sale,
    inject_area_mismatch,
    inject_identity_mismatch,
    inject_temporal_paradox,
    DEFAULT_DB_PATH
)
from core.detector import run_detection
from core.reporter import export_alerts_to_csv, generate_markdown_audit_report
from data.generator import seed_database


# Page Configuration
st.set_page_config(
    page_title="JomiGuard — Land Fraud & Double-Selling Alert System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling — modern, clean design system
st.markdown("""
<style>
    :root {
        --jg-bg: #F7F8FC;
        --jg-surface: #FFFFFF;
        --jg-ink: #0F172A;
        --jg-muted: #64748B;
        --jg-border: #E6E9F0;
        --jg-primary: #4F46E5;
        --jg-primary-soft: #EEF0FF;
        --jg-radius: 14px;
        --jg-shadow: 0 1px 2px rgba(15, 23, 42, 0.04), 0 8px 24px -12px rgba(15, 23, 42, 0.12);
    }

    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Inter, Roboto, "Helvetica Neue", Arial, sans-serif;
        color: var(--jg-ink);
    }

    .stApp {
        background: var(--jg-bg);
    }

    /* Blend Streamlit's fixed top bar with the page so there is no seam */
    [data-testid="stAppViewContainer"] {
        background: var(--jg-bg);
    }
    [data-testid="stHeader"] {
        background: transparent;
        backdrop-filter: none;
        box-shadow: none;
        border-bottom: none;
    }
    [data-testid="stDecoration"] {
        display: none;
    }

    /* Tighten default vertical rhythm */
    .block-container {
        padding-top: 2.6rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column"] > [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: var(--jg-radius);
    }

    /* ---------- Headers ---------- */
    .main-header {
        font-size: 1.9rem;
        font-weight: 750;
        letter-spacing: -0.02em;
        color: var(--jg-ink);
        margin-bottom: 0.15rem;
        line-height: 1.2;
    }
    .sub-header {
        font-size: 1rem;
        color: var(--jg-muted);
        margin-bottom: 1.4rem;
    }

    /* ---------- Notice / disclaimer ---------- */
    .disclaimer-card {
        background: #FFFBEB;
        border: 1px solid #FDE68A;
        border-left: 4px solid #F59E0B;
        padding: 14px 18px;
        border-radius: 12px;
        color: #78350F;
        font-size: 0.92rem;
        line-height: 1.55;
        margin-bottom: 1.4rem;
    }

    /* ---------- Claim / KPI cards ---------- */
    .kpi-card {
        background: var(--jg-surface);
        border: 1px solid var(--jg-border);
        border-radius: var(--jg-radius);
        padding: 18px 18px 16px;
        box-shadow: var(--jg-shadow);
        height: 100%;
    }
    .kpi-label {
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        color: var(--jg-muted);
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 1.75rem;
        font-weight: 750;
        letter-spacing: -0.02em;
        color: var(--jg-ink);
        line-height: 1.1;
    }
    .kpi-foot {
        font-size: 0.8rem;
        color: var(--jg-muted);
        margin-top: 6px;
    }

    /* ---------- Plot record cards ---------- */
    .record-card {
        background: var(--jg-surface);
        border: 1px solid var(--jg-border);
        border-radius: var(--jg-radius);
        padding: 16px 18px;
        box-shadow: var(--jg-shadow);
        height: 100%;
    }
    .record-label {
        font-size: 0.74rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: var(--jg-muted);
        margin-bottom: 4px;
    }
    .record-value {
        font-size: 1.15rem;
        font-weight: 700;
        color: var(--jg-ink);
        word-break: break-word;
    }
    .record-foot {
        font-size: 0.82rem;
        color: var(--jg-muted);
        margin-top: 4px;
    }

    /* ---------- Severity pills ---------- */
    .badge-critical, .badge-high, .badge-medium, .badge-low {
        display: inline-block;
        padding: 3px 11px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.72rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        line-height: 1.6;
    }
    .badge-critical { background: #FEE2E2; color: #B91C1C; }
    .badge-high     { background: #FFEDD5; color: #C2410C; }
    .badge-medium   { background: #FEF3C7; color: #B45309; }
    .badge-low      { background: #E0E7FF; color: #4338CA; }

    /* ---------- Trigger / evidence box ---------- */
    .trigger-box {
        background: var(--jg-primary-soft);
        border: 1px solid #DDE1FF;
        border-left: 4px solid var(--jg-primary);
        padding: 12px 14px;
        border-radius: 10px;
        margin: 8px 0;
    }

    /* ---------- Trigger field fact grid ---------- */
    .tf-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 10px;
        margin: 6px 0 4px;
    }
    .tf-item {
        background: #FFFFFF;
        border: 1px solid var(--jg-border);
        border-left: 3px solid #CBD5E1;
        border-radius: 10px;
        padding: 10px 13px;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);
    }
    .tf-label {
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: var(--jg-muted);
        margin-bottom: 4px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .tf-value {
        font-size: 0.92rem;
        font-weight: 650;
        color: var(--jg-ink);
        word-break: break-word;
        font-variant-numeric: tabular-nums;
    }
    .tf-item.tf-flag { border-left-color: #DC2626; background: #FEF2F2; }
    .tf-item.tf-flag .tf-value { color: #B91C1C; }
    .tf-item.tf-ok { border-left-color: #16A34A; background: #F0FDF4; }
    .tf-item.tf-ok .tf-value { color: #15803D; }
    .tf-item.tf-warn { border-left-color: #F59E0B; background: #FFFBEB; }
    .tf-item.tf-warn .tf-value { color: #B45309; }

    /* ---------- Timeline event legend ---------- */
    .tl-legend {
        display: flex;
        flex-direction: column;
        gap: 6px;
        margin: 4px 0 8px;
    }
    .tl-item {
        display: flex;
        align-items: center;
        gap: 12px;
        background: #FFFFFF;
        border: 1px solid var(--jg-border);
        border-radius: 10px;
        padding: 9px 14px;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);
    }
    .tl-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        flex: 0 0 auto;
    }
    .tl-idx {
        flex: 0 0 auto;
        width: 22px;
        height: 22px;
        border-radius: 50%;
        background: var(--jg-primary-soft);
        color: #4338CA;
        font-size: 0.72rem;
        font-weight: 750;
        display: inline-flex;
        align-items: center;
        justify-content: center;
    }
    .tl-date {
        flex: 0 0 auto;
        font-size: 0.8rem;
        color: var(--jg-muted);
        font-variant-numeric: tabular-nums;
        min-width: 92px;
    }
    .tl-event {
        font-size: 0.9rem;
        color: var(--jg-ink);
        font-weight: 500;
    }

    /* ---------- Record comparison table ---------- */
    .cmp-table {
        border: 1px solid var(--jg-border);
        border-radius: 12px;
        overflow: hidden;
        background: var(--jg-surface);
        box-shadow: var(--jg-shadow);
        margin: 4px 0 8px;
    }
    .cmp-table .cmp-grid {
        display: grid;
        grid-template-columns: 1.1fr 1.6fr 1.6fr;
    }
    .cmp-table.single .cmp-grid {
        grid-template-columns: 1.1fr 1fr;
    }
    .cmp-table .cmp-head > div {
        padding: 11px 16px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: var(--jg-muted);
        background: #F8FAFC;
        border-bottom: 1px solid var(--jg-border);
    }
    .cmp-table .cmp-head > div.cmp-col-left::before {
        content: "";
        display: inline-block;
        width: 8px; height: 8px;
        border-radius: 50%;
        background: #94A3B8;
        margin-right: 8px;
    }
    .cmp-table .cmp-head > div.cmp-col-right::before {
        content: "";
        display: inline-block;
        width: 8px; height: 8px;
        border-radius: 50%;
        background: var(--jg-primary);
        margin-right: 8px;
    }
    .cmp-table .cmp-row { display: contents; }
    .cmp-table .cmp-field,
    .cmp-table .cmp-cell {
        padding: 10px 16px;
        font-size: 0.9rem;
        border-bottom: 1px solid #F1F5F9;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .cmp-table .cmp-field {
        color: var(--jg-muted);
        font-weight: 600;
        background: #FCFCFE;
    }
    .cmp-table .cmp-cell {
        color: var(--jg-ink);
        font-weight: 500;
        word-break: break-word;
    }
    .cmp-table .cmp-row:last-child .cmp-field,
    .cmp-table .cmp-row:last-child .cmp-cell {
        border-bottom: none;
    }
    .cmp-table .cmp-row.is-diff .cmp-field {
        background: #FFF7ED;
        color: #9A3412;
        font-weight: 700;
    }
    .cmp-table .cmp-row.is-diff .cmp-field::before {
        content: "!";
        flex: 0 0 auto;
        width: 16px; height: 16px;
        border-radius: 50%;
        background: #F59E0B;
        color: #FFFFFF;
        font-size: 0.66rem;
        font-weight: 800;
        display: inline-flex;
        align-items: center;
        justify-content: center;
    }
    .cmp-table .cmp-row.is-diff .cmp-cell {
        background: #FFFDF8;
        color: #7C2D12;
        font-weight: 700;
    }
    .cmp-table .cmp-row.is-diff .cmp-cell.cmp-shifted {
        box-shadow: inset 0 0 0 9999px #FFF7ED;
    }
    .cmp-empty { color: #CBD5E1; font-weight: 400; font-style: italic; }
    .cmp-legend {
        display: flex;
        align-items: center;
        gap: 18px;
        margin: 6px 0 10px;
        font-size: 0.8rem;
        color: var(--jg-muted);
    }
    .cmp-legend .dot {
        display: inline-block;
        width: 8px; height: 8px;
        border-radius: 50%;
        margin-right: 6px;
    }

    /* ---------- Metrics (native st.metric) ---------- */
    [data-testid="stMetric"] {
        background: var(--jg-surface);
        border: 1px solid var(--jg-border);
        border-radius: var(--jg-radius);
        padding: 16px 18px;
        box-shadow: var(--jg-shadow);
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        color: var(--jg-muted) !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.55rem !important;
        font-weight: 750 !important;
        letter-spacing: -0.02em;
        color: var(--jg-ink) !important;
    }

    /* ---------- Buttons ---------- */
    .stButton > button, .stDownloadButton > button {
        border-radius: 10px;
        border: 1px solid var(--jg-border);
        font-weight: 600;
        transition: all 0.15s ease;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        border-color: var(--jg-primary);
        color: var(--jg-primary);
        transform: translateY(-1px);
    }
    .stButton > button[kind="primary"], .stDownloadButton > button[kind="primary"] {
        background: var(--jg-primary);
        border-color: var(--jg-primary);
    }
    .stButton > button[kind="primary"]:hover, .stDownloadButton > button[kind="primary"]:hover {
        background: #4338CA;
        color: #FFFFFF;
    }

    /* ---------- Expanders / containers / dataframes ---------- */
    [data-testid="stExpander"] {
        border: 1px solid var(--jg-border);
        border-radius: 12px;
        background: var(--jg-surface);
        box-shadow: var(--jg-shadow);
        overflow: hidden;
    }
    [data-testid="stExpander"] summary {
        font-weight: 600;
    }
    [data-testid="stDataFrame"], [data-testid="stTable"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid var(--jg-border);
    }
    div[data-testid="stAlert"] {
        border-radius: 12px;
    }

    /* ---------- Tabs ---------- */
    [data-testid="stTabs"] [data-baseweb="tab-list"] {
        gap: 6px;
        border-bottom: 1px solid var(--jg-border);
    }
    [data-testid="stTabs"] [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 8px 16px;
        font-weight: 600;
    }
    [data-testid="stTabs"] [aria-selected="true"] {
        color: var(--jg-primary);
    }

    /* ---------- Sidebar ---------- */
    [data-testid="stSidebar"] {
        background: #FFFFFF;
        border-right: 1px solid var(--jg-border);
    }
    [data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem;
    }
    .brand-box {
        background: linear-gradient(135deg, #4F46E5 0%, #6366F1 55%, #8B5CF6 100%);
        border-radius: 16px;
        padding: 18px 18px 16px;
        color: #FFFFFF;
        margin-bottom: 4px;
        box-shadow: 0 12px 30px -14px rgba(79, 70, 229, 0.7);
    }
    .brand-title {
        font-size: 1.25rem;
        font-weight: 750;
        letter-spacing: -0.01em;
        margin: 0;
    }
    .brand-sub {
        font-size: 0.8rem;
        opacity: 0.9;
        margin-top: 4px;
        line-height: 1.4;
    }
    [data-testid="stSidebar"] [role="radiogroup"] {
        gap: 4px;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label {
        border-radius: 10px;
        padding: 8px 10px;
        transition: background 0.15s ease;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label:hover {
        background: var(--jg-primary-soft);
    }

    .section-title {
        font-size: 1.15rem;
        font-weight: 700;
        letter-spacing: -0.01em;
        margin: 0.4rem 0 0.8rem;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# EVIDENCE COMPARISON RENDERING HELPERS
# -----------------------------------------------------------------------------
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
    "approved_by": "Approved By",
    "remarks": "Remarks",
    "deed_registration_date": "Deed Registration Date",
    "days_preceding_deed": "Days Preceding Deed",
    "seller_recorded_balance": "Seller Recorded Balance (dec)",
    "attempted_transfer": "Attempted Transfer (dec)",
    "registry_lookup_result": "Registry Lookup Result",
    "verified_owners_at_execution": "Verified Owners at Execution",
    "variance": "Variance",
    "conflict_type": "Conflict Type",
    "days_between_sales": "Days Between Sales",
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
    "deed_2_no": "Second Deed No",
    "deed_2_date": "Second Deed Date",
    "deed_2_buyer": "Second Deed Buyer",
    "deed_2_area_decimals": "Second Deed Area (dec)",
    "deed_1_no": "First Deed No",
    "deed_1_date": "First Deed Date",
    "deed_1_buyer": "First Deed Buyer",
    "deed_1_area_decimals": "First Deed Area (dec)",
    "plot_initial_owner": "Plot Initial Owner",
    "plot_initial_owner_nid": "Plot Initial Owner NID",
    "inversion_days": "Chronological Inversion (days)",
    "direction": "Direction",
    "recipient_name": "Recipient Name",
    "recipient_nid": "Recipient NID",
}


def _pretty_field(key):
    return _FIELD_LABELS.get(key, str(key).replace("_", " ").title())


def _pretty_value(value):
    if value is None or value == "":
        return '<span class="cmp-empty">—</span>'
    if isinstance(value, bool):
        return html.escape(str(value))
    if isinstance(value, (int, float)):
        if isinstance(value, float) and not value.is_integer():
            return f"{value:,.2f}"
        return f"{int(value):,}"
    return html.escape(str(value))


def render_comparison_table(left, right, left_title, right_title):
    """Render a clean field-by-field comparison with differing rows highlighted."""
    left = left or {}
    right = right or {}

    ordered_keys = list(left.keys())
    ordered_keys += [k for k in right.keys() if k not in left]

    rows_html = []
    for key in ordered_keys:
        in_left = key in left
        in_right = key in right
        is_diff = in_left and in_right and str(left[key]) != str(right[key])

        left_cell = _pretty_value(left[key]) if in_left else '<span class="cmp-empty">—</span>'
        right_cell = _pretty_value(right[key]) if in_right else '<span class="cmp-empty">—</span>'

        row_class = "cmp-row is-diff" if is_diff else "cmp-row"
        rows_html.append(f"""
        <div class="{row_class}">
            <div class="cmp-field">{html.escape(_pretty_field(key))}</div>
            <div class="cmp-cell">{left_cell}</div>
            <div class="cmp-cell">{right_cell}</div>
        </div>""")

    anchor_left = html.escape(str(left.get("deed_no") or left.get("mutation_case_no") or "Record A"))
    anchor_right = html.escape(str(right.get("deed_no") or right.get("mutation_case_no") or "Record B"))

    st.markdown(f"""
    <div class="cmp-table">
        <div class="cmp-grid cmp-head">
            <div>Field</div>
            <div class="cmp-col-left">{html.escape(left_title)} · <code>{anchor_left}</code></div>
            <div class="cmp-col-right">{html.escape(right_title)} · <code>{anchor_right}</code></div>
        </div>
        <div class="cmp-grid">{''.join(rows_html)}
        </div>
    </div>
    """, unsafe_allow_html=True)


def _flatten_record(data, prefix=""):
    """Flatten a record (with nested dicts/lists) into ordered label -> value items."""
    items = []
    for key, value in data.items():
        label = _pretty_field(key)
        if isinstance(value, dict):
            label = _FIELD_LABELS.get(prefix + key, label)
            for sub_key, sub_val in value.items():
                items.append((_pretty_field(sub_key), sub_val))
        elif isinstance(value, (list, tuple)):
            items.append((label, ", ".join(str(v) for v in value)))
        else:
            items.append((label, value))
    return items


def render_record_table(data, title="Evidence Record"):
    """Render a single record as a clean Field / Value table."""
    rows_html = []
    for label, value in _flatten_record(data):
        rows_html.append(f"""
        <div class="cmp-row">
            <div class="cmp-field">{html.escape(str(label))}</div>
            <div class="cmp-cell">{_pretty_value(value)}</div>
        </div>""")

    st.markdown(f"""
    <div class="cmp-table single">
        <div class="cmp-grid cmp-head">
            <div>Field</div>
            <div class="cmp-col-right">{html.escape(title)}</div>
        </div>
        <div class="cmp-grid">{''.join(rows_html)}
        </div>
    </div>
    """, unsafe_allow_html=True)


_TRIGGER_FLAG_KEYS = (
    "discrepancy", "excess", "inversion", "days_between",
    "days_preceding", "variance", "defect", "mismatch",
)


def render_trigger_fields(trigger_data):
    """Render triggered fields as a clean, color-coded fact grid."""
    if not trigger_data:
        st.info("No trigger fields were recorded for this alert.")
        return

    items_html = []
    for key, value in trigger_data.items():
        label = html.escape(_pretty_field(key))

        if isinstance(value, bool):
            cls = "tf-item tf-ok" if value else "tf-item tf-flag"
            display = "Yes" if value else "No"
        else:
            cls = "tf-item"
            if any(flag in str(key).lower() for flag in _TRIGGER_FLAG_KEYS):
                cls += " tf-warn"
            display = _pretty_value(value)

        items_html.append(
            f'<div class="{cls}">'
            f'<div class="tf-label" title="{label}">{label}</div>'
            f'<div class="tf-value">{display}</div>'
            f'</div>'
        )

    st.markdown(f'<div class="tf-grid">{"".join(items_html)}</div>', unsafe_allow_html=True)


# Initialize Database and Run Detector once
init_db_if_needed(DEFAULT_DB_PATH)
if "last_scan_metrics" not in st.session_state:
    alerts, summary = run_detection(DEFAULT_DB_PATH)
    st.session_state["last_scan_metrics"] = summary


# -----------------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="brand-box">
        <p class="brand-title">🛡️ JomiGuard</p>
        <p class="brand-sub">Land Fraud & Double-Selling Alert System</p>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Rule-based anomaly detection & explainable risk screening")
    st.markdown("")
    
    nav_option = st.radio(
        "Navigation",
        [
            "📊 Dashboard Overview",
            "🚨 Alerts & Risk Investigation",
            "🔍 Searchable Plot History",
            "🧪 Interactive Demo & Sandbox",
            "📑 Downloadable Reports"
        ],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("##### ⚙️ Quick Actions")
    
    if st.button("🔄 Re-run Anomaly Scan", use_container_width=True):
        alerts, summary = run_detection(DEFAULT_DB_PATH)
        st.session_state["last_scan_metrics"] = summary
        st.success(f"Scan complete! {len(alerts)} inconsistencies flagged.")
        st.rerun()
        
    if st.button("🔁 Reset Benchmark Data", use_container_width=True):
        p, d, m = seed_database(DEFAULT_DB_PATH)
        alerts, summary = run_detection(DEFAULT_DB_PATH)
        st.session_state["last_scan_metrics"] = summary
        st.info("Database reset to original clean benchmark seed.")
        st.rerun()
        
    st.markdown("")
    st.caption("JomiGuard Land Prototype v1.0 • SQLite Engine")


# -----------------------------------------------------------------------------
# VIEW 1: DASHBOARD OVERVIEW
# -----------------------------------------------------------------------------
if nav_option == "📊 Dashboard Overview":
    st.markdown('<div class="main-header">🛡️ JomiGuard Operational Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Automated screening of deed registrations, land mutations, and parcel integrity</div>', unsafe_allow_html=True)
    
    # Official Administrative Disclaimer
    st.markdown("""
    <div class="disclaimer-card">
        <strong>⚠️ Administrative & Legal Notice:</strong>
        An alert indicates a <em>possible procedural discrepancy or record inconsistency</em>, <strong>not proven fraud</strong>. 
        Repeated plot identifiers, mismatched areas, or missing records can have legitimate legal explanations (e.g., unrecorded inheritance partitions, partial surveys, or court decrees) and strictly require human review by authorized Land Revenue and Sub-Registry Officers.
    </div>
    """, unsafe_allow_html=True)
    
    plots_df = get_all_plots(DEFAULT_DB_PATH)
    deeds_df = get_all_deeds(DEFAULT_DB_PATH)
    mutations_df = get_all_mutations(DEFAULT_DB_PATH)
    alerts_df = get_all_alerts(DEFAULT_DB_PATH)
    
    # Metrics Strip
    critical_count = len(alerts_df[alerts_df["severity"] == "CRITICAL"]) if not alerts_df.empty else 0
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Plots Screened</div>
            <div class="kpi-value">{len(plots_df)}</div>
            <div class="kpi-foot">Parcels under integrity review</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Registered Deeds</div>
            <div class="kpi-value">{len(deeds_df)}</div>
            <div class="kpi-foot">Sub-Registry sale records</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Approved Mutations</div>
            <div class="kpi-value">{len(mutations_df)}</div>
            <div class="kpi-foot">AC Land revenue transfers</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Active Inconsistencies</div>
            <div class="kpi-value">{len(alerts_df)}</div>
            <div class="kpi-foot">{critical_count} flagged critical</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("")
    
    # Charts Row
    ch_col1, ch_col2 = st.columns(2)
    
    with ch_col1:
        st.subheader("Inconsistencies by Severity")
        if not alerts_df.empty:
            sev_counts = alerts_df["severity"].value_counts().reset_index()
            sev_counts.columns = ["Severity", "Count"]
            color_map = {
                "CRITICAL": "#DC2626",
                "HIGH": "#EA580C",
                "MEDIUM": "#D97706",
                "LOW": "#2563EB"
            }
            fig_sev = px.pie(
                sev_counts,
                names="Severity",
                values="Count",
                color="Severity",
                color_discrete_map=color_map,
                hole=0.45,
            )
            fig_sev.update_traces(textposition='inside', textinfo='percent+label')
            fig_sev.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=300)
            st.plotly_chart(fig_sev, use_container_width=True)
        else:
            st.info("No active inconsistencies detected.")
            
    with ch_col2:
        st.subheader("Inconsistencies by Rule Category")
        if not alerts_df.empty:
            rule_counts = alerts_df["rule_name"].value_counts().reset_index()
            rule_counts.columns = ["Rule Name", "Incidents"]
            fig_rule = px.bar(
                rule_counts,
                x="Incidents",
                y="Rule Name",
                orientation="h",
                color="Incidents",
                color_continuous_scale="Reds"
            )
            fig_rule.update_layout(
                yaxis={'categoryorder': 'total ascending'},
                margin=dict(t=10, b=10, l=10, r=10),
                height=300
            )
            st.plotly_chart(fig_rule, use_container_width=True)
        else:
            st.info("No active inconsistencies detected.")

    st.markdown("")
    st.markdown('<div class="section-title">🚨 Priority Inconsistency Ledger</div>', unsafe_allow_html=True)
    
    if not alerts_df.empty:
        display_df = alerts_df[[
            "alert_id", "severity", "plot_id", "rule_name", "title", "triage_status", "created_at"
        ]].copy()
        
        st.dataframe(
            display_df,
            use_container_width=True,
            column_config={
                "alert_id": "Alert ID",
                "severity": st.column_config.TextColumn("Severity"),
                "plot_id": "Plot ID",
                "rule_name": "Triggered Rule",
                "title": "Incident Summary",
                "triage_status": "Review Status",
                "created_at": "Timestamp"
            },
            hide_index=True
        )
    else:
        st.success("All screened records are consistent with verified chain of title.")


# -----------------------------------------------------------------------------
# VIEW 2: ALERTS & EXPLAINABLE RISK INVESTIGATION
# -----------------------------------------------------------------------------
elif nav_option == "🚨 Alerts & Risk Investigation":
    st.markdown('<div class="main-header">🚨 Flagged Inconsistencies & Explainable Evidence</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Inspect specific triggered fields, compare conflicting records, and record human determinations</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="disclaimer-card">
        <strong>⚠️ Review Protocol:</strong>
        JomiGuard highlights exact conflicting parameters. Please inspect the comparison payload below, cross-reference the physical Volume Register at the Sub-Registry Office, and document your findings before modifying the review status.
    </div>
    """, unsafe_allow_html=True)
    
    # Filter Controls
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        filter_sev = st.selectbox("Filter by Severity", ["ALL", "CRITICAL", "HIGH", "MEDIUM", "LOW"])
    with f_col2:
        filter_status = st.selectbox(
            "Filter by Review Status",
            ["ALL", "Pending Review", "Under Investigation", "Marked Legitimate", "Confirmed Inconsistency"]
        )
    with f_col3:
        filter_plot = st.text_input("Filter by Plot ID", placeholder="e.g. P-201").strip().upper()
        
    alerts_df = get_all_alerts(
        DEFAULT_DB_PATH,
        severity=filter_sev,
        triage_status=filter_status
    )
    
    if filter_plot:
        alerts_df = alerts_df[alerts_df["plot_id"].str.contains(filter_plot, na=False)]
        
    st.markdown(f"<span style='color:#64748B;font-size:0.9rem;'>Showing <strong style='color:#0F172A;'>{len(alerts_df)}</strong> flagged record(s)</span>", unsafe_allow_html=True)
    
    if alerts_df.empty:
        st.info("No alerts match the selected criteria.")
    else:
        for idx, row in alerts_df.iterrows():
            aid = row["alert_id"]
            sev = row["severity"]
            pid = row["plot_id"]
            r_name = row["rule_name"]
            title = row["title"]
            explanation = row["explanation"]
            status = row["triage_status"]
            notes = row["reviewer_notes"] or ""
            
            trigger_data = json.loads(row["trigger_fields_json"]) if row["trigger_fields_json"] else {}
            evidence_data = json.loads(row["evidence_json"]) if row["evidence_json"] else {}
            
            badge_class = f"badge-{sev.lower()}"
            
            with st.expander(f"[{sev}] {title} — Plot {pid} ({status})", expanded=(idx < 2)):
                st.markdown(f"""
                <span class="{badge_class}">{sev} SEVERITY</span> &nbsp;
                <strong>Rule:</strong> {r_name} &nbsp;|&nbsp; 
                <strong>Alert ID:</strong> <code>{aid}</code> &nbsp;|&nbsp;
                <strong>Plot ID:</strong> <code>{pid}</code>
                """, unsafe_allow_html=True)
                
                st.markdown("#### 💡 Explainable Detection Rationale")
                st.write(explanation)
                
                # Highlighted Trigger Fields Card
                st.markdown("#### 🔍 Specific Fields That Triggered This Alert")
                render_trigger_fields(trigger_data)
                
                # Side-by-side Evidence Comparison
                st.markdown("#### ⚖️ Conflicting Records Side-by-Side")
                if "first_deed" in evidence_data and "second_deed" in evidence_data:
                    # Double-Selling comparison
                    render_comparison_table(
                        evidence_data["first_deed"],
                        evidence_data["second_deed"],
                        "Prior Registered Deed",
                        "Subsequent Conflicting Deed"
                    )
                elif "deed_record" in evidence_data and "mutation_record" in evidence_data:
                    # Deed vs Mutation comparison
                    render_comparison_table(
                        evidence_data["deed_record"],
                        evidence_data["mutation_record"],
                        "Registered Sale Deed",
                        "Revenue Mutation Record"
                    )
                elif "deed_party" in evidence_data and "mutation_party" in evidence_data:
                    # Identity mismatch comparison
                    render_comparison_table(
                        evidence_data["deed_party"],
                        evidence_data["mutation_party"],
                        "Registered Deed Buyer",
                        "Mutation Applicant"
                    )
                else:
                    render_record_table(evidence_data, "Flagged Evidence Payload")
                    
                st.markdown("---")
                
                # Human Triage & Resolution Workflow
                st.markdown("#### ✍️ Official Determination & Case Triage")
                w_col1, w_col2, w_col3 = st.columns([2, 4, 1.5])
                
                with w_col1:
                    new_status = st.selectbox(
                        "Update Status",
                        [TriageStatus.PENDING.value, TriageStatus.INVESTIGATING.value,
                         TriageStatus.CLEARED.value, TriageStatus.CONFIRMED.value],
                        index=[TriageStatus.PENDING.value, TriageStatus.INVESTIGATING.value,
                               TriageStatus.CLEARED.value, TriageStatus.CONFIRMED.value].index(status),
                        key=f"status_select_{aid}"
                    )
                with w_col2:
                    new_notes = st.text_input(
                        "Auditor Notes / Legal Verification Reference",
                        value=notes,
                        placeholder="e.g. Cross-checked with Sub-Registry Book 4; verified boundary rectification decree.",
                        key=f"notes_input_{aid}"
                    )
                with w_col3:
                    st.write("")
                    st.write("")
                    if st.button("Save Determination", key=f"btn_save_{aid}", use_container_width=True):
                        update_alert_triage(aid, new_status, new_notes, DEFAULT_DB_PATH)
                        st.success("Triage updated!")
                        st.rerun()


# -----------------------------------------------------------------------------
# VIEW 3: SEARCHABLE PLOT HISTORY & TIMELINE
# -----------------------------------------------------------------------------
elif nav_option == "🔍 Searchable Plot History":
    st.markdown('<div class="main-header">🔍 Searchable Plot History & Chain of Title</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Search any parcel to reconstruct its chronological deed ledger and revenue mutation history</div>', unsafe_allow_html=True)
    
    search_query = st.text_input(
        "Search by Plot ID, Dag No, Khatian No, Deed No, NID, or Owner Name",
        placeholder="e.g. P-201, 2401, RS-410, Fatema Begum, or 19782619827361234"
    )
    
    plots_df = get_all_plots(DEFAULT_DB_PATH)
    
    if search_query:
        matched_plots = search_plots(search_query, DEFAULT_DB_PATH)
    else:
        matched_plots = plots_df
        
    if matched_plots.empty:
        st.warning("No plots found matching your search query.")
    else:
        st.markdown(f"<span style='color:#64748B;font-size:0.9rem;'>Found <strong style='color:#0F172A;'>{len(matched_plots)}</strong> plot(s)</span>", unsafe_allow_html=True)
        selected_plot_id = st.selectbox(
            "Select Plot to Inspect Detailed Chain of Title",
            options=matched_plots["plot_id"].tolist(),
            format_func=lambda x: f"Plot {x} — {matched_plots[matched_plots['plot_id']==x]['mouza'].values[0]} (Dag: {matched_plots[matched_plots['plot_id']==x]['dag_no'].values[0]}, Area: {matched_plots[matched_plots['plot_id']==x]['total_area_decimals'].values[0]} dec)"
        )
        
        plot_info = get_plot_details(selected_plot_id, DEFAULT_DB_PATH)
        deeds_df, mutations_df = get_plot_transactions(selected_plot_id, DEFAULT_DB_PATH)
        plot_alerts = get_all_alerts(DEFAULT_DB_PATH)
        if not plot_alerts.empty:
            plot_alerts = plot_alerts[plot_alerts["plot_id"] == selected_plot_id]
            
        # Plot Details Cards
        st.markdown('<div class="section-title">🗺️ Plot Registry Master Record</div>', unsafe_allow_html=True)
        p_c1, p_c2, p_c3, p_c4 = st.columns(4)
        with p_c1:
            st.markdown(f"""
            <div class="record-card">
                <div class="record-label">Mouza & JL</div>
                <div class="record-value">{plot_info['mouza']} · JL {plot_info['jl_no']}</div>
                <div class="record-foot">Thana/Upazila: {plot_info['upazila']}</div>
            </div>
            """, unsafe_allow_html=True)
        with p_c2:
            st.markdown(f"""
            <div class="record-card">
                <div class="record-label">Dag & Khatian</div>
                <div class="record-value">Dag {plot_info['dag_no']}</div>
                <div class="record-foot">Khatian: {plot_info['khatian_no']}</div>
            </div>
            """, unsafe_allow_html=True)
        with p_c3:
            st.markdown(f"""
            <div class="record-card">
                <div class="record-label">Total Land Area</div>
                <div class="record-value">{plot_info['total_area_decimals']} Decimals</div>
                <div class="record-foot">Classification: {plot_info['land_type']}</div>
            </div>
            """, unsafe_allow_html=True)
        with p_c4:
            st.markdown(f"""
            <div class="record-card">
                <div class="record-label">Initial Recorded Owner</div>
                <div class="record-value">{plot_info['initial_owner_name']}</div>
                <div class="record-foot">NID: {plot_info['initial_owner_nid']}</div>
            </div>
            """, unsafe_allow_html=True)
            
        # Alert warning if plot has flags
        if not plot_alerts.empty:
            st.error(f"🚨 This plot has {len(plot_alerts)} active inconsistency alert(s) on file! Review ledger below.")
            for _, pa in plot_alerts.iterrows():
                st.markdown(f"- **[{pa['severity']}] {pa['title']}** — _{pa['explanation']}_")
        else:
            st.success("✅ No conflicting transactions or mutation inconsistencies detected for this plot.")
            
        st.markdown("---")
        
        # Interactive Plotly Visual Timeline
        st.markdown('<div class="section-title">📈 Visual Transaction & Ownership Timeline</div>', unsafe_allow_html=True)
        
        timeline_events = []
        
        # Initial Genesis
        timeline_events.append({
            "Date": "2021-01-01",
            "Event": f"Initial Record: {plot_info['initial_owner_name']}",
            "Type": "Genesis Record",
            "Area": f"{plot_info['total_area_decimals']} dec",
            "Color": "#10B981"
        })
        
        for _, d in deeds_df.iterrows():
            timeline_events.append({
                "Date": d["registration_date"],
                "Event": f"Deed {d['deed_no']}: {d['seller_name']} ➔ {d['buyer_name']}",
                "Type": "Deed Registration",
                "Area": f"{d['transferred_area_decimals']} dec",
                "Color": "#3B82F6"
            })
            
        for _, m in mutations_df.iterrows():
            timeline_events.append({
                "Date": m["mutation_date"],
                "Event": f"Mutation {m['mutation_case_no']} (Khatian {m['new_khatian_no']})",
                "Type": "Mutation Approved",
                "Area": f"{m['mutated_area_decimals']} dec",
                "Color": "#8B5CF6"
            })
            
        df_timeline = pd.DataFrame(timeline_events).sort_values("Date").reset_index(drop=True)
        df_timeline["Index"] = df_timeline.index + 1

        fig = go.Figure()

        # Scatter line for chronological flow — numbered markers avoid label overlap
        fig.add_trace(go.Scatter(
            x=df_timeline["Date"],
            y=[1] * len(df_timeline),
            mode="lines+markers+text",
            text=[str(i) for i in df_timeline["Index"]],
            textposition="middle center",
            textfont=dict(color="#FFFFFF", size=10, family="Arial, sans-serif"),
            marker=dict(
                size=30,
                color=df_timeline["Color"],
                line=dict(color="#FFFFFF", width=2),
            ),
            line=dict(color="#CBD5E1", width=3),
            hoverinfo="text",
            hovertext=[
                f"<b>#{r['Index']} · {r['Type']}</b><br>{r['Event']}<br>Date: {r['Date']} · Area: {r['Area']}"
                for _, r in df_timeline.iterrows()
            ]
        ))

        fig.update_layout(
            height=200,
            xaxis=dict(title="Transaction Date", showgrid=True, tickfont=dict(size=11)),
            yaxis=dict(showticklabels=False, range=[0.6, 1.4], showgrid=False),
            margin=dict(l=20, r=20, t=20, b=30),
            showlegend=False,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)

        # Event legend (keeps timeline readable without overlapping labels)
        legend_html = "".join(
            f'<div class="tl-item">'
            f'<span class="tl-dot" style="background:{r.Color}"></span>'
            f'<span class="tl-idx">{r.Index}</span>'
            f'<span class="tl-date">{r.Date}</span>'
            f'<span class="tl-event">{html.escape(str(r.Event))}</span>'
            f'</div>'
            for r in df_timeline.itertuples()
        )
        st.markdown(f'<div class="tl-legend">{legend_html}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Comprehensive Ledger Tables
        t_col1, t_col2 = st.columns(2)
        with t_col1:
            st.markdown("#### 📜 Registered Deeds (Sub-Registry Office)")
            if deeds_df.empty:
                st.info("No sale deeds on file for this plot.")
            else:
                st.dataframe(
                    deeds_df[[
                        "deed_no", "registration_date", "seller_name", "buyer_name",
                        "transferred_area_decimals", "deed_value_bdt"
                    ]],
                    use_container_width=True,
                    hide_index=True
                )
                
        with t_col2:
            st.markdown("#### 🏛️ Revenue Mutations (AC Land Office)")
            if mutations_df.empty:
                st.info("No mutations recorded for this plot.")
            else:
                st.dataframe(
                    mutations_df[[
                        "mutation_case_no", "deed_no", "mutation_date", "applicant_name",
                        "mutated_area_decimals", "new_khatian_no", "status"
                    ]],
                    use_container_width=True,
                    hide_index=True
                )


# -----------------------------------------------------------------------------
# VIEW 4: INTERACTIVE DEMO & SANDBOX
# -----------------------------------------------------------------------------
elif nav_option == "🧪 Interactive Demo & Sandbox":
    st.markdown('<div class="main-header">🧪 Interactive Anomaly Injection Sandbox</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Live demonstration: Inject conflicting land sales or record mismatches and observe instant rule-based detection</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="disclaimer-card">
        <strong>💡 Demonstration Workflow:</strong>
        This sandbox allows testing the detection engine in real time. Choose a scenario below to introduce a conflicting sale or record mismatch into the SQLite database. The engine will instantly run anomaly detection, extract explainable trigger indicators, and display the resulting alert.
    </div>
    """, unsafe_allow_html=True)
    
    plots_df = get_all_plots(DEFAULT_DB_PATH)
    deeds_df = get_all_deeds(DEFAULT_DB_PATH)
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "1️⃣ Duplicate Sale Injection",
        "2️⃣ Area Mismatch Injection",
        "3️⃣ Identity Impostor Injection",
        "4️⃣ Chronological Paradox Injection"
    ])
    
    # Tab 1: Duplicate Sale
    with tab1:
        st.markdown("### Inject Conflicting Double-Selling")
        st.write("Simulates a rogue seller executing a second deed for the same plot to a different buyer.")
        
        # Select plot
        clean_plots = plots_df[~plots_df["plot_id"].isin(["P-201", "P-202"])]["plot_id"].tolist()
        c_p = st.selectbox("Select Target Plot for Injection", options=clean_plots, key="inj_p_dup")
        
        plot_info = get_plot_details(c_p, DEFAULT_DB_PATH)
        p_deeds, _ = get_plot_transactions(c_p, DEFAULT_DB_PATH)
        
        st.caption(f"Plot {c_p} — Area: {plot_info['total_area_decimals']} decimals | Initial Owner: {plot_info['initial_owner_name']}")
        
        d_col1, d_col2 = st.columns(2)
        with d_col1:
            seller_name = st.text_input("Seller Name", value=plot_info["initial_owner_name"], key="inj_s_name")
            seller_nid = st.text_input("Seller NID", value=plot_info["initial_owner_nid"], key="inj_s_nid")
        with d_col2:
            buyer_2_name = st.text_input("Second Buyer Name (Victim 2)", value="Zubair Al Mahmud", key="inj_b2_name")
            buyer_2_nid = st.text_input("Second Buyer NID", value="19952619827361999", key="inj_b2_nid")
            
        area_to_sell = st.number_input(
            "Transferred Area (decimals)",
            min_value=1.0,
            max_value=50.0,
            value=float(plot_info["total_area_decimals"]),
            key="inj_area_dup"
        )
        
        if st.button("🚨 Inject Duplicate Sale Now", key="btn_inj_dup", type="primary"):
            new_deed = inject_duplicate_sale(
                plot_id=c_p,
                seller_nid=seller_nid,
                seller_name=seller_name,
                buyer_nid=buyer_2_nid,
                buyer_name=buyer_2_name,
                transferred_area=area_to_sell,
                deed_value=area_to_sell * 400000.0,
                reg_date=datetime.now().strftime("%Y-%m-%d"),
                db_path=DEFAULT_DB_PATH
            )
            # Re-run detection
            alerts, summary = run_detection(DEFAULT_DB_PATH)
            st.session_state["last_scan_metrics"] = summary
            st.success(f"Conflicting deed {new_deed} injected! Detection engine flagged {len(alerts)} alerts.")
            st.info("Check 'Alerts & Risk Investigation' or 'Searchable Plot History' to inspect the evidence trail.")
            st.rerun()

    # Tab 2: Area Mismatch
    with tab2:
        st.markdown("### Inject Registration vs. Mutation Area Mismatch")
        st.write("Simulates unauthorized inflation of land area during revenue mutation (Namjari).")
        
        # Pick deed
        target_deed_no = st.selectbox("Select Registered Deed to Mutate", options=deeds_df["deed_no"].tolist()[:10], key="inj_deed_area")
        selected_deed = deeds_df[deeds_df["deed_no"] == target_deed_no].iloc[0]
        
        deed_area = float(selected_deed["transferred_area_decimals"])
        st.write(f"**Deed Transferred Area:** {deed_area:.2f} decimals (Buyer: {selected_deed['buyer_name']})")
        
        inflated_area = st.number_input(
            "Inflated Mutation Area (decimals)",
            min_value=deed_area + 0.1,
            max_value=deed_area + 20.0,
            value=round(deed_area + 5.0, 2),
            step=0.5,
            key="inj_inflated_val"
        )
        
        if st.button("🚨 Inject Area Inflation Now", key="btn_inj_area", type="primary"):
            new_mut = inject_area_mismatch(target_deed_no, inflated_area, DEFAULT_DB_PATH)
            alerts, summary = run_detection(DEFAULT_DB_PATH)
            st.session_state["last_scan_metrics"] = summary
            st.success(f"Inflated mutation {new_mut} injected (+{inflated_area - deed_area:.2f} decimals)! Anomaly detected.")
            st.rerun()

    # Tab 3: Identity Mismatch
    with tab3:
        st.markdown("### Inject Applicant Identity Mismatch")
        st.write("Simulates a mutation approved in favor of an unauthorized applicant instead of the registered deed buyer.")
        
        target_deed_id = st.selectbox("Select Deed", options=deeds_df["deed_no"].tolist()[:10], key="inj_deed_id")
        selected_deed_id = deeds_df[deeds_df["deed_no"] == target_deed_id].iloc[0]
        
        st.write(f"**Registered Buyer:** {selected_deed_id['buyer_name']} (NID: {selected_deed_id['buyer_nid']})")
        
        impostor_name = st.text_input("Mismatched Applicant Name", value="Akramuzzaman Khan", key="inj_imp_name")
        impostor_nid = st.text_input("Mismatched Applicant NID", value="19652619827361777", key="inj_imp_nid")
        
        if st.button("🚨 Inject Identity Mismatch Now", key="btn_inj_id", type="primary"):
            new_mut = inject_identity_mismatch(target_deed_id, impostor_name, impostor_nid, DEFAULT_DB_PATH)
            alerts, summary = run_detection(DEFAULT_DB_PATH)
            st.session_state["last_scan_metrics"] = summary
            st.success(f"Mismatched mutation {new_mut} injected! Alert triggered.")
            st.rerun()

    # Tab 4: Chronological Paradox
    with tab4:
        st.markdown("### Inject Chronological Paradox")
        st.write("Simulates a mutation record bearing an approval date earlier than the deed registration date.")
        
        target_deed_time = st.selectbox("Select Deed for Paradox", options=deeds_df["deed_no"].tolist()[:10], key="inj_deed_time")
        selected_deed_time = deeds_df[deeds_df["deed_no"] == target_deed_time].iloc[0]
        
        st.write(f"**Deed Registration Date:** {selected_deed_time['registration_date']}")
        
        if st.button("🚨 Inject Chronological Paradox Now", key="btn_inj_time", type="primary"):
            new_mut = inject_temporal_paradox(target_deed_time, DEFAULT_DB_PATH)
            alerts, summary = run_detection(DEFAULT_DB_PATH)
            st.session_state["last_scan_metrics"] = summary
            st.success(f"Paradoxical mutation {new_mut} injected (approved 90 days before deed registration)! Alert triggered.")
            st.rerun()


# -----------------------------------------------------------------------------
# VIEW 5: DOWNLOADABLE AUDIT REPORTS
# -----------------------------------------------------------------------------
elif nav_option == "📑 Downloadable Reports":
    st.markdown('<div class="main-header">📑 Formal Audit & Investigation Reports</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Export structured anomaly records and generate formal printable land inspection reports</div>', unsafe_allow_html=True)
    
    alerts_df = get_all_alerts(DEFAULT_DB_PATH)
    summary_metrics = st.session_state.get("last_scan_metrics", {})
    
    rep_col1, rep_col2 = st.columns(2)
    
    with rep_col1:
        with st.container(border=True):
            st.markdown('<div class="section-title">📥 Export Alerts Ledger (CSV)</div>', unsafe_allow_html=True)
            st.write("Tabular export of all flagged alerts, severity scores, and triage notes.")
            csv_data = export_alerts_to_csv(alerts_df)
            st.download_button(
                label="Download Alerts Ledger (CSV)",
                data=csv_data,
                file_name=f"jomiguard_alerts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
    with rep_col2:
        with st.container(border=True):
            st.markdown('<div class="section-title">📄 Export Investigation Report (Markdown)</div>', unsafe_allow_html=True)
            st.write("Comprehensive formal inspection report including executive summary, case dossiers, and officer sign-off.")
            md_report = generate_markdown_audit_report(alerts_df, summary_metrics)
            st.download_button(
                label="Download Formal Report (.md)",
                data=md_report,
                file_name=f"jomiguard_investigation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                use_container_width=True,
                type="primary"
            )
        
    st.markdown("")
    st.markdown('<div class="section-title">👁️ Report Preview</div>', unsafe_allow_html=True)
    st.markdown(md_report)
