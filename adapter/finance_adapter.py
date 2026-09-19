from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Literal
from uuid import uuid4

from app import main as core
from fastapi import Depends, Header, HTTPException
from pydantic import BaseModel, Field

app = core.app
STATE_FILE = Path(os.getenv("LEDGERPROOF_FINANCE_STATE_FILE", "/data/finance-state.json"))
FINANCE_ACTIONS = {
    "hold_payment_batch": {"risk": "L2", "reversible": True},
}


class FinanceActionRequest(BaseModel):
    incident_id: str = Field(min_length=3, max_length=128)
    action: Literal["hold_payment_batch"]
    target: str = Field(min_length=3, max_length=128)
    reason: str = Field(min_length=10, max_length=2000)
    idempotency_key: str = Field(min_length=8, max_length=128)
    run_id: str = Field(min_length=3, max_length=128)
    model_mode: Literal["unknown", "live", "replay", "deterministic"] = "unknown"
    evidence_root_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    transaction_ids: list[str] = Field(min_length=1, max_length=100)
    affected_amount: float = Field(gt=0)


class FinanceVerificationRequest(BaseModel):
    status: Literal["VERIFIED", "FAILED", "INCONCLUSIVE"]
    checks: dict[str, bool]
    evidence_root_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    observed_state_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    verifier: str = Field(min_length=3, max_length=128)


class FinanceRollbackRequest(BaseModel):
    approver: str = Field(min_length=2, max_length=128)
    reason: str = Field(min_length=6, max_length=300)


def authorize_verifier(authorization: str | None = Header(default=None)) -> None:
    expected = os.getenv("LEDGERPROOF_VERIFIER_TOKEN", "")
    supplied = (authorization or "").removeprefix("Bearer ")
    if not expected or not core.hmac.compare_digest(supplied, expected):
        raise HTTPException(status_code=401, detail="invalid verifier token")


def load_finance_state() -> dict[str, Any]:
    if not STATE_FILE.exists():
        return {"holds": {}}
    try:
        value = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        raise HTTPException(status_code=503, detail="finance state is unreadable") from None
    if not isinstance(value, dict) or not isinstance(value.get("holds"), dict):
        raise HTTPException(status_code=503, detail="finance state is invalid")
    return value


def save_finance_state(value: dict[str, Any]) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    temporary = STATE_FILE.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    os.replace(temporary, STATE_FILE)


def action_events(action_id: str) -> list[dict[str, Any]]:
    return [item for item in core.load_events() if item.get("action_id") == action_id]


def proposal_for(action_id: str) -> dict[str, Any]:
    proposal = next(
        (item for item in action_events(action_id) if item.get("status") == "pending_approval"),
        None,
    )
    if proposal is None:
        raise HTTPException(status_code=404, detail="finance action not found")
    return proposal


@app.post("/finance/actions/propose", dependencies=[Depends(core.authorize)])
def propose_finance_action(request: FinanceActionRequest) -> dict[str, Any]:
    with core.LOCK:
        core.require_valid_audit()
        for event in reversed(core.load_events()):
            if event.get("idempotency_key") == request.idempotency_key:
                if event.get("incident_id") != request.incident_id or event.get("target") != request.target:
                    raise HTTPException(
                        status_code=409,
                        detail="idempotency key is already bound to a different finance proposal",
                    )
                return event
        action_id = f"FIN-{uuid4().hex[:12]}"
        event = {
            "action_id": action_id,
            **request.model_dump(),
            **FINANCE_ACTIONS[request.action],
            "execution_mode": core.execution_mode(),
            "environment": "financial_digital_twin",
            "execution": "simulated",
            "status": "pending_approval",
        }
        core.append_event(event)
        return event


