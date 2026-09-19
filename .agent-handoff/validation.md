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

## 2026-09-20 GitHub 发布（GLM 会话）

| Command/Check | Result | Notes |
| --- | --- | --- |
| Secret scan of committed tree (`git grep` token/key patterns) | passed | No matches; `.env.example` contains only documented demo placeholders. |
| Repo create via API（stored GCM token，account `armaygooser`，scopes gist/repo/workflow） | passed | https://github.com/armaygooser/LedgerProof created public. |
| `git push -u origin main` | passed | GCM-stored credential，non-interactive（`GCM_INTERACTIVE=Never`）。 |
| WebFetch of repo page | passed | Public README renders; flagged description mojibake. |
| Repo description PATCH via Python（UTF-8 payload） | passed | Codepoint-verified correct Chinese. |
| README clone-URL fix commit + push | passed | `d6056d0` pushed. |
| `gh auth login --with-token` | failed | Token lacks `read:org`; used direct API + GCM instead. |
| Anonymous package settings page | 404 | Private package hidden from anonymous users，consistent with `unauthorized` pull. |

## 2026-09-20 默认 GHCR 镜像验证（用户 docker login 后）

| Command/Check | Result | Notes |
| --- | --- | --- |
| `docker pull ghcr.io/elsechord/cyberguard-executor:sha-3b34e4c` | passed | Authenticated via user's read:packages token；digest `sha256:dd4715f6bd2eed0d806b75d16ca1cb97e7534ab2f0ecefa8ba7faa3ae7162845`. |
| `docker compose config` | passed | No local `.env` override；build arg resolved to the default GHCR tag. |
| `docker compose build --pull cyberguard-governance` | passed | `FROM` resolved by digest from GHCR；image rebuilt. |
| `docker compose up -d` | passed | Governance recreated and healthy; api/web reused（healthy）. |
| `scripts/smoke_http.py`（default-image stack） | passed | Case `FIN-2026-0919-007` → `rolled_back`; 42 accumulated audit records; audit head non-empty. |

## Caveats

- Registry image bytes ARE now validated（authenticated pull，2026-09-20）. The earlier dev-equivalent runs used the same source commit `3b34e4c`.
- Anonymous (unauthenticated) pulls still fail: the package remains private; new machines must `docker login ghcr.io` first.
