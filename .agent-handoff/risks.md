# Risks, Blockers, And Unknowns

## Current Blockers

- None. GHCR access resolved 2026-09-20 via authenticated `docker login ghcr.io`（read:packages token）。

## Current Risks

- The GHCR package remains **private**（org policy forbids member visibility changes）. Any new/demo machine must `docker login ghcr.io` before `docker compose up --build`, or an org owner must make it public.
- The read:packages token lives only in the local Docker credential store; it is not in the repository. Losing it means re-issuing from GitHub token settings.
- Current Agent outputs and payment rail are deterministic simulations. Overclaiming live model or bank integration would be inaccurate; `agentteams/` files are deployment drafts, not live runs.
- Demo credentials in Compose are intentionally weak placeholders and must not be used in production.
- Audit ledger accumulates across runs in the Docker volume（design behavior）; demo case state resets on API restart.

## Unknowns / Confirmations Needed

- UNKNOWN: the exact AgentTeams model/runtime available on the final demo machine; `agentteams/workers.yaml` mirrors the ProofOps reference (`deepseek-v4-flash` / `copaw`) and must be adjusted before real deployment.
