# LedgerProof implementation plan

## Goal

Build a runnable financial audit agent console that uses the CyberGuard Executor GHCR image at runtime for proposal-bound approval, HMAC audit records, controlled execution and rollback.

## Current Phase

Phase 5 — publication and handoff. Core implementation is complete.

## Phases

### Phase 0 — Project initialization
**Status:** complete
- [x] Create independent repository structure and baseline documentation.
- [x] Create persistent plan, findings and progress files.
- [x] Bootstrap Codex, Claude and GLM handoff files.

### Phase 1 — CyberGuard governance adapter
**Status:** complete
- [x] Build a thin derived image from the CyberGuard Executor.
- [x] Add finance proposal, execution receipt, verification and rollback routes.
- [x] Keep CyberGuard approval, hash, HMAC, expiry and audit verification logic unchanged.

### Phase 2 — Financial audit backend
**Status:** complete
- [x] Implement deterministic payment dataset and risk controls.
- [x] Implement seven role-scoped audit agents and case state machine.
- [x] Integrate the backend with the CyberGuard adapter over HTTP.
- [x] Add meaningful end-to-end backend tests.

### Phase 3 — Ant Design audit console
**Status:** complete
- [x] Implement the professional financial audit workspace.
- [x] Add risk analytics, Agent activity, approval and evidence-chain views.
- [x] Implement approve, execute, verify, rollback and reset interactions.

### Phase 4 — Packaging and runtime validation
**Status:** complete_with_external_caveat
- [x] Add Docker Compose, health checks and isolated networking.
- [x] Build frontend and backend containers.
- [x] Run full scenario smoke test against the exact CyberGuard source commit.
- [ ] Rerun against the default GHCR image after registry access is available.

### Phase 5 — Publication and handoff
**Status:** in_progress
- [x] Complete README, architecture, demo truth boundary and recording runbook.
- [x] Update durable handoff state for GLM continuation.
- [x] Generate demo screenshots and animation.
- [ ] Complete domainpack and AgentTeams/Element files.
- [ ] Clean generated files, run final checks, and create a baseline commit.

## Decisions

| Date | Decision | Reason |
|---|---|---|
| 2026-09-20 | Product name is LedgerProof · 财证中枢. | Connects ledger evidence with verifiable decisions and fits the ProofOps naming family. |
| 2026-09-20 | Use payment audit and reversible payment hold as the single demo. | Strong fit for evidence, human approval, independent verification and rollback. |
| 2026-09-20 | Reuse CyberGuard by deriving from its executor image. | Provides runtime reuse without relabeling security actions as financial actions. |
| 2026-09-20 | Keep the first Agent behavior deterministic and truthfully labeled. | Makes the one-day demo reproducible and leaves a clear path to AgentTeams live workers. |

## Errors

| Date | Error | Resolution |
|---|---|---|
| 2026-09-20 | GHCR executor pull returned `unauthorized`. | Built exact commit `3b34e4c` locally for equivalent validation; actual image verification remains pending. |
| 2026-09-20 | Windows computer-use helper failed to initialize twice. | Used headless Edge with isolated profiles for visual captures. |
