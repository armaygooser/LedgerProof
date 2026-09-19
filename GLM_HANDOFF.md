# 智谱 GLM 交接文档：LedgerProof · 财证中枢

> 更新时间：2026-09-20  
> 仓库：`D:\Projects\LedgerProof`  
> 当前接手目标：完成仓库收尾、默认 GHCR 镜像复测、AgentTeams/Element 文件、最终提交和 GitHub 发布准备。

## 1. 先做什么

依次阅读：

1. `README.md`
2. `.agent-handoff/snapshot.md`
3. `.agent-handoff/risks.md`
4. `.agent-handoff/backlog.md`
5. `docs/ARCHITECTURE.md`
6. `docs/CYBERGUARD_RUNTIME_REUSE.md`
7. `docs/DEMO_TRUTH_BOUNDARY.md`

不要重新设计产品。名称、领域、七 Agent 和 UI 路线已经确定并实现。

## 2. 产品目标

LedgerProof 是从 CyberGuard 迁移出的独立金融审计项目。演示案例：对 1,024 笔付款做全量审计，发现三笔各 ¥98,000 的拆分付款，由七个权限隔离 Agent 调查；人类批准止付；CyberGuard 执行并记录哈希链；独立复核 Agent 重查状态；最后可受控回滚并使旧复核结论失效。

核心演示词：**Agent 干活调查，人来审批；每一步有哈希证据链；执行后独立复测；错误动作可回滚。**

## 3. 已完成代码

### 后端

- `backend/ledgerproof_api/dataset.py`：固定种子生成 1,024 笔交易，三笔高风险交易总计 ¥294,000。
- `backend/ledgerproof_api/agents.py`：七 Agent 的角色、权限和确定性调查结果。
- `backend/ledgerproof_api/engine.py`：案件状态机：`detected → investigating/findings_ready → awaiting_approval → approved → executed → verified → rolled_back`。
- `backend/ledgerproof_api/governance.py`：通过 HTTP 调用 CyberGuard 治理容器。
- `backend/ledgerproof_api/app.py`：演示 API。
- `backend/tests/test_demo_flow.py`：完整流程和哈希确定性测试。

### CyberGuard 适配

- `adapter/Dockerfile`：默认 `FROM ghcr.io/elsechord/cyberguard-executor:sha-3b34e4c`。
- `adapter/finance_adapter.py`：导入基础镜像内的 `app.main`，增加金融提案、付款止付、复核和回滚路由；不复制 CyberGuard 的核心审计实现。

### 前端

- `frontend/src/App.tsx`：完整演示流程和人工审批/回滚弹窗。
- `frontend/src/components/`：风险分析、七 Agent、审批工作台、交易表和哈希证据链。
- React 19 + Ant Design 6 + ECharts，金融审计工作台风格。

### 容器和素材

- `compose.yaml`：三个服务，端口 18866/18865/18805。
- `release/ledgerproof-demo.gif`：五段状态循环动图。
- `release/demo-frames/`：异常发现、待审批、已执行、已复核、已回滚五张 1920×1080 截图。
- `scripts/smoke_http.py`：真实 HTTP 端到端流程。

### 文档

- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/CYBERGUARD_RUNTIME_REUSE.md`
- `docs/DEMO_TRUTH_BOUNDARY.md`
- `docs/DEMO_RUNBOOK.md`

## 4. 已验证结果

以下均在 2026-09-20 实际运行通过：

```powershell
.\.venv\Scripts\python.exe -m ruff check backend adapter
# All checks passed

.\.venv\Scripts\python.exe -m pytest
# 2 passed（仅有上游 TestClient 弃用警告）

cd frontend
npm test -- --run
# 1 file / 2 tests passed

