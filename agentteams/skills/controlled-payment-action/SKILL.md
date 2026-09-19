---
name: controlled-payment-action
description: 形成并执行绑定证据根、人类审批和回滚通道的金融白名单动作。
version: 0.1.0
---

# 受控付款动作

## 强制流程

1. 验证 `run_id`、Evidence ID 与动作白名单（当前仅 `hold_payment_batch`）。
2. 固定 `action`、`target`、`transaction_ids`、`affected_amount`、理由、证据根哈希和复核契约；止付范围必须是最小影响集。
3. L2 提案暂停等待人类批准；Agent 不得获得审批密钥，不得自行批准。
4. 执行前核对批准记录与提案 SHA-256 完全一致且未过期（15 分钟有效期）。
5. 只返回真实 Action ID、领域回执、审计哈希；释放必须走人工回滚通道并使旧复核失效。

任何不一致均输出 `BLOCKED`，不得替换相近目标或扩大止付范围。
