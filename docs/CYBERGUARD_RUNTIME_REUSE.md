# CyberGuard 运行时复用

## 基础镜像

LedgerProof 默认从以下 CyberGuard Executor 镜像构建金融治理容器：

```text
ghcr.io/elsechord/cyberguard-executor:sha-3b34e4c
```

该标签对应源码提交：

```text
3b34e4cd5e332897a59f6ca8862a7174b25e286d
```

`adapter/Dockerfile` 以它为 `FROM`，只复制 `finance_adapter.py`。适配器导入镜像内原始 `app.main`，继续使用 CyberGuard 的事件追加、批准、动作历史、审计校验和回滚逻辑。

## 为什么需要适配层

CyberGuard 原执行器的动作白名单是网络安全动作。直接把 `block_ioc` 改名成“暂停付款”会形成虚假复用。LedgerProof 增加 `hold_payment_batch`，把同一套治理协议映射到真实的金融领域状态：

- proposal：批次、三笔交易、金额、理由、证据根；
- execute：写入 `HELD` 状态并返回领域执行回执；
- verify：记录独立复核的六项断言；
- rollback：把批次恢复为 `RELEASED`，并关联失效的复核记录。

## 调用路径

| LedgerProof 操作 | CyberGuard / adapter API |
|---|---|
| 创建止付提案 | `POST /finance/actions/propose` |
| 人工批准 | `POST /actions/approve` |
| 执行止付 | `POST /finance/actions/{id}/execute` |
| 查询付款状态 | `GET /finance/state/{target}` |
| 记录独立复核 | `POST /finance/actions/{id}/verification` |
| 受控回滚 | `POST /finance/actions/{id}/rollback` |
| 读取动作历史 | `GET /actions/{id}` |
| 校验全局审计链 | `GET /audit/verify` |

## GHCR 使用

公开包无需登录：

```bash
docker compose up --build
```

私有包需要具有 `read:packages` 权限的 GitHub token：

```bash
echo "$GHCR_TOKEN" | docker login ghcr.io -u <github-user> --password-stdin
docker compose up --build
```

比赛演示建议将 `cyberguard-executor` package 设为 Public，避免换机时受登录状态影响。

## 本次等价源码验证

2026-09-20，GHCR 未登录拉取返回 `unauthorized`。为不中断集成验证，我们从本地 CyberGuard Git 对象导出精确提交 `3b34e4c`，使用该提交自带的 `services/response-executor/Dockerfile` 构建：

```text
ledgerproof/cyberguard-executor-dev:3b34e4c
```

随后通过构建参数替换基础镜像：

```powershell
$env:CYBERGUARD_EXECUTOR_BASE='ledgerproof/cyberguard-executor-dev:3b34e4c'
docker compose up --build
```

这验证了同一提交源码与 LedgerProof 适配层的兼容性。

## 默认 GHCR 镜像验证（已完成）

同日稍后，使用具有 `read:packages` 权限的 token 执行 `docker login ghcr.io` 后，默认镜像链路完成真实验证：

```text
ghcr.io/elsechord/cyberguard-executor:sha-3b34e4c
digest: sha256:dd4715f6bd2eed0d806b75d16ca1cb97e7534ab2f0ecefa8ba7faa3ae7162845
```

`docker compose build --pull cyberguard-governance` 以该镜像为 `FROM` 重建金融治理容器，三个容器健康，`scripts/smoke_http.py` 完整跑至 `rolled_back`。

注意：该 package 在组织中仍为私有（组织策略禁止成员改公开）。未登录机器拉取仍会返回 `unauthorized`，换演示机前需要先 `docker login ghcr.io`，或由组织管理员放开公开策略。

## 运行时边界

- `ledgerproof-api` 不直接访问 CyberGuard 数据文件，只通过 HTTP 使用治理能力。
- 审批密钥、执行 token、审计读取 token 和复核 token 分开配置。
- 默认凭据只用于本地演示，正式环境必须通过 secret manager 注入。
- 付款状态为隔离模拟，不连接银行或真实 ERP。