npm run build
# 通过；只有 bundle >500 kB 的非阻塞提示
```

容器等价源码验证：

- 已确认镜像标签对应 Git 提交：`3b34e4cd5e332897a59f6ca8862a7174b25e286d`。
- 从本地 `D:\Projects\CyberGuard` 导出该精确提交并按原 Dockerfile 构建：`ledgerproof/cyberguard-executor-dev:3b34e4c`。
- 用 `CYBERGUARD_EXECUTOR_BASE=ledgerproof/cyberguard-executor-dev:3b34e4c` 启动三个容器，全部健康。
- `scripts/smoke_http.py` 通过，最后状态为 `rolled_back`，产生 7 条连续审计记录，链头非空。

当前容器可能仍在运行：

```powershell
docker compose ps
```

## 5. 唯一外部阻塞

默认镜像拉取：

```text
ghcr.io/elsechord/cyberguard-executor:sha-3b34e4c
```

未登录执行 `docker pull` 返回 `unauthorized`，说明 GHCR package 当前不是公开可读。解决方式二选一：

1. 用户在 GitHub Package 设置中把 `cyberguard-executor` 改为 Public；推荐比赛演示使用。
2. `docker login ghcr.io`，使用有 `read:packages` 权限的 token。

解决后必须用默认配置再跑一次：

```powershell
Remove-Item Env:CYBERGUARD_EXECUTOR_BASE -ErrorAction SilentlyContinue
docker compose build --pull cyberguard-governance
docker compose up -d
.\.venv\Scripts\python.exe scripts\smoke_http.py
```

在此之前只能说“同一提交源码等价验证通过”，不能说“GHCR 镜像字节已经验证”。

## 6. 下一步任务，按优先级

### P0 — 完成交付文件

- [ ] 新建 `domainpack/finance-audit.yaml`，描述证据类型、控制规则、动作白名单和复核断言。
- [ ] 参考 `D:\Projects\ProofOps\agentteams\workers.yaml`，创建 LedgerProof 的七个 AgentTeams Worker。
- [ ] 创建三个技能：`financial-audit-observation`、`controlled-payment-action`、`independent-financial-verification`。
- [ ] 创建 `agentteams/ELEMENT_LAUNCH.md` 和 `agentteams/room-message.md`；准确写明 Element 只是从房间链接打开 Service Publishing 地址，不能宣称内嵌 Widget 或 live Agent run。
- [ ] 增加 `docs/adr/0001-financial-audit-domain.md`。
- [ ] 检查 `.gitignore`，加入 `.tmp/` 和 `*.egg-info/`。

### P0 — 清理和最终验证

- [ ] 删除或忽略 `.tmp/`；不要误删其他目录。
- [ ] 检查 `git status --short`，确保没有 `.venv`、`node_modules`、临时 Edge profile 或 Python egg-info 入库。
- [ ] 重新执行后端测试、前端测试/构建、`docker compose config` 和 HTTP smoke。
- [ ] 检查 `release/ledgerproof-demo.gif` 可播放；如果 UI 变更，重新生成素材。
- [ ] 更新所有 `.agent-handoff/*` 和 `progress.md`。
- [ ] 创建首个 Git commit。当前仓库尚未提交，也没有远程地址。

### P1 — 用户提供 GitHub 仓库后

- [ ] 添加 remote 并 push。
- [ ] 若创建 PR，附到当前任务。
- [ ] GitHub README 检查动图、Mermaid 和中文排版。

## 7. 事实边界，不能越过

真实：Docker 容器、HTTP 调用、提案哈希绑定、批准有效期、HMAC 链、动作历史、复核记录、回滚记录、付款模拟状态持久化。

模拟：交易数据、Agent 调查输出、关系图、控制规则、付款通道。当前没有在线大模型、ERP、银行或真实资金冻结。

不要把确定性函数写成“七个在线大模型正在自主运行”。AgentTeams Worker 文件完成后，也必须等真实部署并拿到回执，才能标记 live run。

## 8. 常见问题

- 审计账本在 Docker volume 中持续累积，重置案件不会清空历史，这是设计行为。
- LedgerProof 案件状态当前保存在 API 进程内，API 重启会回到初始案件。
- `scripts/smoke_http.py` 会把当前页面推进到 `rolled_back`；录屏前在页面点击“重置演示案件”。
- 前端 bundle 较大是 ECharts + Ant Design 造成的，比赛演示不阻塞，暂不做拆包优化。
- `.env.example` 中是明确的本地演示值，生产环境必须替换。

## 9. 完成标准

- 默认 GHCR 镜像可以拉取并完成 smoke，或文档明确保留私有阻塞。
- 七 Agent 的 AgentTeams/Element 文件齐全。
- README 动图和快速启动可用。
- 所有检查通过。
- 工作区无临时文件，首个 commit 可审查。
- handoff 文件更新后再结束任务。
