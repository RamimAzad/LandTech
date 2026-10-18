"""
JomiGuard — Land Fraud & Double-Selling Alert System
Institutional RegTech & Land Title Verification Platform
Primary Language: Bengali (বাংলা), Secondary Language: English
Modeled with KrishiBondhu-inspired design aesthetics and Institutional RegTech precision.
"""

import html
import json
from datetime import datetime
import streamlit as st
import streamlit.components.v1 as components
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
from core.i18n import t, to_bn_digits, fmt_num
from core.theme import get_theme_css


# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="JomiGuard — জমিগার্ড",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if "lang" not in st.session_state:
    st.session_state["lang"] = "bn"  # Primary language is Bangla

if "view_mode" not in st.session_state:
    st.session_state["view_mode"] = "landing"  # Default to welcoming front page

if "user_theme_mode" not in st.session_state:
    st.session_state["user_theme_mode"] = "Auto (System)"

if "just_injected" not in st.session_state:
    st.session_state["just_injected"] = False

if "active_nav_app" not in st.session_state:
    st.session_state["active_nav_app"] = "dashboard"

# Deep-linking query parameter handling
if "view" in st.query_params:
    st.session_state["view_mode"] = st.query_params["view"]
if "tab" in st.query_params:
    raw_tab = str(st.query_params["tab"]).strip().lower()
    tab_map = {
        "dash": "dashboard", "dashboard": "dashboard",
        "alert": "alerts", "alerts": "alerts",
        "plot": "plots", "plots": "plots",
        "demo": "sandbox", "sandbox": "sandbox",
        "audit": "reports", "report": "reports", "reports": "reports"
    }
    st.session_state["active_nav_app"] = tab_map.get(raw_tab, raw_tab)
if "lang" in st.query_params:
    st.session_state["lang"] = st.query_params["lang"]


# Initialize Database & Engine
init_db_if_needed(DEFAULT_DB_PATH)
if "last_scan_metrics" not in st.session_state:
    alerts, summary = run_detection(DEFAULT_DB_PATH)
    st.session_state["last_scan_metrics"] = summary


# Inject Theme CSS
_active_theme = st.session_state.get("user_theme_mode", "Auto (System)")
st.markdown(get_theme_css(_active_theme), unsafe_allow_html=True)

lang = st.session_state["lang"]


# -----------------------------------------------------------------------------
# FIELD FORMATTING & LOCALIZATION HELPERS
# -----------------------------------------------------------------------------
_FIELD_LABELS_BN = {
    "deed_no": "দলিল নম্বর",
    "plot_id": "দাগ আইডি (Plot ID)",
    "registration_date": "রেজিস্ট্রেশনের তারিখ",
    "seller_nid": "বিক্রেতার এনআইডি",
    "seller_name": "বিক্রেতার নাম",
    "buyer_nid": "ক্রেতার এনআইডি",
    "buyer_name": "ক্রেতার নাম",
    "transferred_area_decimals": "হস্তান্তরিত আয়তন (শতাংশ)",
    "deed_value_bdt": "দলিল মূল্য (টাকা)",
    "sub_registry_office": "সাব-রেজিস্ট্রি অফিস",
    "status": "বর্তমান অবস্থা",
    "created_at": "রেকর্ডের সময়",
    "name": "নাম",
    "nid": "এনআইডি (NID)",
    "mutation_case_no": "নামজারি কেস নম্বর",
    "mutation_date": "নামজারির তারিখ",
    "applicant_name": "আবেদনকারীর নাম",
    "applicant_nid": "আবেদনকারীর এনআইডি",
    "mutated_area_decimals": "নামজারিকৃত আয়তন (শতাংশ)",
    "new_khatian_no": "নতুন খতিয়ান নম্বর",
    "ac_land_office": "এসি ল্যান্ড অফিস",
    "approved_by": "অনুমোদনকারী কর্মকর্তা",
    "remarks": "মন্তব্য",
    "deed_1_no": "প্রথম দলিল নম্বর",
    "deed_1_date": "প্রথম দলিলের তারিখ",
    "deed_1_buyer": "প্রথম দলিলের ক্রেতা",
    "deed_1_area_decimals": "প্রথম দলিলের আয়তন",
    "deed_2_no": "দ্বিতীয় দলিল নম্বর",
    "deed_2_date": "দ্বিতীয় দলিলের তারিখ",
    "deed_2_buyer": "দ্বিতীয় দলিলের ক্রেতা",
    "deed_2_area_decimals": "দ্বিতীয় দলিলের আয়তন",
    "conflict_type": "অসঙ্গতির ধরন",
    "days_between_sales": "বিক্রয়ের মধ্যবর্তী দিন",
    "excess_area_decimals": "অতিরিক্ত জমি (শতাংশ)",
    "discrepancy_decimals": "আয়তন গরমিল (শতাংশ)",
    "available_balance_decimals": "অবশিষ্ট স্বত্ব (শতাংশ)",
}

_FIELD_LABELS_EN = {
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
    "deed_1_no": "First Deed No",
    "deed_1_date": "First Deed Date",
    "deed_1_buyer": "First Deed Buyer",
    "deed_1_area_decimals": "First Deed Area (dec)",
    "deed_2_no": "Second Deed No",
    "deed_2_date": "Second Deed Date",
    "deed_2_buyer": "Second Deed Buyer",
    "deed_2_area_decimals": "Second Deed Area (dec)",
    "conflict_type": "Conflict Type",
    "days_between_sales": "Days Between Sales",
    "excess_area_decimals": "Excess Area (dec)",
    "discrepancy_decimals": "Discrepancy (dec)",
    "available_balance_decimals": "Available Balance (dec)",
}


def pretty_field(key: str, cur_lang: str = "bn") -> str:
    """Return localized field label."""
    if cur_lang == "bn":
        return _FIELD_LABELS_BN.get(key, str(key).replace("_", " ").title())
    return _FIELD_LABELS_EN.get(key, str(key).replace("_", " ").title())


def pretty_value(value, key: str = "", cur_lang: str = "bn") -> str:
    """Format value with JetBrains Mono for identifiers and decimals."""
    if value is None or value == "":
        return '<span style="color:var(--jg-muted); font-style:italic;">—</span>'
    
    val_str = str(value)
    # Check if this is an identifier field (plot_id, deed_no, mutation_case_no, NID)
    is_id_field = any(k in key.lower() for k in ["plot_id", "deed", "mutation", "nid", "khatian", "dag"])
    is_num_field = isinstance(value, (int, float)) or any(k in key.lower() for k in ["area", "decimal", "value", "balance", "excess", "days"])
    
    if is_id_field:
        return f'<span class="mono-id">{html.escape(val_str)}</span>'
    
    if isinstance(value, float):
        formatted = f"{value:,.2f}"
        if cur_lang == "bn":
            formatted = to_bn_digits(formatted)
        return f'<span class="mono-id">{formatted}</span>'
    
    if isinstance(value, int):
        formatted = f"{value:,}"
        if cur_lang == "bn":
            formatted = to_bn_digits(formatted)
        return f'<span class="mono-id">{formatted}</span>'
        
    return html.escape(val_str)


