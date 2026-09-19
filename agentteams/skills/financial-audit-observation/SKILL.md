---
name: financial-audit-observation
description: 以只读权限调查总账、发票、订单、供应商与审批日志，输出可解析的 Evidence ID 引用。
version: 0.1.0
---

# 金融审计只读调查

## 安全边界

- 只读取本次 `run_id` 的总账、发票、采购订单、供应商主数据、审批日志与脱敏关系图。
- 不调用止付或释放端点，不生成审批，不把其他 Agent 的叙述当作账务事实。
- 工具未返回 Evidence ID 时只能输出 `PARTIAL` 或 `BLOCKED`。
- 对照 `domainpack/finance-audit.yaml` 的控制规则输出命中编号，不得改写规则。

## 输出

返回 `status`、`finding`、`evidence_ids[]`、`counter_evidence[]`、`unknowns[]` 与 `recommended_next_read`。所有结论必须能回溯到证据哈希。
