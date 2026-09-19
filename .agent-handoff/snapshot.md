# Handoff Snapshot

## Current State

- Last updated: 2026-09-20
- Last agent: GLM（收尾会话）
- Workspace root: `D:\Projects\LedgerProof`
- Current objective: Finish and publish a runnable CyberGuard-based financial audit migration demo.
- Current status: **All P0 complete.** Default GHCR image validated with authenticated pull（digest `sha256:dd4715f6…`），default-image stack rebuilt，three containers healthy，full smoke to `rolled_back`（case 007，42 records）. Repo published at https://github.com/armaygooser/LedgerProof.
- Immediate next actions:
  1. Optional: org admin makes the GHCR package public（org policy currently forbids member visibility changes）so demo machines need no login.
  2. Optional: visual check of README gif/Mermaid on GitHub.
- Active files:
  - `docs/CYBERGUARD_RUNTIME_REUSE.md`（updated with registry validation）
  - `domainpack/finance-audit.yaml`、`agentteams/`、`docs/adr/0001-financial-audit-domain.md`
- Blockers: none. GHCR access resolved via user's `docker login ghcr.io`（read:packages token，stored only in Docker credential store，not in repo）.
- Open questions:
  - Final demo machine's AgentTeams model/runtime; workers.yaml currently mirrors the ProofOps reference（`deepseek-v4-flash` / `copaw`）。
  - Whether/when to make the GHCR package public（needs org owner；package remains private today）.

## Recovery Summary

- Product, docs, and delivery files are complete; do not redesign.
- Validation state lives in `.agent-handoff/validation.md`; the only failed/blocked check is the default GHCR image pull.
- Agent behavior and the payment rail remain deterministic simulations; see `docs/DEMO_TRUTH_BOUNDARY.md` and ADR 0001.
