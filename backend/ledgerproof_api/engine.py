from __future__ import annotations

from datetime import UTC, datetime

from fastapi import HTTPException

from .agents import evidence_agent, initial_agents, investigation_findings, mark_agent, plan_action
from .dataset import build_transactions, canonical_sha256, relationship_graph
from .governance import GovernanceError, GovernancePort
from .models import AuditEvent, DemoState, GovernanceStatus


class DemoEngine:
    def __init__(self, governance: GovernancePort) -> None:
        self.governance = governance
        self.generation = 1
        self.state = self._new_state()

    def _new_state(self) -> DemoState:
        transactions = build_transactions()
        high = [tx for tx in transactions if tx.risk_level == "high"]
        medium = [tx for tx in transactions if tx.risk_level == "medium"]
        return DemoState(
            case_id=f"FIN-2026-0919-{self.generation:03d}",
            phase="detected",
            title="PAY-2026-0919 异常付款审计",
            company="华岳集团",
            period="2026 Q3",
            materiality=100000.0,
            population_count=len(transactions),
            total_amount=round(sum(tx.amount for tx in transactions), 2),
            high_risk_count=len(high),
            high_risk_amount=round(sum(tx.amount for tx in high), 2),
            medium_risk_count=len(medium),
            evidence_coverage=0.0,
            transactions=transactions,
            evidence=[],
            findings=[],
            agents=initial_agents(),
            relationship_graph=relationship_graph(),
            control_points=[
                {"name": "审批阈值拆分", "score": 30, "severity": "critical"},
                {"name": "新供应商大额付款", "score": 20, "severity": "high"},
                {"name": "关联联系电话", "score": 20, "severity": "high"},
                {"name": "订单金额不一致", "score": 15, "severity": "high"},
                {"name": "审批路径绕过", "score": 15, "severity": "high"},
                {"name": "周末付款", "score": 10, "severity": "medium"},
            ],
        )

    def require_phase(self, *allowed: str) -> None:
        if self.state.phase not in allowed:
            raise HTTPException(
                status_code=409,
                detail=f"phase {self.state.phase} does not allow this operation; expected {allowed}",
            )

    async def refresh_governance(self) -> None:
        try:
            health = await self.governance.health()
            audit = await self.governance.audit_verify()
            self.state.governance = GovernanceStatus(
                connected=True,
                mode=health.get("mode", "unknown"),
                service=health.get("service", "response-executor"),
                audit_valid=bool(audit.get("valid")),
                audit_records=int(audit.get("records", 0)),
                audit_head=audit.get("head"),
            )
        except GovernanceError as exc:
            self.state.governance = GovernanceStatus(error=str(exc))

    async def sync_action_history(self) -> None:
        if not self.state.proposal:
            return
        history = await self.governance.action_history(self.state.proposal["action_id"])
        events: list[AuditEvent] = []
        for item in history.get("events", []):
            events.append(
                AuditEvent(
                    status=item.get("status", "unknown"),
                    record_sha256=item.get("record_sha256", ""),
                    previous_record_sha256=item.get("previous_record_sha256"),
                    record_hmac_sha256=item.get("record_hmac_sha256"),
                    recorded_at=item.get("recorded_at", ""),
                    action_id=item.get("action_id"),
                    proposal_record_sha256=item.get("proposal_record_sha256"),
                    approval_record_sha256=item.get("approval_record_sha256"),
                    execution_record_sha256=item.get("execution_record_sha256"),
                    detail={
                        key: item[key]
                        for key in (
                            "action",
                            "target",
                            "result",
                            "approver",
                            "verification_status",
                            "evidence_root_sha256",
                            "invalidates_verification_record_sha256",
                        )
                        if key in item
                    },
                )
            )
        self.state.audit_events = events
        await self.refresh_governance()

    async def snapshot(self) -> DemoState:
        await self.refresh_governance()
        return self.state

    async def investigate(self) -> DemoState:
        self.require_phase("detected")
        self.state.phase = "investigating"
        self.state.agents[0].status = "running"
        self.state.agents[0].started_at = datetime.now(UTC)
        evidence, evidence_finding = evidence_agent(self.state.transactions, self.state.agents[0])
        self.state.evidence = evidence
        self.state.evidence_coverage = 100.0
        self.state.findings = [evidence_finding]
        for agent in self.state.agents[1:5]:
            agent.status = "running"
            agent.started_at = datetime.now(UTC)
        self.state.findings.extend(investigation_findings(self.state.agents, evidence))
        self.state.phase = "findings_ready"
        return self.state

    async def propose(self) -> DemoState:
        self.require_phase("findings_ready")
        self.state.agents[5].status = "running"
        self.state.agents[5].started_at = datetime.now(UTC)
        proposal = plan_action(self.state.agents[5], self.state.findings, self.state.evidence)
        remote = await self.governance.propose(
            {
                "incident_id": self.state.case_id,
                "action": proposal["action"],
                "target": proposal["target"],
                "reason": proposal["reason"],
                "idempotency_key": f"{self.state.case_id}-payment-hold",
                "run_id": self.state.case_id,
                "model_mode": "deterministic",
                "evidence_root_sha256": proposal["evidence_root_sha256"],
                "transaction_ids": proposal["transaction_ids"],
                "affected_amount": proposal["affected_amount"],
            }
        )
        self.state.proposal = {**proposal, **remote}
        self.state.phase = "awaiting_approval"
        await self.sync_action_history()
        return self.state

    async def approve(self, approver: str) -> DemoState:
        self.require_phase("awaiting_approval")
        assert self.state.proposal is not None
        approval = await self.governance.approve(self.state.proposal["action_id"], approver)
        self.state.approval = approval
        self.state.phase = "approved"
        await self.sync_action_history()
        return self.state

    async def execute(self) -> DemoState:
        self.require_phase("approved")
        assert self.state.proposal is not None
        result = await self.governance.execute(self.state.proposal["action_id"])
        self.state.execution = result
        self.state.phase = "executed"
        await self.sync_action_history()
        return self.state

    async def verify(self) -> DemoState:
        self.require_phase("executed")
        assert self.state.proposal is not None
        action_id = self.state.proposal["action_id"]
        finance_state = await self.governance.finance_state(self.state.proposal["target"])
        audit = await self.governance.audit_verify()
        hold = finance_state.get("hold") or {}
        checks = {
            "target_held": hold.get("status") == "HELD",
            "transaction_scope_exact": sorted(hold.get("transaction_ids", []))
            == sorted(self.state.proposal["transaction_ids"]),
            "affected_amount_exact": float(hold.get("affected_amount", 0))
            == float(self.state.proposal["affected_amount"]),
            "unaffected_payments_released": finance_state.get("unaffected_payments", 0)
            == self.state.population_count - len(self.state.proposal["transaction_ids"]),
            "audit_chain_valid": bool(audit.get("valid")),
            "evidence_root_matches": hold.get("evidence_root_sha256")
            == self.state.proposal["evidence_root_sha256"],
        }
        verified = all(checks.values())
        payload = {
            "status": "VERIFIED" if verified else "FAILED",
            "checks": checks,
            "evidence_root_sha256": self.state.proposal["evidence_root_sha256"],
            "observed_state_sha256": canonical_sha256(finance_state),
            "verifier": "agent-verifier",
        }
        remote = await self.governance.record_verification(action_id, payload)
        self.state.verification = {**payload, **remote, "valid": verified}
        verifier = self.state.agents[6]
        mark_agent(
            verifier,
            "止付范围、金额、证据根和 CyberGuard 审计链均已独立复核" if verified else "独立复核失败",
            [item.evidence_id for item in self.state.evidence],
            payload,
        )
        verifier.status = "verified" if verified else "complete"
        self.state.phase = "verified" if verified else "executed"
        await self.sync_action_history()
        return self.state

    async def rollback(self, approver: str, reason: str) -> DemoState:
        self.require_phase("executed", "verified")
        assert self.state.proposal is not None
        result = await self.governance.rollback(self.state.proposal["action_id"], approver, reason)
        self.state.rollback = result
        if self.state.verification:
            self.state.verification["valid"] = False
            self.state.verification["invalidated_by_rollback"] = True
            self.state.agents[6].status = "invalidated"
            self.state.agents[6].summary = "原复核结论因回滚而失效，需重新复核"
        self.state.phase = "rolled_back"
        await self.sync_action_history()
        return self.state

    async def reset(self) -> DemoState:
        self.generation += 1
        self.state = self._new_state()
        await self.refresh_governance()
        return self.state
