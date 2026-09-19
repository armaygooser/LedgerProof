# Validation History

| Date | Command/Check | Result | Notes |
| --- | --- | --- | --- |
| 2026-09-20 | `.\.venv\Scripts\python.exe -m ruff check backend adapter` | passed | No Ruff errors. |
| 2026-09-20 | `.\.venv\Scripts\python.exe -m pytest` | passed | 2 tests passed; two upstream TestClient deprecation warnings. |
| 2026-09-20 | `npm test -- --run` | passed | 1 test file, 2 tests. |
| 2026-09-20 | `npm run build` | passed | Production build passed; non-blocking bundle-size warning. |
| 2026-09-20 | `docker compose config` | passed | Three services and health checks resolved. |
| 2026-09-20 | Exact CyberGuard source image build | passed | Commit `3b34e4c`, original response-executor Dockerfile. |
| 2026-09-20 | Three-container startup | passed | Governance and API healthy; web served on 18866. |
| 2026-09-20 | `scripts/smoke_http.py` | passed | Reset → investigate/propose → approve → execute → verify → rollback; 7 records. |
| 2026-09-20 | 1920×1080 visual capture | passed | Five distinct PNG hashes and an animated GIF generated. |
| 2026-09-20 | Default GHCR image pull | blocked | Unauthenticated pull returned `unauthorized`; package visibility/authentication required. |

## 2026-09-20 final rerun（GLM 收尾会话，交付文件与清理之后）

| Command/Check | Result | Notes |
| --- | --- | --- |
| `.\.venv\Scripts\python.exe -m ruff check backend adapter` | passed | All checks passed. |
| `.\.venv\Scripts\python.exe -m pytest` | passed | 2 tests; same upstream TestClient deprecation warnings only. |
| `npm test -- --run` | passed | 1 file, 2 tests. |
| `npm run build` | passed | Non-blocking bundle >500 kB warning unchanged. |
| `docker compose config --quiet` | passed | Compose resolves cleanly. |
| `docker compose ps` | passed | 3/3 containers healthy (dev-equivalent base image). |
| `scripts/smoke_http.py` | passed | Final phase `rolled_back`; 35 accumulated audit records (6th case generation, 7 records per run); audit head non-empty. |
| `release/ledgerproof-demo.gif` | passed | 5 frames, 960×540; UI unchanged so no regeneration needed. |
| `git status --short --untracked-files=all` | passed | 84 files; no `.venv`/`node_modules`/egg-info/`.tmp`/Edge-profile leaks. |
| Default GHCR image pull re-probe | blocked | Still `unauthorized`; external blocker unchanged. |

## Caveats

- Equivalent source integration passed, but registry image bytes have not been validated（until GHCR access is granted）。
- The full-container smoke ran against the dev-equivalent base image `ledgerproof/cyberguard-executor-dev:3b34e4c`（same source commit `3b34e4c`）, not the default GHCR tag.
