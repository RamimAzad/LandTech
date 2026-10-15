-- JomiGuard Database Schema
-- Land Fraud & Double-Selling Alert System

CREATE TABLE IF NOT EXISTS plots (
    plot_id TEXT PRIMARY KEY,
    mouza TEXT NOT NULL,
    jl_no INTEGER NOT NULL,
    khatian_no TEXT NOT NULL,
    dag_no TEXT NOT NULL,
    total_area_decimals REAL NOT NULL,
    district TEXT NOT NULL,
    upazila TEXT NOT NULL,
    land_type TEXT NOT NULL,
    initial_owner_nid TEXT NOT NULL,
    initial_owner_name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS deeds (
    deed_no TEXT PRIMARY KEY,
    plot_id TEXT NOT NULL,
    registration_date TEXT NOT NULL,
    seller_nid TEXT NOT NULL,
    seller_name TEXT NOT NULL,
    buyer_nid TEXT NOT NULL,
    buyer_name TEXT NOT NULL,
    transferred_area_decimals REAL NOT NULL,
    deed_value_bdt REAL NOT NULL,
    sub_registry_office TEXT NOT NULL,
    status TEXT DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (plot_id) REFERENCES plots(plot_id)
);

CREATE TABLE IF NOT EXISTS mutations (
    mutation_case_no TEXT PRIMARY KEY,
    deed_no TEXT NOT NULL,
    plot_id TEXT NOT NULL,
    mutation_date TEXT NOT NULL,
    applicant_nid TEXT NOT NULL,
    applicant_name TEXT NOT NULL,
    mutated_area_decimals REAL NOT NULL,
    new_khatian_no TEXT NOT NULL,
    ac_land_office TEXT NOT NULL,
    status TEXT DEFAULT 'Approved',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (plot_id) REFERENCES plots(plot_id)
);

CREATE TABLE IF NOT EXISTS alerts (
    alert_id TEXT PRIMARY KEY,
    rule_id TEXT NOT NULL,
    rule_name TEXT NOT NULL,
    plot_id TEXT NOT NULL,
    severity TEXT NOT NULL,
    title TEXT NOT NULL,
    explanation TEXT NOT NULL,
    trigger_fields_json TEXT NOT NULL,
    evidence_json TEXT NOT NULL,
    triage_status TEXT DEFAULT 'Pending Review',
    reviewer_notes TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (plot_id) REFERENCES plots(plot_id)
);

-- Indices for rapid querying and analysis
CREATE INDEX IF NOT EXISTS idx_deeds_plot_id ON deeds(plot_id);
CREATE INDEX IF NOT EXISTS idx_deeds_seller_nid ON deeds(seller_nid);
CREATE INDEX IF NOT EXISTS idx_deeds_buyer_nid ON deeds(buyer_nid);
CREATE INDEX IF NOT EXISTS idx_deeds_date ON deeds(registration_date);
CREATE INDEX IF NOT EXISTS idx_mutations_plot_id ON mutations(plot_id);
CREATE INDEX IF NOT EXISTS idx_mutations_deed_no ON mutations(deed_no);
CREATE INDEX IF NOT EXISTS idx_alerts_plot_id ON alerts(plot_id);
CREATE INDEX IF NOT EXISTS idx_alerts_severity ON alerts(severity);
CREATE INDEX IF NOT EXISTS idx_alerts_triage ON alerts(triage_status);
