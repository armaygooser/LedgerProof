from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

Phase = Literal[
    "detected",
    "investigating",
    "findings_ready",
    "awaiting_approval",
    "approved",
    "executed",
    "verified",
    "rolled_back",
]
AgentStatus = Literal["pending", "running", "complete", "verified", "invalidated"]


class Transaction(BaseModel):
    transaction_id: str
    invoice_id: str
    vendor_id: str
    vendor_name: str
    amount: float
    currency: str = "CNY"
    submitted_at: str
    approver: str
    payment_account: str
    risk_score: int
    risk_level: Literal["high", "medium", "low"]
    triggers: list[str] = Field(default_factory=list)


class EvidenceRecord(BaseModel):
    evidence_id: str
    kind: str
    label: str
    source: str
    sha256: str
    integrity: Literal["verified"] = "verified"


class Finding(BaseModel):
    finding_id: str
    agent_id: str
    title: str
    summary: str
    severity: Literal["critical", "high", "medium", "info"]
    evidence_ids: list[str]
    control_points: list[str] = Field(default_factory=list)
    output_sha256: str


class AgentRun(BaseModel):
    agent_id: str
    sequence: int
    name: str
    role: str
    status: AgentStatus = "pending"
    permission: str
    started_at: datetime | None = None
    completed_at: datetime | None = None
    summary: str = "等待调度"
    tool: str
    input_evidence_ids: list[str] = Field(default_factory=list)
    output_sha256: str | None = None


class GovernanceStatus(BaseModel):
    connected: bool = False
    image: str = "ghcr.io/elsechord/cyberguard-executor:sha-3b34e4c"
    service: str = "response-executor"
    mode: str = "unavailable"
    audit_valid: bool = False
    audit_records: int = 0
    audit_head: str | None = None
    error: str | None = None


class AuditEvent(BaseModel):
    status: str
    record_sha256: str
    previous_record_sha256: str | None = None
    record_hmac_sha256: str | None = None
    recorded_at: str
    action_id: str | None = None
    proposal_record_sha256: str | None = None
    approval_record_sha256: str | None = None
    execution_record_sha256: str | None = None
    detail: dict[str, Any] = Field(default_factory=dict)


class DemoState(BaseModel):
    case_id: str
    phase: Phase
    title: str
    company: str
    period: str
    materiality: float
    population_count: int
    total_amount: float
    high_risk_count: int
    high_risk_amount: float
    medium_risk_count: int
    evidence_coverage: float
    transactions: list[Transaction]
    evidence: list[EvidenceRecord]
    findings: list[Finding]
    agents: list[AgentRun]
    relationship_graph: dict[str, Any]
    control_points: list[dict[str, Any]]
    proposal: dict[str, Any] | None = None
    approval: dict[str, Any] | None = None
    execution: dict[str, Any] | None = None
    verification: dict[str, Any] | None = None
    rollback: dict[str, Any] | None = None
    audit_events: list[AuditEvent] = Field(default_factory=list)
    governance: GovernanceStatus = Field(default_factory=GovernanceStatus)


class ApprovalInput(BaseModel):
    approver: str = Field(min_length=2, max_length=80)


class RollbackInput(BaseModel):
    approver: str = Field(min_length=2, max_length=80)
    reason: str = Field(min_length=6, max_length=300)