@app.post("/finance/actions/{action_id}/execute", dependencies=[Depends(core.authorize)])
def execute_finance_action(action_id: str) -> dict[str, Any]:
    with core.LOCK:
        existing = next(
            (item for item in reversed(action_events(action_id)) if item.get("status") == "domain_executed"),
            None,
        )
        if existing is not None:
            return existing
        proposal = proposal_for(action_id)
        executed = core.execute(action_id)
        if executed.get("status") != "executed":
            return executed
        state = load_finance_state()
        hold = {
            "action_id": action_id,
            "target": proposal["target"],
            "status": "HELD",
            "transaction_ids": proposal["transaction_ids"],
            "affected_amount": proposal["affected_amount"],
            "evidence_root_sha256": proposal["evidence_root_sha256"],
            "core_execution_record_sha256": executed["record_sha256"],
        }
        state["holds"][proposal["target"]] = hold
        save_finance_state(state)
        event = {
            "action_id": action_id,
            "incident_id": proposal["incident_id"],
            "action": proposal["action"],
            "target": proposal["target"],
            "execution_record_sha256": executed["record_sha256"],
            "status": "domain_executed",
            "result": "PAYMENT.HOLD accepted",
            "finance_receipt": hold,
            "verification_status": "pending",
        }
        core.append_event(event)
        return event


@app.get("/finance/state/{target}", dependencies=[Depends(core.authorize_audit_reader)])
def finance_state(target: str) -> dict[str, Any]:
    hold = load_finance_state()["holds"].get(target)
    proposal = next(
        (
            item
            for item in reversed(core.load_events())
            if item.get("target") == target and item.get("status") == "pending_approval"
        ),
        None,
    )
    affected = len((proposal or {}).get("transaction_ids", []))
    return {
        "target": target,
        "hold": hold,
        "population_count": 1024,
        "unaffected_payments": 1024 - affected,
    }


@app.post(
    "/finance/actions/{action_id}/verification",
    dependencies=[Depends(authorize_verifier)],
)
def record_finance_verification(
    action_id: str, request: FinanceVerificationRequest
) -> dict[str, Any]:
    with core.LOCK:
        core.require_valid_audit()
        existing = next(
            (item for item in reversed(action_events(action_id)) if item.get("status") == "verification_recorded"),
            None,
        )
        if existing is not None:
            return existing
        proposal = proposal_for(action_id)
        domain_execution = next(
            (item for item in action_events(action_id) if item.get("status") == "domain_executed"),
            None,
        )
        if domain_execution is None:
            raise HTTPException(status_code=409, detail="finance action has not been executed")
        if request.evidence_root_sha256 != proposal["evidence_root_sha256"]:
            raise HTTPException(status_code=409, detail="verification evidence root differs from proposal")
        if request.status == "VERIFIED" and not request.checks.get("audit_chain_valid"):
            raise HTTPException(status_code=422, detail="cannot verify an invalid audit chain")
        event = {
            "action_id": action_id,
            "incident_id": proposal["incident_id"],
            "execution_record_sha256": domain_execution["record_sha256"],
            "status": "verification_recorded",
            "verification_status": request.status,
            "checks": request.checks,
            "evidence_root_sha256": request.evidence_root_sha256,
            "observed_state_sha256": request.observed_state_sha256,
            "verifier": request.verifier,
        }
        core.append_event(event)
        return event


@app.post("/finance/actions/{action_id}/rollback", dependencies=[Depends(core.authorize)])
def rollback_finance_action(
    action_id: str,
    request: FinanceRollbackRequest,
    x_approval_secret: str | None = Header(default=None),
) -> dict[str, Any]:
    expected = os.getenv("CYBERGUARD_APPROVAL_SECRET", "")
    if not expected or not core.hmac.compare_digest(x_approval_secret or "", expected):
        raise HTTPException(status_code=403, detail="finance rollback requires human approval secret")
    with core.LOCK:
        existing = next(
            (item for item in reversed(action_events(action_id)) if item.get("status") == "domain_rolled_back"),
            None,
        )
        if existing is not None:
            return existing
        proposal = proposal_for(action_id)
        core_rollback = core.rollback(action_id, x_approval_secret)
        state = load_finance_state()
        state["holds"].pop(proposal["target"], None)
        save_finance_state(state)
        verification = next(
            (item for item in reversed(action_events(action_id)) if item.get("status") == "verification_recorded"),
            None,
        )
        event = {
            "action_id": action_id,
            "incident_id": proposal["incident_id"],
            "action": "release_payment_hold",
            "target": proposal["target"],
            "execution_record_sha256": core_rollback["record_sha256"],
            "status": "domain_rolled_back",
            "result": "PAYMENT.RELEASE accepted",
            "approver": request.approver,
            "reason": request.reason,
        }
        if verification is not None:
            event["invalidates_verification_record_sha256"] = verification["record_sha256"]
        core.append_event(event)
        return event
