---
name: independent-financial-verification
description: 在止付执行后独立复测范围、金额与审计链，并在回滚后作废旧结论。
version: 0.1.0
---

# 独立金融复核

## 验证契约

以下六项必须来自执行后的独立观测（重新读取付款状态与审计链），不能使用执行 Agent 的叙述：

- 目标批次状态为 `HELD`
- 止付交易清单与提案完全一致
- 止付金额与提案完全一致
- 未受影响付款数量 = 总体数量 − 提案笔数
- CyberGuard 审计链从头重算通过
- 执行回执证据根与提案证据根一致

只返回 `VERIFIED`、`FAILED` 或 `INCONCLUSIVE`。输出 `checks[]`、`evidence_ids[]`、观测状态哈希和回滚建议。检测到回滚事件时，旧结论必须标记为 `invalidated`。
