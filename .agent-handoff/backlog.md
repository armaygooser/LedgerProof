# Task Backlog

## P0

- [x] Add `domainpack/finance-audit.yaml` with evidence, controls, actions, and verification assertions.
- [x] Add seven LedgerProof workers to `agentteams/workers.yaml`.
- [x] Add AgentTeams skills for financial observation, controlled payment action, and independent verification.
- [x] Add `agentteams/ELEMENT_LAUNCH.md` and `agentteams/room-message.md` using the accurate link-out model.
- [x] Add `docs/adr/0001-financial-audit-domain.md`.
- [x] Add `.tmp/` and `*.egg-info/` to `.gitignore`; verified no generated artifacts are tracked.
- [x] Rerun all checks, update handoff, and create the first commit.
- [x] Resolve GHCR access and validate the default `ghcr.io/elsechord/cyberguard-executor:sha-3b34e4c` image（2026-09-20：用户 `docker login ghcr.io`（read:packages）后拉取成功，digest `sha256:dd4715f6…`；默认镜像重建 + 全量 smoke 通过）。

## P1

- [x] Create public repository https://github.com/armaygooser/LedgerProof and push `main`（2026-09-20，GLM session，via stored GCM token）。
- [x] Fix repo description UTF-8 mojibake（PowerShell 5.1 ANSI decode；re-PATCHed via Python）and point README quick-start at the real clone URL。
- [~] ~~Optional: org owner makes the GHCR package public~~（用户决定不需要：2026-09-20 确认"我电脑能跑通即可"，本机已 docker login，无需公开）。
- [ ] Check README animation and Mermaid rendering on GitHub（page renders publicly；gif visual check pending）。
- [ ] Optionally reduce the frontend bundle after the competition demo; current warning is non-blocking.
- [ ] After real AgentTeams Worker deployment with receipts: mark the Element flow as live run and adjust model/runtime.
