# 🛡️ JomiGuard — Land Fraud & Double-Selling Alert System

> **Focus:** Data analytics + rule-based anomaly detection for land transactions, deed registrations, and revenue mutation records.

---

## 📌 Executive Summary

Manual verification of land sales and mutation records is prone to oversights, allowing fraudulent actors to execute **double sales**, register **unauthorized area inflations**, or submit **phantom mutations**.

**JomiGuard** is an explainable anomaly detection dashboard that screens land records across Sub-Registry and AC Land revenue offices. It flags conflicting transactions, highlights the specific contradictory fields, maps the complete chronological chain of title, and empowers human officers to make informed administrative determinations.

> ⚠️ **Core Principle**: An alert indicates a *possible inconsistency*, not proven fraud. Repeated identifiers or discrepancies can have legitimate explanations (such as co-owner inheritance partitions or pending court rectifications) and strictly require human administrative review.

---

## 🚀 Key Features

1. **Synthetic Land Dataset & SQLite Engine**:
   - Seeded benchmark containing 41 plots across 8 Mouzas (Gulshan, Badda, Uttara, Mirpur, Dhanmondi, Savar, Tejgaon, Keraniganj).
   - Realistic multi-stage transaction histories with clean baseline chains and planted anomalies.

2. **Rule-Based Anomaly Detection**:
   - `RULE_DOUBLE_SALE`: Conflicting repeated plot sales by the same seller without proof of reacquisition, or cumulative sold area exceeding parcel boundaries.
   - `RULE_AREA_MISMATCH`: Mutated area approved by AC Land office differing from registered deed transferred area (with configurable tolerance >0.02 decimals / >0.5%).
   - `RULE_IDENTITY_MISMATCH`: Mutation applicant name/NID differing from registered deed buyer without power of attorney or inheritance link.
   - `RULE_TEMPORAL_CONFLICT`: Chronological paradox where mutation approval date precedes deed registration date.
   - `RULE_PHANTOM_MUTATION`: Mutation record citing a deed number non-existent in the Sub-Registry repository.
   - `RULE_BROKEN_CHAIN`: Sale executed by an entity with no prior recorded ownership or approved purchase in the chain of title.

3. **Explainable Risk Indicators**:
   - Every alert displays the exact trigger fields (e.g. `deed_transferred_area: 7.50 dec` vs `mutated_area: 12.00 dec` $\rightarrow$ `Discrepancy: +4.50 dec (+60% inflation)`).
   - Side-by-side evidence comparison cards (Deed vs Deed or Deed vs Mutation).
   - Human Triage Workflow: Update status (`Pending Review`, `Under Investigation`, `Marked Legitimate`, `Confirmed Inconsistency`) with auditor notes.

4. **Searchable Plot History & Visual Timeline**:
   - Instant search across Plot IDs, Dag Nos, Khatian Nos, Deed Nos, Owner Names, and NIDs.
   - Interactive Plotly chronological timeline visualizing all genesis records, deed transfers, and mutation approvals.
   - Complete ledger table of all registered deeds and revenue mutations.

5. **Interactive Anomaly Injection Sandbox (Demo Flow)**:
   - 1-click test scenarios to inject a duplicate sale, area inflation, identity mismatch, or chronological paradox.
   - Instant live detection with immediate alert surfacing.
   - 1-click database reset to benchmark state.

6. **Downloadable Audit Reports**:
   - 1-click export of alerts ledger in CSV format.
   - Formatted, printable Land Anomaly Investigation Report in Markdown format with executive metrics and officer sign-off signature blocks.

---

## 🛠️ Technology Stack

- **Language:** Python 3.13+
- **Data Analytics:** Pandas 3.0+
- **Database:** SQLite 3 (with relational integrity and indices)
- **UI & Dashboard:** Streamlit 1.42+
- **Visualizations:** Plotly Express & Plotly Graph Objects
- **Testing:** Pytest

---

## 📦 Quick Start Guide

### 1. Run via Startup Script
```bash
./run.sh
```
This script will automatically configure the virtual environment, install dependencies, and launch the Streamlit app on `http://localhost:8501`.

### 2. Manual Installation
```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Unit Tests
PYTHONPATH=. pytest -v tests/test_detector.py

# Launch Dashboard
PYTHONPATH=. streamlit run app.py
```

---

## 🧪 Demonstration Walkthrough

1. Open `http://localhost:8501` in your browser.
2. In **Dashboard Overview**, inspect the key metrics (41 plots screened, 6 active inconsistencies, severity distribution).
3. In **Alerts & Risk Investigation**, expand `Plot P-201` to view the **Conflicting Double-Selling** alert.
   - Observe the explainable trigger fields showing both conflicting deeds (`REG-2023-7001` and `REG-2023-7002`) executed by the same seller 15 days apart.
   - Inspect the side-by-side deed JSON comparison.
   - Update triage status to `Under Investigation` and add review notes.
4. In **Searchable Plot History**, search for `P-203`.
   - Inspect the Plotly chronological timeline and compare the 7.50 dec deed against the 12.00 dec mutation.
5. In **Interactive Demo & Sandbox**, navigate to "1️⃣ Duplicate Sale Injection".
   - Select a clean plot (e.g., `P-101`), enter a second buyer, and click `🚨 Inject Duplicate Sale Now`.
   - Notice the system immediately detects the conflicting transaction and generates a new Critical alert.
6. In **Downloadable Reports**, download the official Investigation Report (`.md`) and the CSV ledger.

---

## 📁 Repository Structure

```
LandTech/
├── app.py                      # Main Streamlit dashboard application
├── run.sh                      # One-click startup script
├── requirements.txt            # Pinned Python package dependencies
├── README.md                   # System documentation & user guide
├── core/
│   ├── __init__.py
│   ├── db.py                   # SQLite database access & mutation injection layer
│   ├── detector.py             # Rule-based anomaly detection engine
│   ├── models.py               # Dataclasses & typed data models
│   └── reporter.py             # Downloadable CSV & Markdown report generators
├── data/
│   ├── __init__.py
│   ├── schema.sql              # Relational database schema with indices
│   └── generator.py            # Synthetic dataset generator & seeder
└── tests/
    └── test_detector.py        # Pytest test suite for all detection rules
```
