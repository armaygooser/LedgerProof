from __future__ import annotations

import hashlib
import json
import random
from datetime import date, timedelta
from typing import Any

from .models import Transaction

SUSPICIOUS_IDS = ["TX-8841-A", "TX-8841-B", "TX-8841-C"]


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def build_transactions() -> list[Transaction]:
    randomizer = random.Random(20260920)
    vendors = [
        ("V-101", "澄海物流", "622202100001"),
        ("V-114", "安岳材料", "622202100002"),
        ("V-128", "青禾科技", "622202100003"),
        ("V-143", "北辰运维", "622202100004"),
        ("V-165", "瑞和设备", "622202100005"),
        ("V-207", "明川咨询", "622202100006"),
    ]
    base = date(2026, 7, 1)
    transactions: list[Transaction] = []
    for index in range(1021):
        vendor_id, vendor_name, account = vendors[index % len(vendors)]
        amount = round(randomizer.uniform(860, 78600), 2)
        submitted = base + timedelta(days=index % 78)
        while submitted.weekday() >= 5:
            submitted += timedelta(days=1)
        triggers: list[str] = []
        risk_score = 8 + (index % 9)
        if index % 53 == 0:
            triggers.append("金额偏离历史均值")
            risk_score += 25
        if index % 89 == 0:
            triggers.append("人工会计分录")
            risk_score += 18
        level = "medium" if risk_score >= 35 else "low"
        transactions.append(
            Transaction(
                transaction_id=f"TX-{index + 1000:05d}",
                invoice_id=f"INV-{index + 2000:05d}",
                vendor_id=vendor_id,
                vendor_name=vendor_name,
                amount=amount,
                submitted_at=f"{submitted.isoformat()} 10:{index % 60:02d}",
                approver="部门负责人",
                payment_account=account,
                risk_score=min(risk_score, 62),
                risk_level=level,
                triggers=triggers,
            )
        )

    for suffix in ("A", "B", "C"):
        transactions.append(
            Transaction(
                transaction_id=f"TX-8841-{suffix}",
                invoice_id="INV-8841",
                vendor_id="V-291",
                vendor_name="华岳设备服务",
                amount=98000.0,
                submitted_at="2026-09-19 22:14",
                approver="财务专员",
                payment_account="622202884129",
                risk_score=95,
                risk_level="high",
                triggers=[
                    "审批阈值拆分",
                    "新供应商大额付款",
                    "周末付款",
                    "关联联系电话",
                    "采购订单金额不一致",
                    "审批路径绕过",
                ],
            )
        )
    return transactions


def relationship_graph() -> dict[str, Any]:
    return {
        "nodes": [
            {"id": "employee-zhang", "name": "采购员 张某", "category": "employee", "risk": 82},
            {"id": "vendor-v291", "name": "华岳设备服务", "category": "vendor", "risk": 95},
            {"id": "account-884129", "name": "账户 6222…4129", "category": "account", "risk": 88},
            {"id": "vendor-v319", "name": "远岚工程", "category": "vendor", "risk": 71},
            {"id": "batch", "name": "PAY-2026-0919", "category": "batch", "risk": 95},
        ],
        "links": [
            {"source": "employee-zhang", "target": "vendor-v291", "label": "相同手机号"},
            {"source": "vendor-v291", "target": "account-884129", "label": "收款账户"},
            {"source": "account-884129", "target": "vendor-v319", "label": "历史共用"},
            {"source": "employee-zhang", "target": "batch", "label": "发起付款"},
            {"source": "vendor-v291", "target": "batch", "label": "¥294,000"},
        ],
    }
