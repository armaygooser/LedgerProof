# Risks, Blockers, And Unknowns

## Current Blockers

- GHCR package `ghcr.io/elsechord/cyberguard-executor:sha-3b34e4c` is not anonymously readable（re-probed 2026-09-20，still `unauthorized`）。Source-equivalent validation exists; registry validation does not. Resolve by making the package Public or `docker login ghcr.io`.

## Current Risks

- Current Agent outputs and payment rail are deterministic simulations. Overclaiming live model or bank integration would be inaccurate; `agentteams/` files are deployment drafts, not live runs.
- Demo credentials in Compose are intentionally weak placeholders and must not be used in production.
- Audit ledger accumulates across runs in the Docker volume（design behavior）; demo case state resets on API restart.
- First commit exists on a branch with no remote; work is not backed up off-machine until the user provides a GitHub repository.

## Unknowns / Confirmations Needed

- UNKNOWN: whether the user will make the CyberGuard GHCR package public or authenticate Docker.
- UNKNOWN: the GitHub repository URL for LedgerProof.
- UNKNOWN: the exact AgentTeams model/runtime available on the final demo machine; `agentteams/workers.yaml` mirrors the ProofOps reference (`deepseek-v4-flash` / `copaw`) and must be adjusted before real deployment.
