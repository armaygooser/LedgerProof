from __future__ import annotations

from collections.abc import Iterable
from datetime import UTC, datetime

from .dataset import SUSPICIOUS_IDS, canonical_sha256
from .models import AgentRun, EvidenceRecord, Finding, Transaction

AGENT_DEFINITIONS = [
    ("agent-evidence", "证据保全 Agent", "封存输入并生成 Evidence ID", "证据写入；无判断和执行权限", "evidence_sealer"),
    ("agent-reconcile", "账目勾稽 Agent", "核对订单、发票、总账和付款", "证据只读；可写调查结论", "three_way_match"),
    ("agent-anomaly", "异常检测 Agent", "执行全量交易风险评分", "交易只读；可调用确定性评分工具", "transaction_risk_engine"),
    ("agent-graph", "关系穿透 Agent", "调查人员、供应商和账户关系", "脱敏关系只读；无审批权限", "counterparty_graph"),
    ("agent-control", "内控合规 Agent", "检查阈值和职责分离控制", "规则与审批日志只读", "control_tester"),
    ("agent-planner", "处置规划 Agent", "形成最小影响止付提案", "可提案；不能批准或执行", "action_planner"),
    ("agent-verifier", "独立复核 Agent", "独立验证执行状态和审计链", "审计与付款状态只读", "independent_reperformance"),
]


def initial_agents() -> list[AgentRun]:
    return [
        AgentRun(
            agent_id=agent_id,
            sequence=index,
            name=name,
            role=role,
            permission=permission,
            tool=tool,
        )
        for index, (agent_id, name, role, permission, tool) in enumerate(AGENT_DEFINITIONS, 1)
    ]


def mark_agent(agent: AgentRun, summary: str, evidence_ids: Iterable[str], output: object) -> AgentRun:
    now = datetime.now(UTC)
    agent.status = "complete"
    agent.started_at = agent.started_at or now
    agent.completed_at = now
    agent.summary = summary
    agent.input_evidence_ids = list(evidence_ids)
    agent.output_sha256 = canonical_sha256(output)
    return agent


def evidence_agent(transactions: list[Transaction], agent: AgentRun) -> tuple[list[EvidenceRecord], Finding]:
    suspicious = [tx.model_dump() for tx in transactions if tx.transaction_id in SUSPICIOUS_IDS]
    sources = [
        ("EVD-LEDGER-0919", "ledger", "总账与付款批次", "ledger-q3.csv", transactions),
        ("EVD-INVOICE-8841", "invoice", "供应商发票 INV-8841", "invoice-8841.pdf", suspicious),
        ("EVD-PO-3327", "purchase_order", "采购订单 PO-3327", "po-3327.pdf", {"amount": 280000}),
        ("EVD-VENDOR-291", "vendor_master", "供应商主数据 V-291", "vendor-master.json", {"age_days": 7}),
        ("EVD-APPROVAL-772", "approval_log", "付款审批日志", "approval-log.json", {"path": ["张某", "财务专员"]}),
    ]
    evidence = [
        EvidenceRecord(
            evidence_id=evidence_id,
            kind=kind,
            label=label,
            source=source,
            sha256=canonical_sha256(value if not isinstance(value, list) else [v.model_dump() if hasattr(v, "model_dump") else v for v in value]),
        )
        for evidence_id, kind, label, source, value in sources
    ]
    output = {"count": len(evidence), "hashes": [item.sha256 for item in evidence]}
    mark_agent(agent, "5 组审计证据已封存，完整性校验通过", [], output)
    finding = Finding(
        finding_id="FND-EVIDENCE-001",
        agent_id=agent.agent_id,
        title="审计证据已形成完整性基线",
        summary="总账、发票、采购订单、供应商主数据和审批日志均已生成 SHA-256。",
        severity="info",
        evidence_ids=[item.evidence_id for item in evidence],
        output_sha256=agent.output_sha256 or "",
    )
    return evidence, finding


def investigation_findings(agents: list[AgentRun], evidence: list[EvidenceRecord]) -> list[Finding]:
    definitions = [
        (
            agents[1],
            "发现发票拆分与采购订单差异",
            "INV-8841 被拆分为三笔 ¥98,000 付款，累计 ¥294,000；采购订单金额为 ¥280,000。",
            ["重复发票", "三方匹配失败"],
            ["EVD-LEDGER-0919", "EVD-INVOICE-8841", "EVD-PO-3327"],
        ),
        (
            agents[2],
            "三笔交易进入最高风险区间",
            "阈值拆分、新供应商、周末提交、关联信息和审批绕过共同形成 95/100 风险分。",
            ["阈值拆分", "周末付款", "历史偏离"],
            ["EVD-LEDGER-0919", "EVD-INVOICE-8841"],
        ),
        (
            agents[3],
            "供应商与内部人员存在关联信号",
            "供应商联系电话与采购员一致，收款账户还与另一供应商存在历史共用记录。",
            ["关联方", "账户共用"],
            ["EVD-VENDOR-291", "EVD-APPROVAL-772"],
        ),
        (
            agents[4],
            "付款绕过三项关键控制",
            "拆分付款绕过高级审批阈值，新供应商缺少二级复核，申请与审批职责未充分分离。",
            ["CONTROL-SPLIT-002", "CONTROL-VENDOR-007", "CONTROL-SOD-004"],
            ["EVD-APPROVAL-772", "EVD-VENDOR-291", "EVD-LEDGER-0919"],
        ),
    ]
    findings: list[Finding] = []
    for index, (agent, title, summary, controls, used_ids) in enumerate(definitions, 2):
        output = {"title": title, "summary": summary, "controls": controls, "evidence": used_ids}
        mark_agent(agent, summary, used_ids, output)
        findings.append(
            Finding(
                finding_id=f"FND-AUDIT-{index:03d}",
                agent_id=agent.agent_id,
                title=title,
                summary=summary,
                severity="high" if index != 4 else "critical",
                evidence_ids=used_ids,
                control_points=controls,
                output_sha256=agent.output_sha256 or canonical_sha256(output),
            )
        )
    return findings


def plan_action(agent: AgentRun, findings: list[Finding], evidence: list[EvidenceRecord]) -> dict:
    evidence_root = canonical_sha256(sorted(item.sha256 for item in evidence))
    proposal = {
        "action": "hold_payment_batch",
        "target": "PAY-2026-0919",
        "transaction_ids": SUSPICIOUS_IDS,
        "affected_amount": 294000.0,
        "reason": "拆单、关联方、周末付款、订单差异与审批绕过形成组合高风险，建议仅暂停三笔付款。",
        "evidence_ids": sorted({item for finding in findings for item in finding.evidence_ids}),
        "evidence_root_sha256": evidence_root,
        "risk": "L2",
        "reversible": True,
    }
    mark_agent(agent, "形成最小影响止付提案，等待财务负责人审批", proposal["evidence_ids"], proposal)
    return proposal
