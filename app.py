"""
JomiGuard — Land Fraud & Double-Selling Alert System
Streamlit Dashboard Application
"""

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

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.1rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.2rem;
    }
    .disclaimer-card {
        background-color: #FEF3C7;
        border-left: 5px solid #F59E0B;
        padding: 12px 16px;
        border-radius: 6px;
        color: #92400E;
        font-size: 0.95rem;
        margin-bottom: 1.2rem;
    }
    .metric-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
    .badge-critical {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.82rem;
    }
    .badge-high {
        background-color: #FFEDD5;
        color: #9A3412;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.82rem;
    }
    .badge-medium {
        background-color: #FEF9C3;
        color: #854D0E;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.82rem;
    }
    .badge-low {
        background-color: #E0F2FE;
        color: #075985;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.82rem;
    }
    .trigger-box {
        background-color: #F1F5F9;
        border-left: 4px solid #3B82F6;
        padding: 12px;
        border-radius: 4px;
        margin-top: 8px;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)


# Initialize Database and Run Detector once
init_db_if_needed(DEFAULT_DB_PATH)
if "last_scan_metrics" not in st.session_state:
    alerts, summary = run_detection(DEFAULT_DB_PATH)
    st.session_state["last_scan_metrics"] = summary


# -----------------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🛡️ JomiGuard")
    st.markdown("**Land Fraud & Double-Selling Alert System**")
    st.caption("Data Analytics & Rule-Based Anomaly Detection")
    st.markdown("---")
    
    nav_option = st.radio(
        "Navigation Menu",
        [
            "📊 Dashboard Overview",
            "🚨 Alerts & Risk Investigation",
            "🔍 Searchable Plot History",
            "🧪 Interactive Demo & Sandbox",
            "📑 Downloadable Reports"
        ]
    )
    
    st.markdown("---")
    st.markdown("### ⚙️ Quick Actions")
    
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
        
    st.markdown("---")
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
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Plots Screened", len(plots_df))
    with col2:
        st.metric("Total Registered Deeds", len(deeds_df))
    with col3:
        st.metric("Total Approved Mutations", len(mutations_df))
    with col4:
        critical_count = len(alerts_df[alerts_df["severity"] == "CRITICAL"]) if not alerts_df.empty else 0
        st.metric("Active Inconsistencies", len(alerts_df), delta=f"{critical_count} Critical", delta_color="inverse")
        
    st.markdown("---")
    
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

    st.markdown("---")
    st.subheader("🚨 Priority Inconsistency Ledger")
    
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
        
    st.markdown(f"**Showing {len(alerts_df)} flagged record(s)**")
    
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
                st.markdown('<div class="trigger-box">', unsafe_allow_html=True)
                
                # Format trigger fields nicely
                cols = st.columns(min(len(trigger_data), 3) if trigger_data else 1)
                t_items = list(trigger_data.items())
                for i, (k, v) in enumerate(t_items):
                    c_idx = i % min(len(trigger_data), 3)
                    with cols[c_idx]:
                        label = k.replace("_", " ").title()
                        st.markdown(f"**{label}**")
                        st.code(str(v), language="text")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Side-by-side Evidence Comparison
                st.markdown("#### ⚖️ Conflicting Records Side-by-Side")
                if "first_deed" in evidence_data and "second_deed" in evidence_data:
                    # Double-Selling comparison
                    c_left, c_right = st.columns(2)
                    with c_left:
                        st.markdown("**Prior Registered Deed**")
                        st.json(evidence_data["first_deed"])
                    with c_right:
                        st.markdown("**Subsequent Conflicting Deed**")
                        st.json(evidence_data["second_deed"])
                elif "deed_record" in evidence_data and "mutation_record" in evidence_data:
                    # Deed vs Mutation comparison
                    c_left, c_right = st.columns(2)
                    with c_left:
                        st.markdown("**Registered Sale Deed**")
                        st.json(evidence_data["deed_record"])
                    with c_right:
                        st.markdown("**Revenue Mutation Record**")
                        st.json(evidence_data["mutation_record"])
                else:
                    st.json(evidence_data)
                    
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
        st.markdown(f"**Found {len(matched_plots)} plot(s)**")
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
        st.markdown("### 🗺️ Plot Registry Master Record")
        p_c1, p_c2, p_c3, p_c4 = st.columns(4)
        with p_c1:
            st.metric("Mouza & JL", f"{plot_info['mouza']} (JL: {plot_info['jl_no']})")
            st.caption(f"Thana/Upazila: {plot_info['upazila']}")
        with p_c2:
            st.metric("Dag & Khatian", f"Dag: {plot_info['dag_no']}")
            st.caption(f"Khatian: {plot_info['khatian_no']}")
        with p_c3:
            st.metric("Total Land Area", f"{plot_info['total_area_decimals']} Decimals")
            st.caption(f"Classification: {plot_info['land_type']}")
        with p_c4:
            st.metric("Initial Recorded Owner", plot_info["initial_owner_name"])
            st.caption(f"NID: {plot_info['initial_owner_nid']}")
            
        # Alert warning if plot has flags
        if not plot_alerts.empty:
            st.error(f"🚨 This plot has {len(plot_alerts)} active inconsistency alert(s) on file! Review ledger below.")
            for _, pa in plot_alerts.iterrows():
                st.markdown(f"- **[{pa['severity']}] {pa['title']}** — _{pa['explanation']}_")
        else:
            st.success("✅ No conflicting transactions or mutation inconsistencies detected for this plot.")
            
        st.markdown("---")
        
        # Interactive Plotly Visual Timeline
        st.markdown("### 📈 Visual Transaction & Ownership Timeline")
        
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
            
        df_timeline = pd.DataFrame(timeline_events).sort_values("Date")
        
        fig = go.Figure()
        
        # Scatter line for chronological flow
        fig.add_trace(go.Scatter(
            x=df_timeline["Date"],
            y=[1] * len(df_timeline),
            mode="lines+markers+text",
            text=df_timeline["Event"],
            textposition="top center",
            marker=dict(
                size=14,
                color=df_timeline["Color"]
            ),
            line=dict(color="#CBD5E1", width=3),
            hoverinfo="text",
            hovertext=[f"Date: {r['Date']}<br>Type: {r['Type']}<br>Area: {r['Area']}" for _, r in df_timeline.iterrows()]
        ))
        
        fig.update_layout(
            height=280,
            xaxis=dict(title="Transaction Date", showgrid=True),
            yaxis=dict(showticklabels=False, range=[0.5, 1.6], showgrid=False),
            margin=dict(l=20, r=20, t=30, b=30),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
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
        st.markdown("### 📥 Export Alerts Ledger (CSV)")
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
        st.markdown("### 📄 Export Investigation Report (Markdown)")
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
        
    st.markdown("---")
    st.markdown("### 👁️ Report Preview")
    st.markdown(md_report)
