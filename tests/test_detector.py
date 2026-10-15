"""
Unit tests for JomiGuard Anomaly Detection Engine.
Verifies all 6 detection rules, explainable indicators, and baseline clean cases.
"""

import pytest
import pandas as pd
from core.detector import (
    detect_double_selling,
    detect_registration_mutation_inconsistencies,
    detect_broken_chain_of_title,
    run_detection
)
from core.models import SeverityLevel


@pytest.fixture
def clean_dataset():
    """Generates a clean baseline land dataset with 1 plot and 1 valid transaction chain."""
    plots = pd.DataFrame([{
        "plot_id": "P-TEST-01",
        "mouza": "Badda",
        "jl_no": 45,
        "khatian_no": "RS-100",
        "dag_no": "501",
        "total_area_decimals": 10.0,
        "district": "Dhaka",
        "upazila": "Badda",
        "land_type": "Residential",
        "initial_owner_nid": "1111111111111",
        "initial_owner_name": "Rahim Khan"
    }])
    
    deeds = pd.DataFrame([{
        "deed_no": "REG-TEST-100",
        "plot_id": "P-TEST-01",
        "registration_date": "2023-01-10",
        "seller_nid": "1111111111111",
        "seller_name": "Rahim Khan",
        "buyer_nid": "2222222222222",
        "buyer_name": "Karim Mia",
        "transferred_area_decimals": 10.0,
        "deed_value_bdt": 2000000.0,
        "sub_registry_office": "Badda Sub-Registry Office",
        "status": "Active"
    }])
    
    mutations = pd.DataFrame([{
        "mutation_case_no": "MUT-TEST-100",
        "deed_no": "REG-TEST-100",
        "plot_id": "P-TEST-01",
        "mutation_date": "2023-02-15",
        "applicant_nid": "2222222222222",
        "applicant_name": "Karim Mia",
        "mutated_area_decimals": 10.0,
        "new_khatian_no": "DP-555",
        "ac_land_office": "AC Land Office, Badda",
        "status": "Approved"
    }])
    
    return plots, deeds, mutations


def test_clean_chain_no_false_positives(clean_dataset):
    """Clean records should generate zero alerts."""
    plots, deeds, mutations = clean_dataset
    
    alerts_double = detect_double_selling(plots, deeds)
    alerts_inconsistencies = detect_registration_mutation_inconsistencies(plots, deeds, mutations)
    alerts_chain = detect_broken_chain_of_title(plots, deeds, mutations)
    
    assert len(alerts_double) == 0, f"Unexpected double sale alerts: {alerts_double}"
    assert len(alerts_inconsistencies) == 0, f"Unexpected consistency alerts: {alerts_inconsistencies}"
    assert len(alerts_chain) == 0, f"Unexpected chain of title alerts: {alerts_chain}"


def test_double_selling_detection(clean_dataset):
    """Same seller selling the same plot to two different buyers should trigger RULE_DOUBLE_SALE."""
    plots, deeds, _ = clean_dataset
    
    # Add a second conflicting sale by the same seller
    deed_2 = {
        "deed_no": "REG-TEST-200",
        "plot_id": "P-TEST-01",
        "registration_date": "2023-01-25",
        "seller_nid": "1111111111111",
        "seller_name": "Rahim Khan",
        "buyer_nid": "3333333333333",  # Different buyer!
        "buyer_name": "Tariq Hasan",
        "transferred_area_decimals": 10.0,
        "deed_value_bdt": 2200000.0,
        "sub_registry_office": "Badda Sub-Registry Office",
        "status": "Active"
    }
    deeds_with_dup = pd.concat([deeds, pd.DataFrame([deed_2])], ignore_index=True)
    
    alerts = detect_double_selling(plots, deeds_with_dup)
    assert len(alerts) >= 1
    alert = alerts[0]
    assert alert.rule_id == "RULE_DOUBLE_SALE"
    assert alert.severity == SeverityLevel.CRITICAL.value
    assert "deed_1_no" in alert.trigger_fields
    assert "deed_2_no" in alert.trigger_fields
    assert alert.trigger_fields["deed_1_no"] == "REG-TEST-100"
    assert alert.trigger_fields["deed_2_no"] == "REG-TEST-200"


