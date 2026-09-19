# Decision Log

| Date | Decision | Reason | Evidence |
| --- | --- | --- | --- |
| 2026-09-20 | Use multi-document Agent handoff memory. | Preserve durable context across Codex, Claude, and GLM sessions. | `AGENT_HANDOFF.md`. |
| 2026-09-20 | Name the product LedgerProof · 财证中枢. | Connect ledger evidence to verifiable decisions and fit the ProofOps family. | User discussion and `README.md`. |
| 2026-09-20 | Demonstrate payment audit and reversible hold. | Best fit for evidence, approval, independent verification, and rollback under the one-day constraint. | `docs/adr/` pending; implementation in `engine.py`. |
| 2026-09-20 | Reuse CyberGuard through a derived executor image. | Preserve the governance core while adding truthful finance semantics. | `adapter/Dockerfile`, `finance_adapter.py`. |
| 2026-09-20 | Keep the first Agent run deterministic. | Makes the competition demo fast and reproducible while clearly separating future live AgentTeams work. | `docs/DEMO_TRUTH_BOUNDARY.md`. |
| 2026-09-20 | Use a restrained financial audit workspace instead of a neon command center. | Better matches finance audit products and makes evidence and approval readable. | `frontend/src/styles/global.css`. |
| 2026-09-20 | ADR 0001 records the financial-audit migration decision. | Make the domain choice, demo scope, adapter approach, and truth boundary durable and reviewable. | `docs/adr/0001-financial-audit-domain.md`. |
| 2026-09-20 | AgentTeams workers/skills are deployment drafts, not live runs. | Preserve the truth boundary until real Worker deployment receipts exist. | `agentteams/workers.yaml` header, `docs/DEMO_TRUTH_BOUNDARY.md`. |
| 2026-09-20 | Remove unreferenced `ledgerproof-dashboard.{jpg,png}` and duplicate `02-awaiting-approval.jpg`. | No source or doc references them; keep only the documented gif and five PNG frames for a reviewable first commit. | `rg` search over README/docs/frontend/src returned no references. |
| 2026-09-20 | Remove stale `docs/progress`, `docs/reports`, `docs/standards`, `docs/templates`. | One-line scaffolding contradicted actual completion state; not part of the documented docs structure. | README 项目结构 section lists docs as 架构/事实边界/运行/录屏手册 only. |
| 2026-09-20 | Keep `.tmp/` on disk but ignored. | Preserves ability to rebuild the source-equivalent image while GHCR access is blocked; excluded from the commit. | `.gitignore`, `.agent-handoff/risks.md`. |
