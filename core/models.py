"""
Data models and dataclasses for JomiGuard.
"""
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, Optional, List
from enum import Enum
import json


class SeverityLevel(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class TriageStatus(str, Enum):
    PENDING = "Pending Review"
    INVESTIGATING = "Under Investigation"
    CLEARED = "Marked Legitimate"
    CONFIRMED = "Confirmed Inconsistency"


@dataclass
class PlotRecord:
    plot_id: str
    mouza: str
    jl_no: int
    khatian_no: str
    dag_no: str
    total_area_decimals: float
    district: str
    upazila: str
    land_type: str
    initial_owner_nid: str
    initial_owner_name: str


@dataclass
class DeedRecord:
    deed_no: str
    plot_id: str
    registration_date: str
    seller_nid: str
    seller_name: str
    buyer_nid: str
    buyer_name: str
    transferred_area_decimals: float
    deed_value_bdt: float
    sub_registry_office: str
    status: str = "Active"


@dataclass
class MutationRecord:
    mutation_case_no: str
    deed_no: str
    plot_id: str
    mutation_date: str
    applicant_nid: str
    applicant_name: str
    mutated_area_decimals: float
    new_khatian_no: str
    ac_land_office: str
    status: str = "Approved"


@dataclass
class AnomalyAlert:
    alert_id: str
    rule_id: str
    rule_name: str
    plot_id: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    title: str
    explanation: str
    trigger_fields: Dict[str, Any]
    evidence: Dict[str, Any]
    triage_status: str = TriageStatus.PENDING.value
    reviewer_notes: str = ""
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def trigger_fields_json(self) -> str:
        return json.dumps(self.trigger_fields, ensure_ascii=False)

    def evidence_json(self) -> str:
        return json.dumps(self.evidence, ensure_ascii=False)
