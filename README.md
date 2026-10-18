# 🛡️ JomiGuard (জমিগার্ড) — Land Title Audit & Anomaly Detection Platform

> **National Civic RegTech & Institutional Record Verification System**<br>
> Real-time cross-matching of Sub-Registry deed registrations and AC Land e-mutations with mathematical parcel integrity verification, explainable evidence diffing, and automated fraud prevention.

---

## 📌 1. Project Overview & Operational Context

In Bangladesh, land ownership records are administered across two fundamentally disconnected government departments:
1. **Sub-Registry Offices (রেজিস্ট্রেশন অধিদপ্তর / আইন মন্ত্রণালয়)**: Record and execute deed transfers (সাব-কবলা দলিল).
2. **AC Land & Union Land Offices (ভূমি সংস্কার বোর্ড / ভূমি মন্ত্রণালয়)**: Record revenue ownership, survey khatians (খতিয়ান), and approve e-Mutations (ই-নামজারি).

Because these systems historically operated without real-time bilateral verification, fraudulent actors could exploit information gaps to execute **double sales**, submit **inflated mutation areas**, use **counterfeit NIDs**, or cite **phantom deed references**.

**JomiGuard (জমিগার্ড)** bridges this administrative divide. It provides an institutional-grade, explainable screening engine that detects conflicting transactions, flags anomalous record pairs, maps chronological chains of title, and empowers human officers (Sub-Registrars, AC Land officers, bank credit auditors, and property buyers) to make informed administrative determinations.

> ℹ️ **Guiding Principle — Decision-Support, Not Defamation**:<br>
> *An alert indicates a potential record inconsistency requiring human administrative verification, not proven criminal fraud.* Repeated plot identifiers or area variances can result from legitimate co-owner inheritance shares, survey corrections, or pending mutation rectifications.

---

## 🚀 2. How to Run JomiGuard

### Prerequisites
- **Python:** 3.10, 3.11, 3.12, or 3.13
- **Operating System:** macOS, Linux, or Windows (WSL / PowerShell)
- **Database:** SQLite 3 (included with Python standard library)

---

### Option A: One-Click Startup (Recommended)

Run the included automated startup script:

```bash
chmod +x run.sh
./run.sh
```

The script will automatically:
1. Create a clean virtual environment (`.venv`).
2. Upgrade `pip` and install all required packages from `requirements.txt`.
3. Set the `PYTHONPATH` and launch the Streamlit app on `http://localhost:8501`.

---

### Option B: Manual Setup & Launch

```bash
# 1. Clone or navigate to the project directory
cd /path/to/LandTech_3

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate       # On Windows: .venv\Scripts\activate

# 3. Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Verify test suite (All 7 anomaly detection rules)
PYTHONPATH=. pytest -v tests/test_detector.py

# 5. Launch the application
PYTHONPATH=. streamlit run app.py
```

Open your browser at **`http://localhost:8501`**.

---

### 3. Application Navigation & Features

| View / Feature | Description | Deep-Link Parameter |
| :--- | :--- | :--- |
| **🏠 Welcoming Landing Page** | Public educational front page detailing the problem, institutional stakeholders, multi-stage roadmap, and FAQs. | `http://localhost:8501/?view=landing` |
| **📊 ড্যাশবোর্ড ওভারভিউ** | Executive KPI cards (total plots, deeds, mutations, active alerts) and interactive Plotly risk charts. | `http://localhost:8501/?view=app&tab=dashboard` |
| **🚨 সতর্কতা ও ঝুঁকি অনুসন্ধান** | Detailed alert feed with filterable severity, triage status, and 4-column bilateral **Evidence Diff** tables (`≠` vs `=`). | `http://localhost:8501/?view=app&tab=alerts` |
| **🔍 দাগের ইতিহাস ও টাইমলাইন** | Searchable plot history across plot IDs, NIDs, Deed Nos, and Mouzas, complete with an interactive transaction timeline. | `http://localhost:8501/?view=app&tab=plots` |
| **🧪 ইন্টারঅ্যাকটিভ ডেমো ও স্যান্ডবক্স** | 1-click test scenarios to inject duplicate sales, area inflations, or identity mismatches live and test detection in real time. | `http://localhost:8501/?view=app&tab=sandbox` |
| **📑 ডাউনলোডযোগ্য অডিট রিপোর্ট** | Export complete investigation reports in printable Markdown format (with signature blocks) or CSV data ledgers. | `http://localhost:8501/?view=app&tab=reports` |