# -----------------------------------------------------------------------------
# GOVERNANCE NOTICE COMPONENT (Strict Non-Accusatory Wording)
# -----------------------------------------------------------------------------
def render_governance_notice(cur_lang: str = "bn"):
    """Render mandatory non-accusatory institutional notice in the active language."""
    notice_text = t("governance_notice", cur_lang)
    st.markdown(f"""
    <div class="governance-shield bn-text">
        <strong>{notice_text}</strong>
    </div>
    """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# MICRO-ANIMATION 2: PLOT AREA OVERFLOW CAPACITY BAR
# -----------------------------------------------------------------------------
def render_plot_capacity_bar(total_area: float, transferred_area: float, cur_lang: str = "bn"):
    """
    Render horizontal capacity bar representing total_area_decimals.
    Smoothly animates its fill width (transition: width 500ms ease-out).
    If cumulative sales <= 100%, Emerald (#1B6B50).
    If > 100%, overflow segment extends in hatched Crimson (#DC2626) with label:
    '+4.50 Decimals Over Plot Capacity'.
    """
    total = float(total_area) if total_area > 0 else 1.0
    transferred = float(transferred_area)
    ratio = (transferred / total) * 100.0
    
    is_overflow = transferred > total + 0.01
    excess = max(0.0, transferred - total)
    
    normal_pct = min(100.0, ratio)
    overflow_pct = min(100.0, ((excess / total) * 100.0)) if is_overflow else 0.0

    total_str = fmt_num(total, cur_lang)
    transferred_str = fmt_num(transferred, cur_lang)
    ratio_str = fmt_num(ratio, cur_lang, decimals=1)
    excess_str = fmt_num(excess, cur_lang, decimals=2)

    title_text = t("capacity_overflow_title", cur_lang)
    
    if is_overflow:
        status_banner = f"""
        <div style="margin-top:10px; padding:10px 14px; background:var(--jg-alert-high-bg); border:1px solid var(--jg-alert-high-border); border-radius:8px; color:var(--jg-alert-high-text); font-weight:750; font-size:0.92rem; display:flex; align-items:center; gap:8px;">
            <span style="font-size:1.15rem;">🚨</span>
            <span>+{excess_str} {("শতাংশ দাগের ধারণক্ষমতার অতিরিক্ত বিক্রয় হয়েছে!" if cur_lang == "bn" else f"Decimals Over Plot Capacity ({ratio_str}% of surveyed size)")}</span>
        </div>
        """
    else:
        status_banner = f"""
        <div style="margin-top:8px; font-size:0.86rem; color:var(--jg-alert-ok-text); font-weight:650;">
            ✅ {("মোট বিক্রিত:" if cur_lang == "bn" else "Transferred:")} {transferred_str} / {total_str} {("শতাংশ" if cur_lang == "bn" else "decimals")} ({ratio_str}%) — {("দাগের বৈধ ধারণক্ষমতার মধ্যে রয়েছে" if cur_lang == "bn" else "Within legal plot capacity")}
        </div>
        """

    st.markdown(f"""
    <div class="capacity-bar-wrapper">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <span style="font-weight:750; font-size:0.92rem; color:var(--jg-ink);">{title_text}</span>
            <span class="mono-id">{transferred_str} / {total_str} {("শতাংশ" if cur_lang == "bn" else "dec")}</span>
        </div>
        <div class="capacity-track">
            <div class="capacity-fill-normal" style="width: {normal_pct:.1f}%;"></div>
            {f'<div class="capacity-fill-overflow" style="width: {overflow_pct:.1f}%;"></div>' if is_overflow else ''}
        </div>
        {status_banner}
    </div>
    """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# SAFE HTML RENDERER (Eliminates Markdown 4-space Code Block Formatting Traps)
# -----------------------------------------------------------------------------
def render_html_block(html_content: str):
    """
    Renders pure HTML safely without Markdown indentation quirks.
    Strips leading spaces from every line so CommonMark can never interpret
    table markup as an indented <pre><code> block.
    """
    lines = [line.strip() for line in html_content.strip().splitlines() if line.strip()]
    st.markdown("\n".join(lines), unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# SIDE-BY-SIDE EVIDENCE DIFF TABLE (Institutional 4-Column Table with ≠ Badge)
# -----------------------------------------------------------------------------
def render_evidence_diff_table(
    record_a: dict,
    record_b: dict,
    title_a: str,
    title_b: str,
    conflict_reason: str,
    cur_lang: str = "bn"
):
    """
    Renders an institutional bilateral evidence diff table comparing Record A and Record B side by side.
    Matching fields sit quietly in neutral styling, while conflicting fields are highlighted with
    a crimson conflict badge (≠) and highlighted monospace values.
    """
    record_a = record_a or {}
    record_b = record_b or {}

    keys_a = list(record_a.keys())
    keys_b = list(record_b.keys())
    all_keys = list(dict.fromkeys(keys_a + keys_b))

    header_field = "আইনি ক্ষেত্র / রেকর্ড প্যারামিটার" if cur_lang == "bn" else "Legal Field / Parameter"
    header_diff = "তুলনা" if cur_lang == "bn" else "Diff"
    diff_title = t("evidence_diff_title", cur_lang)

    table_rows = []
    for key in all_keys:
        in_a = key in record_a
        in_b = key in record_b
        val_a = record_a.get(key)
        val_b = record_b.get(key)

        is_diff = in_a and in_b and str(val_a).strip() != str(val_b).strip()
        field_lbl = pretty_field(key, cur_lang)

        val_a_fmt = pretty_value(val_a, key, cur_lang) if in_a else '<span class="diff-empty">—</span>'
        val_b_fmt = pretty_value(val_b, key, cur_lang) if in_b else '<span class="diff-empty">—</span>'

        if is_diff:
            row_html = (
                f'<tr class="diff-row-conflict">'
                f'<td class="diff-cell-field diff-conflict-text">'
                f'<span class="diff-conflict-dot">!</span>{html.escape(field_lbl)}'
                f'</td>'
                f'<td class="diff-conflict-val"><span class="trigger-field-highlight">{val_a_fmt}</span></td>'
                f'<td class="diff-cell-badge"><span class="diff-neq-pill" title="Mismatched Parameter">≠</span></td>'
                f'<td class="diff-conflict-val"><span class="trigger-field-highlight">{val_b_fmt}</span></td>'
                f'</tr>'
            )
        else:
            row_html = (
                f'<tr class="diff-row-match">'
                f'<td class="diff-cell-field">{html.escape(field_lbl)}</td>'
                f'<td>{val_a_fmt}</td>'
                f'<td class="diff-cell-badge"><span class="diff-match-pill" title="Matching Record">=</span></td>'
                f'<td>{val_b_fmt}</td>'
                f'</tr>'
            )
        table_rows.append(row_html)

    table_body = "\n".join(table_rows)

    wrapper_html = f"""
<div class="diff-table-wrapper">
    <div class="diff-card-header">
        <div class="diff-header-title">⚖️ {diff_title}</div>
        <div class="diff-conflict-reason-badge">⚠️ {html.escape(conflict_reason)}</div>
    </div>
    <table class="diff-table">
        <thead>
            <tr>
                <th style="width:26%;">{header_field}</th>
                <th style="width:34%;">📁 {html.escape(title_a)}</th>
                <th style="width:6%; text-align:center;">{header_diff}</th>
                <th style="width:34%;">📑 {html.escape(title_b)}</th>
            </tr>
        </thead>
        <tbody>
            {table_body}
        </tbody>
    </table>
</div>
"""
    render_html_block(wrapper_html)


# Backwards compatibility alias
render_evidence_diff_card = render_evidence_diff_table


# -----------------------------------------------------------------------------
# SINGLE EVIDENCE DOSSIER TABLE (For Non-Pairwise Anomaly Payloads)
# -----------------------------------------------------------------------------
def render_single_evidence_table(
    evidence_data: dict,
    cur_lang: str = "bn",
    title: str = ""
):
    """
    Renders non-pairwise or single record evidence data in an institutional table.
    Eliminates raw JSON dumps and formats all fields with monospace identifiers.
    """
    if not evidence_data:
        return

    default_title = "নথি ও পরিমাপ সারসংক্ষেপ" if cur_lang == "bn" else "Record Evidence Dossier"
    display_title = title or default_title
    header_param = "প্যারামিটার / ক্ষেত্র" if cur_lang == "bn" else "Parameter / Field"
    header_val = "রেকর্ডীয় তথ্য / মান" if cur_lang == "bn" else "Recorded Value / Status"

    table_rows = []

    # Flatten nested dictionaries if any
    flattened_items = []
    for k, v in evidence_data.items():
        if isinstance(v, dict):
            flattened_items.append((f"--- {pretty_field(k, cur_lang)} ---", None))
            for sub_k, sub_v in v.items():
                flattened_items.append((sub_k, sub_v))
        elif isinstance(v, list):
            val_strs = [pretty_value(item, k, cur_lang) for item in v]
            flattened_items.append((k, ", ".join(val_strs)))
        else:
            flattened_items.append((k, v))

    for key, val in flattened_items:
        if val is None:
            row_html = (
                f'<tr style="background:var(--jg-tbl-head-bg);">'
                f'<td colspan="2" style="font-weight:750; font-size:0.84rem; color:var(--jg-brand); text-transform:uppercase; padding:6px 12px;">'
                f'{html.escape(key)}'
                f'</td>'
                f'</tr>'
            )
        else:
            field_lbl = pretty_field(key, cur_lang)
            val_fmt = pretty_value(val, key, cur_lang)
            
            is_anomaly = any(x in key.lower() for x in ["discrepancy", "excess", "variance", "not found", "inversion", "conflict"]) or ("not found" in str(val).lower())
            
            if is_anomaly:
                row_html = (
                    f'<tr class="diff-row-conflict">'
                    f'<td class="diff-cell-field diff-conflict-text">'
                    f'<span class="diff-conflict-dot">!</span>{html.escape(field_lbl)}'
                    f'</td>'
                    f'<td class="diff-conflict-val"><span class="trigger-field-highlight">{val_fmt}</span></td>'
                    f'</tr>'
                )
            else:
                row_html = (
                    f'<tr class="diff-row-match">'
                    f'<td class="diff-cell-field">{html.escape(field_lbl)}</td>'
                    f'<td>{val_fmt}</td>'
                    f'</tr>'
                )
        table_rows.append(row_html)

    table_body = "\n".join(table_rows)

    wrapper_html = f"""
<div class="diff-table-wrapper">
    <div class="diff-card-header">
        <div class="diff-header-title">📋 {html.escape(display_title)}</div>
        <div style="font-size:0.82rem; color:var(--jg-muted); font-weight:600;">{'রেকর্ডীয় প্রমাণপত্র' if cur_lang == 'bn' else 'Documentary Evidence'}</div>
    </div>
    <table class="diff-table">
        <thead>
            <tr>
                <th style="width:35%;">{header_param}</th>
                <th style="width:65%;">{header_val}</th>
            </tr>
        </thead>
        <tbody>
            {table_body}
        </tbody>
    </table>
</div>
"""
    render_html_block(wrapper_html)


# -----------------------------------------------------------------------------
# TOP FLOATING NAVBAR (Clean 5-Column Institutional Layout)
# -----------------------------------------------------------------------------
def render_navbar(cur_lang: str = "bn", in_app: bool = False):
    """
    Renders top floating frosted glass navbar with:
    Brand logo, language toggle, theme toggle, Home/Demo jump, and Get Started CTA.
    Screen recorder is fully removed.
    """
    brand_name = t("brand_name", cur_lang)
    
    # Top navbar container using Streamlit columns
    with st.container():
        nav_c1, nav_c2, nav_c3, nav_c4, nav_c5 = st.columns([3.4, 1.4, 1.4, 1.5, 2.3])
        
        with nav_c1:
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:8px; padding-top:4px;">
                <span style="font-size:1.5rem;">🛡️</span>
                <span style="font-size:1.35rem; font-weight:850; color:var(--jg-brand); letter-spacing:-0.02em;">{brand_name}</span>
            </div>
            """, unsafe_allow_html=True)

        with nav_c2:
            # Language Switcher
            current_lang_label = "🌐 বাং / EN" if cur_lang == "bn" else "🌐 EN / বাং"
            if st.button(current_lang_label, key="nav_btn_lang", use_container_width=True):
                st.session_state["lang"] = "en" if cur_lang == "bn" else "bn"
                st.rerun()

        with nav_c3:
            # Theme Switcher
            cur_th = st.session_state.get("user_theme_mode", "Auto (System)")
            theme_icon = "🌓" if cur_th == "Auto (System)" else ("☀️" if cur_th == "Light" else "🌙")
            next_th = "Light" if cur_th == "Dark" else ("Dark" if cur_th == "Light" else "Dark")
            if st.button(f"{theme_icon} থিম" if cur_lang == "bn" else f"{theme_icon} Theme", key="nav_btn_theme", use_container_width=True):
                st.session_state["user_theme_mode"] = next_th
                st.rerun()

        with nav_c4:
            # Home / Reset view button
            if in_app:
                if st.button("🏠 হোম" if cur_lang == "bn" else "🏠 Home", key="nav_btn_home", use_container_width=True):
                    st.session_state["view_mode"] = "landing"
                    st.rerun()
            else:
                if st.button(t("nav_demo", cur_lang), key="nav_btn_demo_jump", use_container_width=True):
                    st.session_state["view_mode"] = "app"
                    st.session_state["active_nav_app"] = "sandbox"
                    st.rerun()

        with nav_c5:
            # Primary CTA Button: Get Started / Enter System
            if in_app:
                st.markdown(f"""
                <div style="background:var(--jg-accent-soft); border:1px solid var(--jg-accent); border-radius:10px; padding:7px 12px; text-align:center; color:var(--jg-accent); font-weight:750; font-size:0.86rem;">
                    ● {('সিস্টেম লাইভ' if cur_lang == 'bn' else 'System Active')}
                </div>
                """, unsafe_allow_html=True)
            else:
                if st.button(t("nav_get_started", cur_lang), key="nav_btn_get_started_top", type="primary", use_container_width=True):
                    st.session_state["view_mode"] = "app"
                    st.session_state["active_nav_app"] = "dashboard"
                    st.rerun()


# -----------------------------------------------------------------------------
# LANDING PAGE VIEW (Welcoming front page like KrishiBondhu)
# -----------------------------------------------------------------------------
def render_landing_page(cur_lang: str = "bn"):
    """
    Renders welcoming front page with:
    - KrishiBondhu styled top navbar
    - Hero section with glowing badge, value proposition, dual CTAs, trust badges
    - Live stat ticker
    - Non-accusatory Governance Notice
    - The Problem section (6 cards)
    - The Solution & Core Modules section (6 rules)
    - How It Works (4-step workflow)
    - Institutional Roadmap (4 phases)
    - FAQ accordion
    - Launch CTA banner
    - Institutional footer
    """
    render_navbar(cur_lang=cur_lang, in_app=False)

    # 1. HERO SECTION
    hero_badge = t("hero_badge", cur_lang)
    hero_title = t("hero_title", cur_lang)
    hero_subtitle = t("hero_subtitle", cur_lang)

    st.markdown(f"""
    <div class="hero-container">
        <div class="hero-badge">{hero_badge}</div>
        <div class="hero-title">{hero_title}</div>
        <div class="hero-subtitle bn-text">{hero_subtitle}</div>
    </div>
    """, unsafe_allow_html=True)

    # Hero Dual Call-to-Action Buttons
    h_btn_col1, h_btn_col2, h_btn_col3, h_btn_col4 = st.columns([1.5, 3.5, 3.5, 1.5])
    with h_btn_col2:
        if st.button(t("hero_cta_primary", cur_lang), key="hero_cta_main", type="primary", use_container_width=True):
            st.session_state["view_mode"] = "app"
            st.session_state["active_nav_app"] = "dashboard"
            st.rerun()
    with h_btn_col3:
        if st.button(t("hero_cta_secondary", cur_lang), key="hero_cta_demo", use_container_width=True):
            st.session_state["view_mode"] = "app"
            st.session_state["active_nav_app"] = "sandbox"
            st.rerun()

    # Hero Trust Strip
    st.markdown(f"""
    <div class="hero-trust-strip">
        <span>{t("hero_trust_badge_1", cur_lang)}</span>
        <span>•</span>
        <span>{t("hero_trust_badge_2", cur_lang)}</span>
        <span>•</span>
        <span>{t("hero_trust_badge_3", cur_lang)}</span>
    </div>
    """, unsafe_allow_html=True)

    # 2. LIVE METRICS TICKER
    plots_df = get_all_plots(DEFAULT_DB_PATH)
    deeds_df = get_all_deeds(DEFAULT_DB_PATH)
    mutations_df = get_all_mutations(DEFAULT_DB_PATH)
    alerts_df = get_all_alerts(DEFAULT_DB_PATH)

    st.markdown(f"""
    <div class="stat-ticker-grid">
        <div class="stat-card">
            <div class="stat-val">{fmt_num(len(plots_df), cur_lang)}</div>
            <div class="stat-lbl">{t("stat_screened_plots", cur_lang)}</div>
        </div>
        <div class="stat-card">
            <div class="stat-val">{fmt_num(len(deeds_df), cur_lang)}</div>
            <div class="stat-lbl">{t("stat_registered_deeds", cur_lang)}</div>
        </div>
        <div class="stat-card">
            <div class="stat-val">{fmt_num(len(mutations_df), cur_lang)}</div>
            <div class="stat-lbl">{t("stat_verified_mutations", cur_lang)}</div>
        </div>
        <div class="stat-card">
            <div class="stat-val">{t("stat_detection_speed_val", cur_lang)}</div>
            <div class="stat-lbl">{t("stat_detection_speed", cur_lang)}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3. MANDATORY GOVERNANCE SHIELD
    render_governance_notice(cur_lang)

    # 4. THE PROBLEM SECTION
    st.markdown(f"""
    <div style="margin-top:2.5rem;">
        <div class="section-badge-center">
            <span class="section-badge">{t("problem_section_badge", cur_lang)}</span>
        </div>
        <div class="section-heading-center">{t("problem_section_title", cur_lang)}</div>
        <div class="section-subheading-center bn-text">{t("problem_section_subtitle", cur_lang)}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card-grid-3">
        <div class="jg-card">
            <div style="font-size:1.8rem;">⚠️</div>
            <div class="jg-card-title">{t("prob_1_title", cur_lang)}</div>
            <div class="jg-card-desc bn-text">{t("prob_1_desc", cur_lang)}</div>
        </div>
        <div class="jg-card">
            <div style="font-size:1.8rem;">📈</div>
            <div class="jg-card-title">{t("prob_2_title", cur_lang)}</div>
            <div class="jg-card-desc bn-text">{t("prob_2_desc", cur_lang)}</div>
        </div>
        <div class="jg-card">
            <div style="font-size:1.8rem;">🎭</div>
            <div class="jg-card-title">{t("prob_3_title", cur_lang)}</div>
            <div class="jg-card-desc bn-text">{t("prob_3_desc", cur_lang)}</div>
        </div>
        <div class="jg-card">
            <div style="font-size:1.8rem;">⏳</div>
            <div class="jg-card-title">{t("prob_4_title", cur_lang)}</div>
            <div class="jg-card-desc bn-text">{t("prob_4_desc", cur_lang)}</div>
        </div>
        <div class="jg-card">
            <div style="font-size:1.8rem;">👻</div>
            <div class="jg-card-title">{t("prob_5_title", cur_lang)}</div>
            <div class="jg-card-desc bn-text">{t("prob_5_desc", cur_lang)}</div>
        </div>
        <div class="jg-card">
            <div style="font-size:1.8rem;">⛓️</div>
            <div class="jg-card-title">{t("prob_6_title", cur_lang)}</div>
            <div class="jg-card-desc bn-text">{t("prob_6_desc", cur_lang)}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 5. CORE MODULES / RULES SECTION
    st.markdown(f"""
    <div style="margin-top:2.5rem;">
        <div class="section-badge-center">
            <span class="section-badge">{t("modules_section_badge", cur_lang)}</span>
        </div>
        <div class="section-heading-center">{t("modules_section_title", cur_lang)}</div>
        <div class="section-subheading-center bn-text">{t("modules_section_subtitle", cur_lang)}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card-grid-3">
        <div class="jg-card">
            <div class="badge-critical" style="margin-bottom:8px;">CRITICAL R1</div>
            <div class="jg-card-title">{t("rule_r1_title", cur_lang)}</div>
            <div class="jg-card-desc bn-text">{t("rule_r1_desc", cur_lang)}</div>
        </div>
        <div class="jg-card">
            <div class="badge-critical" style="margin-bottom:8px;">CRITICAL R2</div>
            <div class="jg-card-title">{t("rule_r2_title", cur_lang)}</div>
            <div class="jg-card-desc bn-text">{t("rule_r2_desc", cur_lang)}</div>
        </div>
        <div class="jg-card">
            <div class="badge-high" style="margin-bottom:8px;">HIGH M1</div>
            <div class="jg-card-title">{t("rule_m1_title", cur_lang)}</div>
            <div class="jg-card-desc bn-text">{t("rule_m1_desc", cur_lang)}</div>
        </div>
        <div class="jg-card">
            <div class="badge-high" style="margin-bottom:8px;">HIGH M2</div>
            <div class="jg-card-title">{t("rule_m2_title", cur_lang)}</div>
            <div class="jg-card-desc bn-text">{t("rule_m2_desc", cur_lang)}</div>
        </div>
        <div class="jg-card">
            <div class="badge-medium" style="margin-bottom:8px;">MEDIUM M3</div>
            <div class="jg-card-title">{t("rule_m3_title", cur_lang)}</div>
            <div class="jg-card-desc bn-text">{t("rule_m3_desc", cur_lang)}</div>
        </div>
        <div class="jg-card">
            <div class="badge-medium" style="margin-bottom:8px;">MEDIUM M4</div>
            <div class="jg-card-title">{t("rule_m4_title", cur_lang)}</div>
            <div class="jg-card-desc bn-text">{t("rule_m4_desc", cur_lang)}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 6. HOW IT WORKS WORKFLOW
    st.markdown(f"""
    <div style="margin-top:2.5rem;">
        <div class="section-badge-center">
            <span class="section-badge">{t("hiw_section_badge", cur_lang)}</span>
        </div>
        <div class="section-heading-center">{t("hiw_section_title", cur_lang)}</div>
        <div class="section-subheading-center bn-text">{t("hiw_section_subtitle", cur_lang)}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card-grid-2">
        <div class="jg-card" style="border-left:5px solid var(--jg-accent);">
            <div class="mono-id" style="font-size:0.9rem; margin-bottom:6px;">STEP 01</div>
            <div class="jg-card-title">{t("step_1_title", cur_lang)}</div>
            <div class="jg-card-desc bn-text">{t("step_1_desc", cur_lang)}</div>
        </div>
        <div class="jg-card" style="border-left:5px solid var(--jg-accent);">
            <div class="mono-id" style="font-size:0.9rem; margin-bottom:6px;">STEP 02</div>
            <div class="jg-card-title">{t("step_2_title", cur_lang)}</div>
            <div class="jg-card-desc bn-text">{t("step_2_desc", cur_lang)}</div>
        </div>
        <div class="jg-card" style="border-left:5px solid var(--jg-accent);">
            <div class="mono-id" style="font-size:0.9rem; margin-bottom:6px;">STEP 03</div>
            <div class="jg-card-title">{t("step_3_title", cur_lang)}</div>
            <div class="jg-card-desc bn-text">{t("step_3_desc", cur_lang)}</div>
        </div>
        <div class="jg-card" style="border-left:5px solid var(--jg-accent);">
            <div class="mono-id" style="font-size:0.9rem; margin-bottom:6px;">STEP 04</div>
            <div class="jg-card-title">{t("step_4_title", cur_lang)}</div>
            <div class="jg-card-desc bn-text">{t("step_4_desc", cur_lang)}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 7. INSTITUTIONAL ROADMAP
    st.markdown(f"""
    <div style="margin-top:2.5rem;">
        <div class="section-badge-center">
            <span class="section-badge">{t("roadmap_section_badge", cur_lang)}</span>
        </div>
        <div class="section-heading-center">{t("roadmap_section_title", cur_lang)}</div>
        <div class="section-subheading-center bn-text">{t("roadmap_section_subtitle", cur_lang)}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card-grid-2">
        <div class="jg-card">
            <span class="badge-critical" style="background:var(--jg-alert-ok-bg); color:var(--jg-alert-ok-text); border-color:var(--jg-alert-ok-border);">
                {t("phase_1_badge", cur_lang)}
            </span>
            <div class="jg-card-title">{t("phase_1_title", cur_lang)}</div>
            <div class="jg-card-desc bn-text">{t("phase_1_desc", cur_lang)}</div>
        </div>
        <div class="jg-card">
            <span class="badge-high">{t("phase_2_badge", cur_lang)}</span>
            <div class="jg-card-title">{t("phase_2_title", cur_lang)}</div>
            <div class="jg-card-desc bn-text">{t("phase_2_desc", cur_lang)}</div>
        </div>
        <div class="jg-card">
            <span class="badge-medium">{t("phase_3_badge", cur_lang)}</span>
            <div class="jg-card-title">{t("phase_3_title", cur_lang)}</div>
            <div class="jg-card-desc bn-text">{t("phase_3_desc", cur_lang)}</div>
        </div>
        <div class="jg-card">
            <span class="badge-low">{t("phase_4_badge", cur_lang)}</span>
            <div class="jg-card-title">{t("phase_4_title", cur_lang)}</div>
            <div class="jg-card-desc bn-text">{t("phase_4_desc", cur_lang)}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 8. FREQUENTLY ASKED QUESTIONS (FAQ)
    st.markdown(f"""
    <div style="margin-top:2.5rem;">
        <div class="section-badge-center">
            <span class="section-badge">{t("faq_section_badge", cur_lang)}</span>
        </div>
        <div class="section-heading-center">{t("faq_section_title", cur_lang)}</div>
        <div class="section-subheading-center bn-text">{t("faq_section_subtitle", cur_lang)}</div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander(f"❓ {t('faq_q1', cur_lang)}", expanded=True):
        st.markdown(f"<div class='bn-text'>{t('faq_a1', cur_lang)}</div>", unsafe_allow_html=True)
    with st.expander(f"❓ {t('faq_q2', cur_lang)}"):
        st.markdown(f"<div class='bn-text'>{t('faq_a2', cur_lang)}</div>", unsafe_allow_html=True)
    with st.expander(f"❓ {t('faq_q3', cur_lang)}"):
        st.markdown(f"<div class='bn-text'>{t('faq_a3', cur_lang)}</div>", unsafe_allow_html=True)
    with st.expander(f"❓ {t('faq_q4', cur_lang)}"):
        st.markdown(f"<div class='bn-text'>{t('faq_a4', cur_lang)}</div>", unsafe_allow_html=True)
    with st.expander(f"❓ {t('faq_q5', cur_lang)}"):
        st.markdown(f"<div class='bn-text'>{t('faq_a5', cur_lang)}</div>", unsafe_allow_html=True)

    # 9. CTA BANNER
    st.markdown(f"""
    <div style="background:linear-gradient(135deg, var(--jg-brand) 0%, #165640 100%); border-radius:16px; padding:2.5rem 1.5rem; text-align:center; color:#FFFFFF; margin:3.5rem 0 2rem; box-shadow:var(--jg-shadow-lg);">
        <h2 style="color:#FFFFFF !important; font-size:2rem; font-weight:850; margin-bottom:0.6rem;">{t("cta_banner_title", cur_lang)}</h2>
        <p class="bn-text" style="color:rgba(255,255,255,0.9); font-size:1.05rem; max-width:650px; margin:0 auto 1.6rem;">{t("cta_banner_subtitle", cur_lang)}</p>
    </div>
    """, unsafe_allow_html=True)

    c_col1, c_col2, c_col3 = st.columns([3, 4, 3])
    with c_col2:
        if st.button(t("cta_banner_btn", cur_lang), key="cta_banner_btn_action", type="primary", use_container_width=True):
            st.session_state["view_mode"] = "app"
            st.session_state["active_nav_app"] = "dashboard"
            st.rerun()

    # 10. INSTITUTIONAL FOOTER
    st.markdown(f"""
    <div style="border-top:1px solid var(--jg-border); padding:2rem 0 1rem; margin-top:2.5rem; text-align:center; color:var(--jg-muted); font-size:0.86rem;">
        <p class="bn-text">{t("footer_credits", cur_lang)}</p>
    </div>
    """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# MAIN APP: VIEW 1 - DASHBOARD OVERVIEW
# -----------------------------------------------------------------------------
def render_dashboard_view(cur_lang: str = "bn"):
    st.markdown(f'<div class="main-header">{t("dash_title", cur_lang)}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header bn-text">{t("dash_sub", cur_lang)}</div>', unsafe_allow_html=True)
    
    render_governance_notice(cur_lang)

    plots_df = get_all_plots(DEFAULT_DB_PATH)
    deeds_df = get_all_deeds(DEFAULT_DB_PATH)
    mutations_df = get_all_mutations(DEFAULT_DB_PATH)
    alerts_df = get_all_alerts(DEFAULT_DB_PATH)

    critical_count = len(alerts_df[alerts_df["severity"] == "CRITICAL"]) if not alerts_df.empty else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{t("kpi_total_plots", cur_lang)}</div>
            <div class="kpi-value">{fmt_num(len(plots_df), cur_lang)}</div>
            <div class="kpi-foot">{t("kpi_total_plots_foot", cur_lang)}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{t("kpi_total_deeds", cur_lang)}</div>
            <div class="kpi-value">{fmt_num(len(deeds_df), cur_lang)}</div>
            <div class="kpi-foot">{t("kpi_total_deeds_foot", cur_lang)}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{t("kpi_total_mutations", cur_lang)}</div>
            <div class="kpi-value">{fmt_num(len(mutations_df), cur_lang)}</div>
            <div class="kpi-foot">{t("kpi_total_mutations_foot", cur_lang)}</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{t("kpi_flagged_alerts", cur_lang)}</div>
            <div class="kpi-value" style="color:#B91C1C;">{fmt_num(len(alerts_df), cur_lang)}</div>
            <div class="kpi-foot">{t("kpi_flagged_alerts_foot", cur_lang, crit=fmt_num(critical_count, cur_lang))}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # Visual Charts
    st.markdown(f'<div class="section-title">{t("dash_charts_title", cur_lang)}</div>', unsafe_allow_html=True)
    ch_col1, ch_col2 = st.columns(2)

    cur_theme = st.session_state.get("user_theme_mode", "Auto (System)")
    is_dark = (cur_theme == "Dark")
    chart_font_color = "#F8FAFC" if is_dark else "#1E293B"
    chart_grid_color = "rgba(255,255,255,0.12)" if is_dark else "rgba(148, 163, 184, 0.2)"

    with ch_col1:
        st.markdown(f"##### {t('chart_severity_title', cur_lang)}")
        if not alerts_df.empty:
            sev_counts = alerts_df["severity"].value_counts().reset_index()
            sev_counts.columns = ["Severity", "Count"]
            color_map = {
                "CRITICAL": "#B91C1C",
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
            fig_sev.update_traces(
                textposition='inside',
                textinfo='percent+label',
                textfont=dict(color="#FFFFFF", size=12, family="Plus Jakarta Sans, sans-serif")
            )
            fig_sev.update_layout(
                margin=dict(t=10, b=10, l=10, r=10),
                height=280,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                showlegend=True,
                font=dict(color=chart_font_color, family="Plus Jakarta Sans, sans-serif"),
                legend=dict(
                    font=dict(color=chart_font_color),
                    orientation="h",
                    yanchor="bottom",
                    y=-0.15,
                    xanchor="center",
                    x=0.5
                )
            )
            st.plotly_chart(fig_sev, use_container_width=True)
        else:
            st.info("No active inconsistencies detected.")

    with ch_col2:
        st.markdown(f"##### {t('chart_rules_title', cur_lang)}")
        if not alerts_df.empty:
            rule_counts = alerts_df["rule_name"].value_counts().reset_index()
            rule_counts.columns = ["Rule Name", "Incidents"]
            fig_rule = px.bar(
                rule_counts,
                x="Incidents",
                y="Rule Name",
                orientation="h",
                color="Incidents",
                color_continuous_scale=[[0, "#10B981" if is_dark else "#1B6B50"], [1, "#059669" if is_dark else "#0F3D2E"]],
            )
            fig_rule.update_layout(
                yaxis={'categoryorder': 'total ascending', 'tickfont': dict(color=chart_font_color)},
                xaxis={'tickfont': dict(color=chart_font_color), 'gridcolor': chart_grid_color},
                font=dict(color=chart_font_color, family="Plus Jakarta Sans, sans-serif"),
                margin=dict(t=10, b=10, l=10, r=10),
                height=280,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                coloraxis_showscale=False,
            )
            st.plotly_chart(fig_rule, use_container_width=True)
        else:
            st.info("No active inconsistencies detected.")

    st.markdown("")
    st.markdown(f'<div class="section-title">{t("dash_recent_alerts_title", cur_lang)}</div>', unsafe_allow_html=True)

    if not alerts_df.empty:
        display_df = alerts_df[[
            "alert_id", "severity", "plot_id", "rule_name", "title", "triage_status", "created_at"
        ]].copy()
        
        if cur_lang == "bn":
            dash_cols = {
                "alert_id": st.column_config.TextColumn("অ্যালার্ট আইডি"),
                "severity": st.column_config.TextColumn("ঝুঁকির মাত্রা (Severity)"),
                "plot_id": st.column_config.TextColumn("দাগ নম্বর (Plot)"),
                "rule_name": st.column_config.TextColumn("রুলের নাম"),
                "title": st.column_config.TextColumn("অসঙ্গতির সারসংক্ষেপ"),
                "triage_status": st.column_config.TextColumn("পর্যালোচনা স্থিতি"),
                "created_at": st.column_config.TextColumn("শনাক্তের সময়"),
            }
        else:
            dash_cols = {
                "alert_id": st.column_config.TextColumn("Alert ID"),
                "severity": st.column_config.TextColumn("Severity"),
                "plot_id": st.column_config.TextColumn("Plot ID"),
                "rule_name": st.column_config.TextColumn("Triggered Rule"),
                "title": st.column_config.TextColumn("Incident Summary"),
                "triage_status": st.column_config.TextColumn("Review Status"),
                "created_at": st.column_config.TextColumn("Timestamp"),
            }

        st.dataframe(
            display_df,
            use_container_width=True,
            column_config=dash_cols,
            hide_index=True
        )
    else:
        st.success("All screened records are consistent with verified chain of title.")


# -----------------------------------------------------------------------------
# MAIN APP: VIEW 2 - ALERTS & RISK INVESTIGATION
# -----------------------------------------------------------------------------
def render_alerts_view(cur_lang: str = "bn"):
    st.markdown(f'<div class="main-header">{t("alerts_view_title", cur_lang)}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header bn-text">{t("alerts_view_sub", cur_lang)}</div>', unsafe_allow_html=True)

    render_governance_notice(cur_lang)

    # Filter Controls
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        filter_sev = st.selectbox(t("filter_severity", cur_lang), ["ALL", "CRITICAL", "HIGH", "MEDIUM", "LOW"])
    with f_col2:
        filter_status = st.selectbox(
            t("filter_status", cur_lang),
            ["ALL", "Pending Review", "Under Investigation", "Marked Legitimate", "Confirmed Inconsistency"]
        )
    with f_col3:
        filter_plot = st.text_input(t("filter_plot", cur_lang), placeholder="e.g. P-201").strip().upper()

    alerts_df = get_all_alerts(
        DEFAULT_DB_PATH,
        severity=filter_sev,
        triage_status=filter_status
    )

    if filter_plot:
        alerts_df = alerts_df[alerts_df["plot_id"].str.contains(filter_plot, na=False)]

    st.markdown(f"<span class='record-count-text'>{('মোট চিহ্নিত রেকর্ড:' if cur_lang == 'bn' else 'Showing flagged records:')} <strong>{fmt_num(len(alerts_df), cur_lang)}</strong></span>", unsafe_allow_html=True)

    if alerts_df.empty:
        st.info(t("no_alerts_found", cur_lang))
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

            # Micro-animation check for injected record
            pulse_class = "conflict-injected" if (idx == 0 and st.session_state.get("just_injected", False)) else ""

            with st.expander(f"[{sev}] {title} — Plot {pid} ({status})", expanded=(idx < 2)):
                st.markdown(f"""
                <div class="{pulse_class}" style="padding:4px 0;">
                    <span class="{badge_class}">{sev}</span> &nbsp;
                    <strong>{('রুল:' if cur_lang == 'bn' else 'Rule:')}</strong> {r_name} &nbsp;|&nbsp;
                    <strong>{('অ্যালার্ট আইডি:' if cur_lang == 'bn' else 'Alert ID:')}</strong> <span class="mono-id">{aid}</span> &nbsp;|&nbsp;
                    <strong>{('দাগ আইডি:' if cur_lang == 'bn' else 'Plot ID:')}</strong> <span class="mono-id">{pid}</span>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"#### 💡 {('ব্যাখ্যামূলক কারণ' if cur_lang == 'bn' else 'Explainable Detection Rationale')}")
                st.markdown(f"<div class='bn-text'>{explanation}</div>", unsafe_allow_html=True)

                # Conflicting Records Side-by-Side with ≠ Badge
                st.markdown(f"#### ⚖️ {t('evidence_diff_title', cur_lang)}")
                if "first_deed" in evidence_data and "second_deed" in evidence_data:
                    render_evidence_diff_table(
                        record_a=evidence_data["first_deed"],
                        record_b=evidence_data["second_deed"],
                        title_a=f"{('পূর্ববর্তী নিবন্ধিত দলিল' if cur_lang == 'bn' else 'Prior Registered Deed')} ({evidence_data['first_deed'].get('deed_no', '')})",
                        title_b=f"{('পরবর্তী দ্বৈত বিক্রয় দলিল' if cur_lang == 'bn' else 'Subsequent Conflicting Deed')} ({evidence_data['second_deed'].get('deed_no', '')})",
                        conflict_reason=("দ্বৈত বিক্রয় বিরোধ (Double Sale Conflict)" if cur_lang == "bn" else "Conflicting Double-Sale by Same Seller"),
                        cur_lang=cur_lang
                    )
                elif "deed_record" in evidence_data and "mutation_record" in evidence_data:
                    render_evidence_diff_table(
                        record_a=evidence_data["deed_record"],
                        record_b=evidence_data["mutation_record"],
                        title_a=f"{('রেজিস্ট্রিকৃত সাব-কবলা দলিল' if cur_lang == 'bn' else 'Registered Sale Deed')} ({evidence_data['deed_record'].get('deed_no', '')})",
                        title_b=f"{('অনুমোদিত নামজারি খতিয়ান' if cur_lang == 'bn' else 'Revenue Mutation Record')} ({evidence_data['mutation_record'].get('mutation_case_no', '')})",
                        conflict_reason=("আয়তন গরমিল (Area Mismatch)" if cur_lang == "bn" else "Registration vs. Mutation Area Mismatch"),
                        cur_lang=cur_lang
                    )
                elif "deed_party" in evidence_data and "mutation_party" in evidence_data:
                    render_evidence_diff_table(
                        record_a=evidence_data["deed_party"],
                        record_b=evidence_data["mutation_party"],
                        title_a=f"{('দলিলের প্রকৃত ক্রেতা' if cur_lang == 'bn' else 'Registered Deed Buyer')}",
                        title_b=f"{('নামজারির আবেদনকারী' if cur_lang == 'bn' else 'Mutation Applicant')}",
                        conflict_reason=("এনআইডি ও নাম গরমিল (Identity Mismatch)" if cur_lang == "bn" else "Identity / NID Impostor Mismatch"),
                        cur_lang=cur_lang
                    )
                elif "deed_registration_date" in evidence_data and "mutation_date" in evidence_data:
                    render_evidence_diff_table(
                        record_a={"deed_registration_date": evidence_data["deed_registration_date"], "deed_no": trigger_data.get("deed_no", "—")},
                        record_b={"mutation_approval_date": evidence_data["mutation_date"], "mutation_case_no": trigger_data.get("mutation_case_no", "—"), "inversion_days": evidence_data.get("days_preceding_deed", "—")},
                        title_a=f"{('সাব-রেজিস্ট্রি দলিলের তারিখ' if cur_lang == 'bn' else 'Registered Deed Date')}",
                        title_b=f"{('অনুমোদিত নামজারির তারিখ' if cur_lang == 'bn' else 'Approved Mutation Date')}",
                        conflict_reason=("কালানুক্রমিক প্যারাডক্স (Chronological Paradox)" if cur_lang == "bn" else "Approval Date Precedes Deed Registration"),
                        cur_lang=cur_lang
                    )
                else:
                    render_single_evidence_table(
                        evidence_data=evidence_data if evidence_data else trigger_data,
                        cur_lang=cur_lang,
                        title=f"{('নথি ও পরিমাপ সারসংক্ষেপ' if cur_lang == 'bn' else 'Anomaly Evidence Dossier')}"
                    )

                st.markdown("---")

                # Institutional Triage Decision Workflow
                st.markdown(f"#### ✍️ {t('triage_box_title', cur_lang)}")
                w_col1, w_col2, w_col3 = st.columns([2, 4, 1.5])

                with w_col1:
                    new_status = st.selectbox(
                        t("filter_status", cur_lang),
                        [TriageStatus.PENDING.value, TriageStatus.INVESTIGATING.value,
                         TriageStatus.CLEARED.value, TriageStatus.CONFIRMED.value],
                        index=[TriageStatus.PENDING.value, TriageStatus.INVESTIGATING.value,
                               TriageStatus.CLEARED.value, TriageStatus.CONFIRMED.value].index(status),
                        key=f"status_select_{aid}"
                    )
                with w_col2:
                    new_notes = st.text_input(
                        t("reviewer_notes_label", cur_lang),
                        value=notes,
                        placeholder="e.g. Cross-checked with Sub-Registry Book 4; verified boundary decree.",
                        key=f"notes_input_{aid}"
                    )
                with w_col3:
                    st.write("")
                    st.write("")
                    if st.button(t("btn_update_triage", cur_lang), key=f"btn_save_{aid}", use_container_width=True):
                        update_alert_triage(aid, new_status, new_notes, DEFAULT_DB_PATH)
                        st.success(t("triage_updated_msg", cur_lang))
                        st.rerun()


# -----------------------------------------------------------------------------
# MAIN APP: VIEW 3 - SEARCHABLE PLOT HISTORY & TIMELINE
# -----------------------------------------------------------------------------
def render_plot_history_view(cur_lang: str = "bn"):
    st.markdown(f'<div class="main-header">{t("plot_view_title", cur_lang)}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header bn-text">{t("plot_view_sub", cur_lang)}</div>', unsafe_allow_html=True)

    search_query = st.text_input(
        t("select_plot_label", cur_lang),
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
        st.markdown(f"<span class='record-count-text'>{('খুঁজে পাওয়া দাগ:' if cur_lang == 'bn' else 'Found plots:')} <strong>{fmt_num(len(matched_plots), cur_lang)}</strong></span>", unsafe_allow_html=True)
        selected_plot_id = st.selectbox(
            t("select_plot_label", cur_lang),
            options=matched_plots["plot_id"].tolist(),
            format_func=lambda x: f"Plot {x} — {matched_plots[matched_plots['plot_id']==x]['mouza'].values[0]} (Dag: {matched_plots[matched_plots['plot_id']==x]['dag_no'].values[0]}, Area: {matched_plots[matched_plots['plot_id']==x]['total_area_decimals'].values[0]} dec)"
        )

        plot_info = get_plot_details(selected_plot_id, DEFAULT_DB_PATH)
        deeds_df, mutations_df = get_plot_transactions(selected_plot_id, DEFAULT_DB_PATH)
        plot_alerts = get_all_alerts(DEFAULT_DB_PATH)
        if not plot_alerts.empty:
            plot_alerts = plot_alerts[plot_alerts["plot_id"] == selected_plot_id]

        # Plot Details Master Cards
        st.markdown(f'<div class="section-title">🗺️ {("দাগের মূল রেকর্ড ও খতিয়ান সারসংক্ষেপ" if cur_lang == "bn" else "Plot Registry Master Record")}</div>', unsafe_allow_html=True)
        p_c1, p_c2, p_c3, p_c4 = st.columns(4)
        with p_c1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">{t("plot_meta_mouza", cur_lang)}</div>
                <div style="font-weight:750; font-size:1.15rem; color:var(--jg-ink);">{plot_info['mouza']} · JL {fmt_num(plot_info['jl_no'], cur_lang)}</div>
                <div class="kpi-foot">{plot_info['upazila']}, {plot_info['district']}</div>
            </div>
            """, unsafe_allow_html=True)
        with p_c2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">{t("plot_meta_dag", cur_lang)}</div>
                <div style="font-weight:750; font-size:1.15rem; color:var(--jg-ink);"><span class="mono-id">{plot_info['dag_no']}</span></div>
                <div class="kpi-foot">{t("plot_meta_khatian", cur_lang)} <span class="mono-id">{plot_info['khatian_no']}</span></div>
            </div>
            """, unsafe_allow_html=True)
        with p_c3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">{t("plot_meta_area", cur_lang)}</div>
                <div style="font-weight:750; font-size:1.15rem; color:var(--jg-ink);"><span class="mono-id">{fmt_num(plot_info['total_area_decimals'], cur_lang)}</span> {("শতাংশ" if cur_lang == "bn" else "dec")}</div>
                <div class="kpi-foot">{t("plot_meta_type", cur_lang)} {plot_info['land_type']}</div>
            </div>
            """, unsafe_allow_html=True)
        with p_c4:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">{t("plot_meta_owner", cur_lang)}</div>
                <div style="font-weight:750; font-size:1.15rem; color:var(--jg-ink);">{plot_info['initial_owner_name']}</div>
                <div class="kpi-foot"><span class="mono-id">{plot_info['initial_owner_nid']}</span></div>
            </div>
            """, unsafe_allow_html=True)

        # Compute total transferred decimals on this plot
        total_transferred = float(deeds_df["transferred_area_decimals"].sum()) if not deeds_df.empty else 0.0

        # ANIMATED PLOT CAPACITY OVERFLOW BAR
        render_plot_capacity_bar(
            total_area=plot_info["total_area_decimals"],
            transferred_area=total_transferred,
            cur_lang=cur_lang
        )

        # Active Inconsistency Warnings
        if not plot_alerts.empty:
            st.error(f"🚨 {('এই দাগে' if cur_lang == 'bn' else 'This plot has')} {fmt_num(len(plot_alerts), cur_lang)} {('টি সক্রিয় অসঙ্গতি বা বিরোধ শনাক্ত হয়েছে!' if cur_lang == 'bn' else 'active inconsistency alert(s) on file!')}")
            if cur_lang == "bn":
                plot_alert_cols = {
                    "alert_id": st.column_config.TextColumn("অ্যালার্ট আইডি"),
                    "severity": st.column_config.TextColumn("ঝুঁকির মাত্রা"),
                    "rule_name": st.column_config.TextColumn("রুলের নাম"),
                    "title": st.column_config.TextColumn("অসঙ্গতির সারসংক্ষেপ"),
                    "triage_status": st.column_config.TextColumn("পর্যালোচনা স্থিতি"),
                }
            else:
                plot_alert_cols = {
                    "alert_id": st.column_config.TextColumn("Alert ID"),
                    "severity": st.column_config.TextColumn("Severity"),
                    "rule_name": st.column_config.TextColumn("Triggered Rule"),
                    "title": st.column_config.TextColumn("Incident Summary"),
                    "triage_status": st.column_config.TextColumn("Review Status"),
                }
            st.dataframe(
                plot_alerts[[
                    "alert_id", "severity", "rule_name", "title", "triage_status"
                ]],
                use_container_width=True,
                column_config=plot_alert_cols,
                hide_index=True
            )
        else:
            st.success("✅ " + ("এই দাগে কোনো দ্বৈত বিক্রয় বা নামজারি বিরোধ শনাক্ত হয়নি।" if cur_lang == "bn" else "No conflicting transactions or mutation inconsistencies detected for this plot."))

        st.markdown("---")

        # Interactive Timeline
        st.markdown(f'<div class="section-title">{t("timeline_section_title", cur_lang)}</div>', unsafe_allow_html=True)

        timeline_events = []
        timeline_events.append({
            "Date": "2021-01-01",
            "Event": f"{('আদি রেকর্ড:' if cur_lang == 'bn' else 'Genesis Record:')} {plot_info['initial_owner_name']}",
            "Type": "Genesis Record",
            "Area": f"{plot_info['total_area_decimals']} dec",
            "Color": "#1B6B50"
        })

        for _, d in deeds_df.iterrows():
            timeline_events.append({
                "Date": d["registration_date"],
                "Event": f"{('দলিল' if cur_lang == 'bn' else 'Deed')} {d['deed_no']}: {d['seller_name']} ➔ {d['buyer_name']}",
                "Type": "Deed Registration",
                "Area": f"{d['transferred_area_decimals']} dec",
                "Color": "#2563EB"
            })

        for _, m in mutations_df.iterrows():
            timeline_events.append({
                "Date": m["mutation_date"],
                "Event": f"{('নামজারি' if cur_lang == 'bn' else 'Mutation')} {m['mutation_case_no']} (Khatian {m['new_khatian_no']})",
                "Type": "Mutation Approved",
                "Area": f"{m['mutated_area_decimals']} dec",
                "Color": "#7C3AED"
            })

        df_timeline = pd.DataFrame(timeline_events).sort_values("Date").reset_index(drop=True)
        df_timeline["Index"] = df_timeline.index + 1

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_timeline["Date"],
            y=[1] * len(df_timeline),
            mode="lines+markers+text",
            text=[fmt_num(i, cur_lang) for i in df_timeline["Index"]],
            textposition="middle center",
            textfont=dict(color="#FFFFFF", size=11, family="JetBrains Mono, monospace"),
            marker=dict(
                size=32,
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
        cur_theme = st.session_state.get("user_theme_mode", "Auto (System)")
        is_dark = (cur_theme == "Dark")
        chart_font_color = "#F8FAFC" if is_dark else "#1E293B"
        chart_grid_color = "rgba(255,255,255,0.12)" if is_dark else "rgba(148, 163, 184, 0.2)"

        fig.update_layout(
            height=200,
            xaxis=dict(
                title=dict(text=("তারিখ" if cur_lang == "bn" else "Transaction Date"), font=dict(color=chart_font_color)),
                showgrid=True,
                gridcolor=chart_grid_color,
                tickfont=dict(color=chart_font_color)
            ),
            yaxis=dict(showticklabels=False, range=[0.6, 1.4], showgrid=False),
            font=dict(color=chart_font_color, family="Plus Jakarta Sans, sans-serif"),
            margin=dict(l=20, r=20, t=20, b=30),
            showlegend=False,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)

        # Timeline Event Legend
        legend_html = "".join(
            f'<div class="tl-item">'
            f'<span class="tl-dot" style="background:{r.Color}"></span>'
            f'<span class="tl-idx mono-id">{fmt_num(r.Index, cur_lang)}</span>'
            f'<span class="tl-date mono-id">{r.Date}</span>'
            f'<span class="tl-event">{html.escape(str(r.Event))}</span>'
            f'</div>'
            for r in df_timeline.itertuples()
        )
        st.markdown(f'<div class="tl-legend">{legend_html}</div>', unsafe_allow_html=True)

        st.markdown("---")

        # Tables for Deeds & Mutations
        t_col1, t_col2 = st.columns(2)
        with t_col1:
            st.markdown(f"#### {t('table_deeds_title', cur_lang)}")
            if deeds_df.empty:
                st.info("No deeds registered for this plot.")
            else:
                if cur_lang == "bn":
                    deed_cols = {
                        "deed_no": st.column_config.TextColumn("দলিল নং"),
                        "registration_date": st.column_config.TextColumn("রেজিস্ট্রেশনের তারিখ"),
                        "seller_name": st.column_config.TextColumn("বিক্রেতার নাম"),
                        "buyer_name": st.column_config.TextColumn("ক্রেতার নাম"),
                        "transferred_area_decimals": st.column_config.NumberColumn(
                            "আয়তন (শতাংশ)", format="%.2f শতাংশ"
                        ),
                        "deed_value_bdt": st.column_config.NumberColumn(
                            "দলিল মূল্য", format="৳ %d"
                        ),
                    }
                else:
                    deed_cols = {
                        "deed_no": st.column_config.TextColumn("Deed No"),
                        "registration_date": st.column_config.TextColumn("Reg. Date"),
                        "seller_name": st.column_config.TextColumn("Seller Name"),
                        "buyer_name": st.column_config.TextColumn("Buyer Name"),
                        "transferred_area_decimals": st.column_config.NumberColumn(
                            "Area (dec)", format="%.2f dec"
                        ),
                        "deed_value_bdt": st.column_config.NumberColumn(
                            "Deed Value", format="BDT %d"
                        ),
                    }
                st.dataframe(
                    deeds_df[[
                        "deed_no", "registration_date", "seller_name", "buyer_name",
                        "transferred_area_decimals", "deed_value_bdt"
                    ]],
                    use_container_width=True,
                    column_config=deed_cols,
                    hide_index=True
                )
        with t_col2:
            st.markdown(f"#### {t('table_mutations_title', cur_lang)}")
            if mutations_df.empty:
                st.info("No mutations approved for this plot.")
            else:
                if cur_lang == "bn":
                    mut_cols = {
                        "mutation_case_no": st.column_config.TextColumn("নামজারি কেস নং"),
                        "deed_no": st.column_config.TextColumn("রেফারেন্স দলিল"),
                        "mutation_date": st.column_config.TextColumn("অনুমোদনের তারিখ"),
                        "applicant_name": st.column_config.TextColumn("আবেদনকারী"),
                        "mutated_area_decimals": st.column_config.NumberColumn(
                            "অনুমোদিত আয়তন", format="%.2f শতাংশ"
                        ),
                        "new_khatian_no": st.column_config.TextColumn("নতুন খতিয়ান নং"),
                        "status": st.column_config.TextColumn("স্থিতি"),
                    }
                else:
                    mut_cols = {
                        "mutation_case_no": st.column_config.TextColumn("Mutation Case No"),
                        "deed_no": st.column_config.TextColumn("Cited Deed No"),
                        "mutation_date": st.column_config.TextColumn("Approval Date"),
                        "applicant_name": st.column_config.TextColumn("Applicant Name"),
                        "mutated_area_decimals": st.column_config.NumberColumn(
                            "Mutated Area (dec)", format="%.2f dec"
                        ),
                        "new_khatian_no": st.column_config.TextColumn("New Khatian"),
                        "status": st.column_config.TextColumn("Status"),
                    }
                st.dataframe(
                    mutations_df[[
                        "mutation_case_no", "deed_no", "mutation_date", "applicant_name",
                        "mutated_area_decimals", "new_khatian_no", "status"
                    ]],
                    use_container_width=True,
                    column_config=mut_cols,
                    hide_index=True
                )


# -----------------------------------------------------------------------------
# MAIN APP: VIEW 4 - INTERACTIVE DEMO & SANDBOX (With conflictPulse Animation)
# -----------------------------------------------------------------------------
def render_sandbox_view(cur_lang: str = "bn"):
    st.markdown(f'<div class="main-header">{t("sandbox_title", cur_lang)}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header bn-text">{t("sandbox_sub", cur_lang)}</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="governance-shield bn-text">
        {t("sandbox_instructions", cur_lang)}
    </div>
    """, unsafe_allow_html=True)

    plots_df = get_all_plots(DEFAULT_DB_PATH)
    deeds_df = get_all_deeds(DEFAULT_DB_PATH)

    tab1, tab2, tab3, tab4 = st.tabs([
        t("tab_inj_duplicate", cur_lang),
        t("tab_inj_area", cur_lang),
        t("tab_inj_identity", cur_lang),
        t("tab_inj_paradox", cur_lang)
    ])

    # Tab 1: Duplicate Sale
    with tab1:
        st.markdown(f"### {('একই দাগে দ্বৈত বিক্রয় দলিল ইনজেকশন' if cur_lang == 'bn' else 'Inject Conflicting Double-Selling')}")
        st.write("Simulates a rogue seller executing a second deed for the same plot to a different buyer.")

        clean_plots = plots_df[~plots_df["plot_id"].isin(["P-201", "P-202"])]["plot_id"].tolist()
        c_p = st.selectbox("Select Target Plot for Injection", options=clean_plots, key="inj_p_dup")

        plot_info = get_plot_details(c_p, DEFAULT_DB_PATH)
        st.caption(f"Plot {c_p} — Area: {plot_info['total_area_decimals']} decimals | Owner: {plot_info['initial_owner_name']}")

        d_col1, d_col2 = st.columns(2)
        with d_col1:
            seller_name = st.text_input("Seller Name", value=plot_info["initial_owner_name"], key="inj_s_name")
            seller_nid = st.text_input("Seller NID", value=plot_info["initial_owner_nid"], key="inj_s_nid")
        with d_col2:
            buyer_2_name = st.text_input("Second Buyer Name", value="Zubair Al Mahmud", key="inj_b2_name")
            buyer_2_nid = st.text_input("Second Buyer NID", value="19952619827361999", key="inj_b2_nid")

        area_to_sell = st.number_input(
            "Transferred Area (decimals)",
            min_value=1.0,
            max_value=50.0,
            value=float(plot_info["total_area_decimals"]),
            key="inj_area_dup"
        )

        if st.button(t("btn_inject_dup", cur_lang), key="btn_inj_dup", type="primary"):
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
            alerts, summary = run_detection(DEFAULT_DB_PATH)
            st.session_state["last_scan_metrics"] = summary
            st.session_state["just_injected"] = True
            st.success(f"Conflicting deed {new_deed} injected! Detection engine flagged {len(alerts)} alerts.")
            st.rerun()

    # Tab 2: Area Mismatch
    with tab2:
        st.markdown(f"### {('নামজারিতে অতিরিক্ত আয়তন ইনজেকশন' if cur_lang == 'bn' else 'Inject Registration vs. Mutation Area Mismatch')}")
        st.write("Simulates unauthorized inflation of land area during revenue mutation (Namjari).")

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

        if st.button(t("btn_inject_area", cur_lang), key="btn_inj_area", type="primary"):
            new_mut = inject_area_mismatch(target_deed_no, inflated_area, DEFAULT_DB_PATH)
            alerts, summary = run_detection(DEFAULT_DB_PATH)
            st.session_state["last_scan_metrics"] = summary
            st.session_state["just_injected"] = True
            st.success(f"Inflated mutation {new_mut} injected (+{inflated_area - deed_area:.2f} decimals)! Anomaly detected.")
            st.rerun()

    # Tab 3: Identity Mismatch
    with tab3:
        st.markdown(f"### {('ভুয়া আবেদনকারী প্রতিস্থাপন ইনজেকশন' if cur_lang == 'bn' else 'Inject Applicant Identity Mismatch')}")
        st.write("Simulates a mutation approved in favor of an unauthorized applicant instead of the registered buyer.")

        target_deed_id = st.selectbox("Select Deed", options=deeds_df["deed_no"].tolist()[:10], key="inj_deed_id")
        selected_deed_id = deeds_df[deeds_df["deed_no"] == target_deed_id].iloc[0]

        st.write(f"**Registered Buyer:** {selected_deed_id['buyer_name']} (NID: {selected_deed_id['buyer_nid']})")

        impostor_name = st.text_input("Mismatched Applicant Name", value="Akramuzzaman Khan", key="inj_imp_name")
        impostor_nid = st.text_input("Mismatched Applicant NID", value="19652619827361777", key="inj_imp_nid")

        if st.button(t("btn_inject_id", cur_lang), key="btn_inj_id", type="primary"):
            new_mut = inject_identity_mismatch(target_deed_id, impostor_name, impostor_nid, DEFAULT_DB_PATH)
            alerts, summary = run_detection(DEFAULT_DB_PATH)
            st.session_state["last_scan_metrics"] = summary
            st.session_state["just_injected"] = True
            st.success(f"Mismatched mutation {new_mut} injected! Alert triggered.")
            st.rerun()

    # Tab 4: Chronological Paradox
    with tab4:
        st.markdown(f"### {('কালানুক্রমিক প্যারাডক্স ইনজেকশন' if cur_lang == 'bn' else 'Inject Chronological Paradox')}")
        st.write("Simulates a mutation record bearing an approval date earlier than the deed registration date.")

        target_deed_time = st.selectbox("Select Deed for Paradox", options=deeds_df["deed_no"].tolist()[:10], key="inj_deed_time")
        selected_deed_time = deeds_df[deeds_df["deed_no"] == target_deed_time].iloc[0]

        st.write(f"**Deed Registration Date:** {selected_deed_time['registration_date']}")

        if st.button(t("btn_inject_time", cur_lang), key="btn_inj_time", type="primary"):
            new_mut = inject_temporal_paradox(target_deed_time, DEFAULT_DB_PATH)
            alerts, summary = run_detection(DEFAULT_DB_PATH)
            st.session_state["last_scan_metrics"] = summary
            st.session_state["just_injected"] = True
            st.success(f"Paradoxical mutation {new_mut} injected! Alert triggered.")
            st.rerun()


# -----------------------------------------------------------------------------
# MAIN APP: VIEW 5 - DOWNLOADABLE REPORTS
# -----------------------------------------------------------------------------
def render_reports_view(cur_lang: str = "bn"):
    st.markdown(f'<div class="main-header">{t("reports_title", cur_lang)}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header bn-text">{t("reports_sub", cur_lang)}</div>', unsafe_allow_html=True)

    alerts_df = get_all_alerts(DEFAULT_DB_PATH)
    summary_metrics = st.session_state.get("last_scan_metrics", {})

    rep_col1, rep_col2 = st.columns(2)
    with rep_col1:
        with st.container(border=True):
            st.markdown(f'<div class="section-title">{t("card_csv_title", cur_lang)}</div>', unsafe_allow_html=True)
            st.write(t("card_csv_desc", cur_lang))
            csv_data = export_alerts_to_csv(alerts_df)
            st.download_button(
                label=t("btn_download_csv", cur_lang),
                data=csv_data,
                file_name=f"jomiguard_alerts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )

    with rep_col2:
        with st.container(border=True):
            st.markdown(f'<div class="section-title">{t("card_md_title", cur_lang)}</div>', unsafe_allow_html=True)
            st.write(t("card_md_desc", cur_lang))
            md_report = generate_markdown_audit_report(alerts_df, summary_metrics)
            st.download_button(
                label=t("btn_download_md", cur_lang),
                data=md_report,
                file_name=f"jomiguard_investigation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                use_container_width=True,
                type="primary"
            )

    st.markdown("")
    st.markdown(f'<div class="section-title">{t("report_preview_title", cur_lang)}</div>', unsafe_allow_html=True)
    st.markdown(md_report)


# -----------------------------------------------------------------------------
# MAIN APP ROUTING & SIDEBAR
# -----------------------------------------------------------------------------
def render_main_application(cur_lang: str = "bn"):
    """Render full operational application with sidebar navigation."""
    render_navbar(cur_lang=cur_lang, in_app=True)

    with st.sidebar:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg, var(--jg-brand) 0%, #155E44 100%); border-radius:14px; padding:16px; color:#FFFFFF; margin-bottom:12px; box-shadow:var(--jg-shadow);">
            <div style="font-size:1.35rem; font-weight:850; letter-spacing:-0.02em;">{t("sidebar_brand", cur_lang)}</div>
            <div style="font-size:0.82rem; color:rgba(255,255,255,0.85);">{t("sidebar_tagline", cur_lang)}</div>
        </div>
        """, unsafe_allow_html=True)

        st.caption(t("sidebar_sub", cur_lang))

        nav_items = [
            ("dashboard", t("nav_tab_dashboard", cur_lang)),
            ("alerts", t("nav_tab_alerts", cur_lang)),
            ("plots", t("nav_tab_plots", cur_lang)),
            ("sandbox", t("nav_tab_sandbox", cur_lang)),
            ("reports", t("nav_tab_reports", cur_lang))
        ]
        
        cur_active = st.session_state.get("active_nav_app", "dashboard")

        st.markdown('<div class="sidebar-nav-wrapper">', unsafe_allow_html=True)
        for key, label in nav_items:
            is_active = (cur_active == key)
            btn_type = "primary" if is_active else "secondary"
            if st.button(
                label,
                key=f"sidebar_nav_{key}",
                use_container_width=True,
                type=btn_type
            ):
                if cur_active != key:
                    st.session_state["active_nav_app"] = key
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown(f"##### {t('sidebar_quick_actions', cur_lang)}")

        if st.button(t("btn_rescan", cur_lang), use_container_width=True):
            alerts, summary = run_detection(DEFAULT_DB_PATH)
            st.session_state["last_scan_metrics"] = summary
            st.success(t("rescan_success", cur_lang, count=fmt_num(len(alerts), cur_lang)))
            st.rerun()

        if st.button(t("btn_reset_db", cur_lang), use_container_width=True):
            seed_database(DEFAULT_DB_PATH)
            alerts, summary = run_detection(DEFAULT_DB_PATH)
            st.session_state["last_scan_metrics"] = summary
            st.info(t("reset_success", cur_lang))
            st.rerun()

        st.markdown("---")
        st.markdown(f"##### {t('sidebar_theme_label', cur_lang)}")
        cur_theme = st.session_state.get("user_theme_mode", "Auto (System)")
        theme_choice = st.segmented_control(
            "Display Theme",
            options=["Auto (System)", "Light", "Dark"],
            default=cur_theme,
            key="theme_mode_selector_app",
            label_visibility="collapsed"
        )
        if theme_choice and theme_choice != cur_theme:
            st.session_state["user_theme_mode"] = theme_choice
            st.rerun()

        st.markdown("")
        st.caption(t("sidebar_engine_caption", cur_lang))

    # Route to view
    active_key = st.session_state.get("active_nav_app", "dashboard")
    if active_key == "dashboard":
        render_dashboard_view(cur_lang)
    elif active_key == "alerts":
        render_alerts_view(cur_lang)
    elif active_key == "plots":
        render_plot_history_view(cur_lang)
    elif active_key == "sandbox":
        render_sandbox_view(cur_lang)
    elif active_key == "reports":
        render_reports_view(cur_lang)


# -----------------------------------------------------------------------------
# APPLICATION ENTRYPOINT
# -----------------------------------------------------------------------------
if st.session_state.get("view_mode", "landing") == "landing":
    render_landing_page(cur_lang=lang)
else:
    render_main_application(cur_lang=lang)
