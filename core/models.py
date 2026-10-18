"""
Data models and dataclasses for JomiGuard.
"""
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, Optional, List
from enum import Enum
import json
import re


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


def mask_nid(nid_val: Any) -> str:
    """
    Mask NID number with (*) keeping only the last 3 digits.
    Example: 19852619827361234 -> **************234
    """
    if nid_val is None:
        return "—"
    s = str(nid_val).strip()
    if not s or s in ("—", "None", "nan", "null"):
        return "—"
    if "*" in s:
        return s
    if s.endswith(".0"):
        s = s[:-2]
    if len(s) <= 3:
        return s
    return ("*" * (len(s) - 3)) + s[-3:]


def mask_nids_in_text(text: str) -> str:
    """
    Mask all 10 to 17-digit NID sequences in narrative text with (*), keeping last 3 digits.
    Protects citizen PII in alert explanations, incident logs, and evidence descriptions.
    """
    if not text or not isinstance(text, str):
        return text

    def _repl_explicit(m):
        prefix = m.group(1)
        raw_num = m.group(2)
        masked = mask_nid(raw_num)
        return f"{prefix}{masked}"

    # Handle explicit prefixes like "NID: 1985...", "এনআইডি: ১৯...", "nid: 123..."
    text = re.sub(
        r'((?:NID|এনআইডি|nid)\s*[:：]?\s*)([\d০-৯]{4,22})',
        _repl_explicit,
        text,
        flags=re.IGNORECASE
    )

    def _repl_digits(m):
        digits = m.group(1)
        if len(digits) >= 10:
            return mask_nid(digits)
        return digits

    # Handle standalone 10 to 18 digit sequences (standard NID numbers)
    text = re.sub(r'\b([\d০-৯]{10,18})\b', _repl_digits, text)
    return text