- **🌐 Bilingual Toggle**: Click `🌐 বাং / EN` in the top frosted navigation bar to toggle between Bengali (primary) and English.
- **🌓 Theme Toggle**: Switch between **Institutional Light Ledger** (light-first high-contrast palette) and **Night / Dark Mode** (`☀️ / 🌙`).

---

## 📊 3. What Data We Used

### A. Realistic Bangladesh Land Record Benchmark
Because live government land records contain sensitive National ID cards (NID) and confidential deed valuations, JomiGuard operates on a high-fidelity **synthetic benchmark dataset** modeled after real Bangladesh land administration conventions (`data/schema.sql` and `data/generator.py`).

The database (`jomiguard.db`) covers **41 unique plots across 8 major Mouzas in Greater Dhaka**:
- **Gulshan** (JL 19)
- **Dhanmondi** (JL 33)
- **Uttara** (JL 12)
- **Mirpur** (JL 28)
- **Tejgaon** (JL 15)
- **Badda** (JL 45)
- **Savar** (JL 56)
- **Keraniganj** (JL 64)

---

### B. Relational Data Entities & Schema

```
┌─────────────────────────────────┐
│              PLOTS              │
│  - plot_id (PK: P-101 .. P-207) │
│  - mouza, jl_no, khatian_no     │
│  - dag_no, total_area_decimals  │
│  - initial_owner_nid, name      │
└────────────────┬────────────────┘
                 │ 1:N
        ┌────────┴────────┐
        ▼                 ▼
┌───────────────────┐   ┌───────────────────────────┐
│       DEEDS       │   │         MUTATIONS         │
│  - deed_no (PK)   │   │  - mutation_case_no (PK)  │
│  - plot_id (FK)   │   │  - deed_no (FK)           │
│  - seller_nid     │   │  - plot_id (FK)           │
│  - buyer_nid      │   │  - applicant_nid, name    │
│  - area_decimals  │   │  - mutated_area_decimals  │
│  - deed_value_bdt │   │  - new_khatian_no         │
│  - status (Active)│   │  - status (Approved)      │
└─────────┬─────────┘   └─────────────┬─────────────┘
          │                           │
          └─────────────┬─────────────┘
                        ▼
┌──────────────────────────────────────────────┐
│                    ALERTS                    │
│  - alert_id (PK: ALT-YYYY-XXXX)              │
│  - rule_id, rule_name, plot_id               │
│  - severity (CRITICAL, HIGH, MEDIUM, LOW)    │
│  - trigger_fields_json, evidence_json        │
│  - triage_status (Pending, Investigating, ..)│
│  - reviewer_notes, updated_at                │
└──────────────────────────────────────────────┘
```

---

### C. Benchmark Anomaly Scenarios (Planted Test Cases)

The dataset contains clean multi-stage sequential transactions as well as controlled real-world anomaly patterns:

1. **`P-201` — Double Selling / Conflicting Transfers (`RULE_DOUBLE_SALE`)**:
   - Seller *Mohammad Rafiqul Islam* registered Deed `REG-2023-7001` to Buyer A on March 10, 2023 for 5.00 decimals.
   - Just 15 days later (March 25, 2023), the same seller registered Deed `REG-2023-7002` transferring 5.00 decimals of the same plot to Buyer B without proof of reacquisition.
2. **`P-202` — Cumulative Area Overflow (`RULE_AREA_OVERFLOW`)**:
   - Total surveyed plot capacity: **10.00 decimals**.
   - Sequential deeds executed: Deed 1 (6.00 dec) + Deed 2 (4.00 dec) + Deed 3 (4.50 dec) = **14.50 decimals (145% of plot capacity)**.
