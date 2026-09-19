# Workspace Map

## Repository Structure

- `adapter/`: thin finance adapter derived from the CyberGuard Executor image.
- `backend/ledgerproof_api/`: FastAPI case state machine, seven Agent roles, deterministic dataset, and CyberGuard HTTP client.
- `backend/tests/`: complete flow and hash-determinism tests.
- `frontend/`: React 19, Ant Design 6, ECharts audit console.
- `docker/` and `compose.yaml`: three-container runtime.
- `domainpack/`: reserved for the reusable finance audit domain definition; currently incomplete.
- `agentteams/`: reserved for AgentTeams Worker and Element launch files; currently incomplete.
- `docs/`: architecture, runtime reuse, truth boundary, and demo runbook.
- `release/`: screenshots and `ledgerproof-demo.gif`.
- `scripts/smoke_http.py`: HTTP end-to-end smoke test.
- `GLM_HANDOFF.md`: direct continuation instructions for 智谱 GLM.

## Main Entry Points

- Web: `frontend/src/App.tsx`
- API: `backend/ledgerproof_api/app.py`
- Workflow: `backend/ledgerproof_api/engine.py`
- CyberGuard client: `backend/ledgerproof_api/governance.py`
- Finance adapter: `adapter/finance_adapter.py`
- Runtime: `compose.yaml`

## Test Entry Points

- `.\.venv\Scripts\python.exe -m ruff check backend adapter`
- `.\.venv\Scripts\python.exe -m pytest`
- `npm test -- --run` from `frontend/`
- `npm run build` from `frontend/`
- `.\.venv\Scripts\python.exe scripts\smoke_http.py` with containers running

## Docs And Specs

- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/CYBERGUARD_RUNTIME_REUSE.md`
- `docs/DEMO_TRUTH_BOUNDARY.md`
- `docs/DEMO_RUNBOOK.md`

## Durable Project Context

- Product name: LedgerProof · 财证中枢.
- Demo domain: payment pre-audit with reversible payment hold.
- Foundation: CyberGuard Executor tag `sha-3b34e4c`.
- Human approval remains mandatory for the L2 action.
- No live ERP, bank, or model connection exists yet.

## Project Conventions

- Keep domain facts linked to Evidence IDs and SHA-256 values.
- Never grant investigation Agents approval or execution credentials.
- Preserve truthful `simulation` labeling until real systems are connected.
- Update handoff files before ending non-trivial work.