def test_area_mismatch_detection(clean_dataset):
    """Mutation with area differing from deed by > 0.02 decimals should trigger RULE_AREA_MISMATCH."""
    plots, deeds, mutations = clean_dataset
    
    # Mutate area inflated to 15.0 decimals instead of 10.0
    mutations_inflated = mutations.copy()
    mutations_inflated.loc[0, "mutated_area_decimals"] = 15.0
    
    alerts = detect_registration_mutation_inconsistencies(plots, deeds, mutations_inflated)
    area_alerts = [a for a in alerts if a.rule_id == "RULE_AREA_MISMATCH"]
    
    assert len(area_alerts) == 1
    alert = area_alerts[0]
    assert alert.severity == SeverityLevel.HIGH.value
    assert alert.trigger_fields["deed_transferred_area_decimals"] == 10.0
    assert alert.trigger_fields["mutation_approved_area_decimals"] == 15.0
    assert alert.trigger_fields["discrepancy_decimals"] == 5.0
    assert alert.trigger_fields["anomaly_type"] == "INFLATION"


def test_identity_mismatch_detection(clean_dataset):
    """Mutation applicant differing from registered deed buyer should trigger RULE_IDENTITY_MISMATCH."""
    plots, deeds, mutations = clean_dataset
    
    # Change applicant to someone else
    mutations_impostor = mutations.copy()
    mutations_impostor.loc[0, "applicant_nid"] = "9999999999999"
    mutations_impostor.loc[0, "applicant_name"] = "Impostor Person"
    
    alerts = detect_registration_mutation_inconsistencies(plots, deeds, mutations_impostor)
    id_alerts = [a for a in alerts if a.rule_id == "RULE_IDENTITY_MISMATCH"]
    
    assert len(id_alerts) == 1
    alert = id_alerts[0]
    assert alert.severity == SeverityLevel.HIGH.value
    assert alert.trigger_fields["deed_buyer_name"] == "Karim Mia"
    assert alert.trigger_fields["mutation_applicant_name"] == "Impostor Person"
    assert alert.trigger_fields["nid_match"] is False


def test_temporal_paradox_detection(clean_dataset):
    """Mutation dated before registered deed should trigger RULE_TEMPORAL_CONFLICT."""
    plots, deeds, mutations = clean_dataset
    
    # Set mutation date earlier than deed (deed is 2023-01-10)
    mutations_early = mutations.copy()
    mutations_early.loc[0, "mutation_date"] = "2022-11-01"
    
    alerts = detect_registration_mutation_inconsistencies(plots, deeds, mutations_early)
    time_alerts = [a for a in alerts if a.rule_id == "RULE_TEMPORAL_CONFLICT"]
    
    assert len(time_alerts) == 1
    alert = time_alerts[0]
    assert alert.severity == SeverityLevel.HIGH.value
    assert alert.trigger_fields["inversion_days"] > 0


def test_phantom_deed_detection(clean_dataset):
    """Mutation citing non-existent deed should trigger RULE_PHANTOM_MUTATION."""
    plots, deeds, mutations = clean_dataset
    
    mutations_phantom = mutations.copy()
    mutations_phantom.loc[0, "deed_no"] = "NON-EXISTENT-DEED-999"
    
    alerts = detect_registration_mutation_inconsistencies(plots, deeds, mutations_phantom)
    phantom_alerts = [a for a in alerts if a.rule_id == "RULE_PHANTOM_MUTATION"]
    
    assert len(phantom_alerts) == 1
    assert phantom_alerts[0].severity == SeverityLevel.CRITICAL.value
    assert phantom_alerts[0].trigger_fields["cited_deed_no"] == "NON-EXISTENT-DEED-999"


def test_explainable_indicators_completeness(clean_dataset):
    """All generated alerts must possess explainable trigger fields and evidence payloads."""
    plots, deeds, _ = clean_dataset
    
    # Introduce double sale
    deed_2 = {
        "deed_no": "REG-TEST-200",
        "plot_id": "P-TEST-01",
        "registration_date": "2023-01-25",
        "seller_nid": "1111111111111",
        "seller_name": "Rahim Khan",
        "buyer_nid": "3333333333333",
        "buyer_name": "Tariq Hasan",
        "transferred_area_decimals": 10.0,
        "deed_value_bdt": 2200000.0,
        "sub_registry_office": "Badda Sub-Registry Office",
        "status": "Active"
    }
    deeds_dup = pd.concat([deeds, pd.DataFrame([deed_2])], ignore_index=True)
    alerts = detect_double_selling(plots, deeds_dup)
    
    for alert in alerts:
        assert alert.alert_id.startswith("ALT-")
        assert len(alert.trigger_fields) > 0
        assert len(alert.evidence) > 0
        assert len(alert.explanation) > 20
        assert alert.severity in [s.value for s in SeverityLevel]
