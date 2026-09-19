from __future__ import annotations

import hashlib
import json
from typing import Any

from fastapi.testclient import TestClient
from ledgerproof_api.app import create_app


class FakeGovernance:
    def __init__(self) -> None:
        self.events: list[dict[str, Any]] = []
        self.holds: dict[str, dict[str, Any]] = {}

    def append(self, event: dict[str, Any]) -> dict[str, Any]:
        value = dict(event)
        value["recorded_at"] = f"2026-09-20T00:00:{len(self.events):02d}+00:00"
        value["previous_record_sha256"] = self.events[-1]["record_sha256"] if self.events else None
        canonical = json.dumps(value, sort_keys=True, ensure_ascii=False)
        value["record_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
        value["record_hmac_sha256"] = "f" * 64
        self.events.append(value)
        return value

    async def health(self) -> dict[str, Any]:
        return {"status": "ok", "service": "response-executor", "mode": "simulation"}

    async def propose(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self.append(
            {
                "action_id": "FIN-test-action",
                **payload,
                "risk": "L2",
                "reversible": True,
                "status": "pending_approval",
            }
        )

    async def approve(self, action_id: str, approver: str) -> dict[str, Any]:
        proposal = self.events[0]
        return self.append(
            {
                "action_id": action_id,
                "incident_id": proposal["incident_id"],
                "proposal_record_sha256": proposal["record_sha256"],
                "approver": approver,
                "approval_expires_at": "2026-09-20T01:00:00+00:00",
                "status": "approved",
            }
        )

    async def execute(self, action_id: str) -> dict[str, Any]:
        proposal = self.events[0]
        approval = self.events[1]
        core = self.append(
            {
                "action_id": action_id,
                "incident_id": proposal["incident_id"],
                "action": proposal["action"],
                "target": proposal["target"],
                "approval_record_sha256": approval["record_sha256"],
                "status": "executed",
                "result": "simulated_success",
            }
        )
        hold = {
            "action_id": action_id,
            "target": proposal["target"],
            "status": "HELD",
            "transaction_ids": proposal["transaction_ids"],
            "affected_amount": proposal["affected_amount"],
            "evidence_root_sha256": proposal["evidence_root_sha256"],
        }
        self.holds[proposal["target"]] = hold
        return self.append(
            {
                "action_id": action_id,
                "incident_id": proposal["incident_id"],
                "action": proposal["action"],
                "target": proposal["target"],
                "execution_record_sha256": core["record_sha256"],
                "status": "domain_executed",
                "result": "PAYMENT.HOLD accepted",
            }
        )

    async def record_verification(self, action_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self.append(
            {
                "action_id": action_id,
                "incident_id": self.events[0]["incident_id"],
                "status": "verification_recorded",
                "verification_status": payload["status"],
                **payload,
            }
        )

    async def rollback(self, action_id: str, approver: str, reason: str) -> dict[str, Any]:
        proposal = self.events[0]
        self.holds.pop(proposal["target"], None)
        return self.append(
            {
                "action_id": action_id,
                "incident_id": proposal["incident_id"],
                "action": "release_payment_hold",
                "target": proposal["target"],
                "approver": approver,
                "reason": reason,
                "status": "domain_rolled_back",
                "result": "PAYMENT.RELEASE accepted",
                "invalidates_verification_record_sha256": self.events[-1]["record_sha256"],
            }
        )

    async def action_history(self, action_id: str) -> dict[str, Any]:
        return {"action_id": action_id, "events": [e for e in self.events if e["action_id"] == action_id]}

    async def audit_verify(self) -> dict[str, Any]:
        return {
            "valid": True,
            "records": len(self.events),
            "head": self.events[-1]["record_sha256"] if self.events else None,
        }

    async def finance_state(self, target: str) -> dict[str, Any]:
        return {
            "target": target,
            "hold": self.holds.get(target),
            "population_count": 1024,
            "unaffected_payments": 1021,
        }


def test_complete_governed_payment_hold_and_rollback() -> None:
    governance = FakeGovernance()
    with TestClient(create_app(governance)) as client:
        initial = client.get("/api/demo").json()
        assert initial["phase"] == "detected"
        assert initial["population_count"] == 1024
        assert initial["high_risk_amount"] == 294000

        proposed = client.post("/api/demo/run-to-approval").json()
        assert proposed["phase"] == "awaiting_approval"
        assert proposed["evidence_coverage"] == 100
        assert len(proposed["evidence"]) == 5
        assert [agent["status"] for agent in proposed["agents"][:6]] == ["complete"] * 6
        proposal_hash = proposed["proposal"]["record_sha256"]

        early_execute = client.post("/api/demo/execute")
        assert early_execute.status_code == 409

        approved = client.post("/api/demo/approve", json={"approver": "财务总监 林岚"}).json()
        assert approved["phase"] == "approved"
        assert approved["approval"]["proposal_record_sha256"] == proposal_hash

        executed = client.post("/api/demo/execute").json()
        assert executed["phase"] == "executed"
        assert executed["execution"]["result"] == "PAYMENT.HOLD accepted"

        verified = client.post("/api/demo/verify").json()
        assert verified["phase"] == "verified"
        assert verified["verification"]["valid"] is True
        assert all(verified["verification"]["checks"].values())
        assert verified["agents"][6]["status"] == "verified"

        rolled_back = client.post(
            "/api/demo/rollback",
            json={"approver": "财务总监 林岚", "reason": "调查完成，批准恢复付款流程"},
        ).json()
        assert rolled_back["phase"] == "rolled_back"
        assert rolled_back["verification"]["valid"] is False
        assert rolled_back["verification"]["invalidated_by_rollback"] is True
        assert rolled_back["agents"][6]["status"] == "invalidated"
        assert rolled_back["governance"]["audit_valid"] is True


def test_evidence_hashes_are_deterministic_and_complete() -> None:
    with TestClient(create_app(FakeGovernance())) as first, TestClient(create_app(FakeGovernance())) as second:
        first_state = first.post("/api/demo/investigate").json()
        second_state = second.post("/api/demo/investigate").json()
        first_hashes = {item["evidence_id"]: item["sha256"] for item in first_state["evidence"]}
        second_hashes = {item["evidence_id"]: item["sha256"] for item in second_state["evidence"]}
        assert first_hashes == second_hashes
        assert all(len(value) == 64 for value in first_hashes.values())