3. **`P-203` — AC Land Mutation Area Inflation (`RULE_AREA_MISMATCH`)**:
   - Sub-Registry Deed `REG-2023-7005` transferred **7.50 decimals**.
   - AC Land e-Mutation `MUT-2023-8003` was approved for **12.00 decimals (+60% area inflation)**.
4. **`P-204` — Mutation Identity Substitution (`RULE_IDENTITY_MISMATCH`)**:
   - Deed `REG-2023-7006` was purchased by *Kamal Hossain* (`NID: 19752619827361239`).
   - AC Land e-Mutation `MUT-2023-8004` was approved for *Moniruzzaman Mia* (`NID: 19712619827361245`) without Power of Attorney or succession records.
5. **`P-205` — Chronological Paradox / Inverted Timeline (`RULE_TEMPORAL_CONFLICT`)**:
   - e-Mutation `MUT-2023-8005` approval date is **February 10, 2023**.
   - Sub-Registry Deed `REG-2023-7007` was registered on **August 25, 2023** (mutation approved 6 months before the deed was executed).
6. **`P-206` — Phantom Deed Citation (`RULE_PHANTOM_MUTATION`)**:
   - e-Mutation `MUT-2023-8006` references Deed `REG-2023-9999`, which does not exist in the Sub-Registry database.
7. **`P-207` — Stale Unmutated Transfer (`RULE_STALE_DEED`)**:
   - Deed `REG-2022-6001` was registered over 180 days ago, yet no AC Land mutation application was filed.

---

## 🤖 4. Which AI & Engineering Tools Were Used

The development of JomiGuard combined frontier Generative AI tools for architecture and UI engineering with a deterministic Symbolic AI (Expert System) core:

### A. AI Engineering & Pair-Programming Tools
1. **Google Gemini & Anthropic Claude (Frontier LLMs)**:
   - **Architecture Co-Design**: Formulated the bilateral record reconciliation schema between Sub-Registry deed data and AC Land mutation data.
   - **Bilingual Legal Engineering**: Engineered domain-specific translations (e.g., differentiating between সাব-রেজিস্ট্রার, নামজারি খতিয়ান, দাগ, খতিয়ান, সাব-কবলা, and ওয়ারিশান) with appropriate Bengali administrative terminology.
   - **Mathematical Rule Formulation**: Designed cumulative area validation equations ($\sum_{i} \text{Area}_i \le \text{Total Plot Area}$) and tolerance thresholding algorithms.
2. **Antigravity Autonomous Coding Agent**:
   - **Full-Stack Implementation**: Generated and refactored modular Python components (`core/detector.py`, `core/db.py`, `core/theme.py`, `app.py`).
   - **Browser CDP Headless Verification**: Automated DOM-level testing and layout inspection using Chrome DevTools Protocol to confirm rendering, test tab switching, and eliminate CommonMark code-block parsing issues.
   - **Accessibility & Dark Mode Contrast Optimization**: Scanned computed DOM color brightness values across all components in both Light and Dark modes to ensure high contrast.
   - **Test-Driven Development (TDD)**: Authored unit tests with `pytest` for all anomaly rules.

---

### B. Core System AI Philosophy: Symbolic AI / Deterministic Expert Engine
Rather than using a black-box deep learning model for real-time land title audit, JomiGuard deliberately employs a **Symbolic AI / Expert Rule Engine**.

#### Why Symbolic AI over Deep Learning for Land Title Audit?
- **Zero Hallucination Tolerance**: In real-estate law and government land administration, an AI hallucination could falsely accuse an innocent citizen of fraud or improperly validate a forged title.
- **Explainable Evidence (No Black-Box Decisions)**: Under administrative law, decisions must cite exact evidence. Every alert generated by JomiGuard produces an exact **Evidence Diff Dossier** highlighting the conflicting parameters (`Deed No`, `NID`, `Area Decimals`, `Approval Dates`) in monospace font (`JetBrains Mono`).
- **Auditability & Legal Scrutiny**: The deterministic rule engine can be audited, challenged, and verified in court or AC Land mutation hearings.

---

