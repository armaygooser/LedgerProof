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

## 2026-09-20（GLM GitHub 发布会话）

- 用户授权使用其 GitHub 账号。机器存储凭据（GCM）为 `armaygooser`（scopes gist/repo/workflow）；`gh` 因缺 `read:org` 无法登录，改用直接 API + GCM 推送。
- 创建公开仓库 https://github.com/armaygooser/LedgerProof 并推送 `main`；密钥扫描通过后才公开。
- 修复仓库描述乱码（PowerShell 5.1 把无 BOM UTF-8 脚本按 ANSI 解析；改用 Python + UTF-8 JSON 重 PATCH）；README 克隆地址替换为真实仓库（`d6056d0`）。
- GHCR 探究：包所有者为 `elsechord`（Peichen Chen，CyberGuard 作者），与 `armaygooser` 不是同一账号；匿名访问包设置页 404。内置浏览器已停在 https://github.com/login 等待用户以 `elsechord` 登录后继续改公开。

## 2026-09-20（GHCR 阻塞解除）

- 用户确认 `elsechord` 是其与 Peichen 共有的组织（API 证实 type=Organization）；包设置页显示组织策略禁止成员改可见性，公开路线交回组织管理员（可选）。
- 用户自行生成 read:packages token 并 `docker login ghcr.io` 成功（token 仅存于本机 Docker 凭据库，未进仓库）。
- 默认镜像验证完成：`docker pull` 成功（digest `sha256:dd4715f6…`）→ `docker compose build --pull` 重建 → `up -d` 三容器健康 → smoke 至 `rolled_back`（case 007，42 条记录）。
- `docs/CYBERGUARD_RUNTIME_REUSE.md` 更新：新增"默认 GHCR 镜像验证（已完成）"章节，保留包仍为私有的换机提示。

## 2026-09-20（审批弹窗溢出修复）

- 用户报告：1280×720 视口下点击"人工批准止付"后弹窗横向超出视口（复现确认：关闭按钮被裁半、输入框溢出、按钮组偏移）。
- 根因：`App.tsx` 审批弹窗 Alert 描述直接渲染完整 64 位 SHA-256 不可断行；`.decision-modal` 为 grid，子项默认 `min-width: auto`，长串把内容列撑出弹窗。
- 修复：哈希改为 `<span className="hash-wrap">` 渲染；CSS 新增 `.decision-modal > * { min-width: 0 }` 与 `.hash-wrap { overflow-wrap: anywhere; word-break: break-all; monospace }`。注意避开了 EvidenceChain 已有的 `.hash-line` 类名（那是三列网格条，混用会再引入布局问题）。
- 验证：前端测试/构建通过；web 容器重建后浏览器复测，弹窗完整居中、哈希两行换行、关闭按钮完整；已关闭弹窗并保持案件在待审批状态。回滚弹窗共用同一 `.decision-modal` 加固，中文描述可自然换行。

## Remaining Operational Work

- None required.
