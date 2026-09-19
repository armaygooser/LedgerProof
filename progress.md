# Progress

## 2026-09-20

- Selected product name: LedgerProof · 财证中枢.
- Selected scope: payment audit, suspicious-batch hold, independent verification and reversible release.
- Initialized the independent repository at `D:\Projects\LedgerProof`.
- Implemented the deterministic financial dataset, seven Agent roles, evidence hashing, controls, and case state machine.
- Implemented a finance adapter derived from the CyberGuard Executor application.
- Implemented the Ant Design + ECharts audit console and all demo interactions.
- Added Docker Compose, health checks, HTTP smoke test, backend tests, frontend tests, and CI workflow.
- Passed Ruff, Pytest, frontend tests, frontend production build, Compose config, three-container startup, and the full HTTP flow.
- Generated five 1920×1080 state captures and `release/ledgerproof-demo.gif`.
- Wrote README, architecture, CyberGuard runtime reuse, truth boundary, demo runbook, and GLM handoff documentation.
- Remaining: default GHCR image retest (blocked on package visibility / docker login) and GitHub remote push after the user supplies the repository.
- GLM closeout session (2026-09-20): added `domainpack/finance-audit.yaml`, `agentteams/` workers + skills + Element launch/room materials, `docs/adr/0001-financial-audit-domain.md`; cleaned unreferenced release duplicates and stale docs scaffolding; reran the full check suite (all passing); created the first Git commit.
- GitHub publish session (2026-09-20): created public repo armaygooser/LedgerProof and pushed `main` using the stored GCM credential (secret scan first); fixed the repo description encoding and pointed the README clone URL at the real repo; GHCR package owner turned out to be `elsechord` (a different account), browser parked on the GitHub login page awaiting the user.