### C. Future AI Roadmap (Phases 2 & 3)
As outlined on the landing page roadmap, future versions will integrate:
- **Vision-Language Models (VLM) & Document Layout AI**: Automated OCR and key-value information extraction from historic handwritten Sub-Registry deeds (হাতে লেখা ব্রিটিশ/পাকিস্তান আমলের সাব-কবলা দলিল ও বায়া দলিল).
- **Graph Neural Networks (GNN)**: Multi-party fraud ring and syndicate detection across connected family transfers and shell acquisitions.
- **LLM-Powered Legal Explanations**: Automated generation of natural-language legal summaries for complex multi-generational inheritance splits (ফারায়েজ / মুসলিম ও হিন্দু উত্তরাধিকার আইন).

---

## 🏗️ 5. Technology Stack

- **Application Framework:** [Streamlit 1.42+](https://streamlit.io/)
- **Data Manipulation & Analytics:** [Pandas 2.0+](https://pandas.pydata.org/)
- **Database Engine:** [SQLite 3](https://www.sqlite.org/) (Zero-latency relational database with indices)
- **Interactive Visualizations:** [Plotly Express & Graph Objects 5.18+](https://plotly.com/python/)
- **Testing & Quality Assurance:** [Pytest 7.0+](https://pytest.org/)
- **Typography & Font Stack:**
  - *Bengali UI & Narrative:* **Hind Siliguri** (400, 500, 600, 700) + **Noto Sans Bengali**
  - *English UI & Executive:* **Plus Jakarta Sans** (400, 500, 600, 700, 800)
  - *Legal Identifiers & Decimals:* **JetBrains Mono** with `font-variant-numeric: tabular-nums`

---

## 📂 6. Repository Structure

```
LandTech_3/
├── app.py                      # Main Streamlit application & interactive routing
├── run.sh                      # One-click executable launch script
├── requirements.txt            # Python package dependencies
├── README.md                   # Complete system documentation & guide
├── jomiguard.db                # SQLite database with seeded benchmark records
├── .streamlit/
│   └── config.toml             # Streamlit server theme configuration
├── core/
│   ├── __init__.py
│   ├── db.py                   # SQLite transactional queries & anomaly injection layer
│   ├── detector.py             # Deterministic Symbolic Anomaly Detection Engine
│   ├── models.py               # Typed dataclasses (AnomalyAlert, TriageStatus, etc.)
│   ├── theme.py                # RegTech theme tokens, dual-mode CSS & micro-animations
│   ├── i18n.py                 # Bilingual translation dictionaries (Bangla & English)
│   └── reporter.py             # CSV ledger & Markdown audit report generators
├── data/
│   ├── __init__.py
│   ├── schema.sql              # Relational database schema with indices & foreign keys
│   └── generator.py            # Synthetic benchmark dataset generator & seeder
└── tests/
    └── test_detector.py        # Automated Pytest suite covering all 7 anomaly detectors
```

---

## 🧪 7. Running Tests

To verify all anomaly detection algorithms against benchmark data:

```bash
# Activate your virtual environment first
source .venv/bin/activate

# Execute pytest
pytest -v tests/test_detector.py
```

Expected output:
```
============================= test session starts ==============================
collected 7 items

tests/test_detector.py::test_clean_chain_no_false_positives PASSED       [ 14%]
tests/test_detector.py::test_double_selling_detection PASSED             [ 28%]
tests/test_detector.py::test_area_mismatch_detection PASSED              [ 42%]
tests/test_detector.py::test_identity_mismatch_detection PASSED          [ 57%]
tests/test_detector.py::test_temporal_paradox_detection PASSED           [ 71%]
tests/test_detector.py::test_phantom_deed_detection PASSED               [ 85%]
tests/test_detector.py::test_explainable_indicators_completeness PASSED  [100%]

============================== 7 passed in 0.33s ===============================
```

---

## ⚖️ 8. Legal Governance & Compliance Notice

JomiGuard is designed strictly as an **administrative decision-support system**. It does not perform judicial adjudications or impose criminal classifications. All flagged alerts require review by an authorized administrative officer (e.g., Sub-Registrar or Assistant Commissioner of Land) before any legal action or deed registration pause is instituted.

---

## 📄 License & Credits

Developed for the **Bangladesh National Land Record & Title Protection Initiative**.
All rights reserved © 2026 JomiGuard.
