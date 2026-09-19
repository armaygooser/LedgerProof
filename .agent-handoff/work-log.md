# Current Work Log

## 2026-09-20

- Initialized independent Git repository at `D:\Projects\LedgerProof`.
- Implemented deterministic 1,024-transaction audit dataset and seven role-scoped Agent workflow.
- Implemented case state machine from detection through approval, execution, verification, and rollback.
- Added thin finance adapter on top of the CyberGuard Executor application.
- Built Ant Design + ECharts financial audit console with human decision gate, runtime status, hash chain, and rollback UI.
- Added three-service Docker Compose runtime and HTTP smoke script.
- Confirmed CyberGuard image tag maps to commit `3b34e4cd5e332897a59f6ca8862a7174b25e286d`.
- Built the exact commit locally as `ledgerproof/cyberguard-executor-dev:3b34e4c` because unauthenticated GHCR pull failed.
- Ran full container flow successfully; final state `rolled_back`, seven audit records.
- Generated five state screenshots and `release/ledgerproof-demo.gif`.
- Replaced the placeholder README and added architecture, runtime reuse, truth boundary, and demo runbook documents.
- Created `GLM_HANDOFF.md` with remaining work and exact commands.

## 2026-09-20（GLM 收尾会话）

- Added `domainpack/finance-audit.yaml`（evidence types、control rules、action whitelist、six verification assertions，全部对齐 `engine.py`/`agents.py`/`finance_adapter.py` 实测值）。
- Added `agentteams/workers.yaml` with the seven LedgerProof workers（model/runtime 沿用 ProofOps 参考，标注部署前需调整；明示非 live run）。
- Added three AgentTeams skills：`financial-audit-observation`、`controlled-payment-action`、`independent-financial-verification`。
- Added `agentteams/ELEMENT_LAUNCH.md` 与 `agentteams/room-message.md`（准确声明 Element 仅经房间链接打开 Service Publishing 地址）。
- Added `docs/adr/0001-financial-audit-domain.md`。
- Cleanup: removed unreferenced `release/ledgerproof-dashboard.{jpg,png}` and duplicate `release/demo-frames/02-awaiting-approval.jpg`; removed stale scaffolding dirs `docs/progress/`, `docs/reports/`, `docs/standards/`, `docs/templates/`（内容与现状矛盾）。`.gitignore` 已含 `.tmp/` 与 `*.egg-info/`，`.tmp/` 保留在磁盘上但保持未跟踪（用于重建等价源码镜像）。
- Reran full validation（ruff、pytest、前端测试/构建、compose config、容器 smoke、GIF 帧校验）；default GHCR pull 仍 `unauthorized`，阻塞保留。
- Created the first Git commit.

## Remaining Operational Work

- After GHCR access is available: rerun default-image build and smoke（`docker compose build --pull cyberguard-governance`）。
- After the user supplies the GitHub repository URL: add remote, push, and check README rendering.
