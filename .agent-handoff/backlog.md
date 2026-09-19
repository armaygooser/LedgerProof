# Task Backlog

## P0

- [x] Add `domainpack/finance-audit.yaml` with evidence, controls, actions, and verification assertions.
- [x] Add seven LedgerProof workers to `agentteams/workers.yaml`.
- [x] Add AgentTeams skills for financial observation, controlled payment action, and independent verification.
- [x] Add `agentteams/ELEMENT_LAUNCH.md` and `agentteams/room-message.md` using the accurate link-out model.
- [x] Add `docs/adr/0001-financial-audit-domain.md`.
- [x] Add `.tmp/` and `*.egg-info/` to `.gitignore`; verified no generated artifacts are tracked.
- [x] Rerun all checks, update handoff, and create the first commit.
- [ ] Resolve GHCR access and validate the default `ghcr.io/elsechord/cyberguard-executor:sha-3b34e4c` image（blocked on user action: make package public or `docker login ghcr.io`）。

## P1

- [ ] Add a GitHub remote and push only after the user supplies or creates the LedgerProof repository.
- [ ] Check README animation and Mermaid rendering on GitHub.
- [ ] Optionally reduce the frontend bundle after the competition demo; current warning is non-blocking.
- [ ] After real AgentTeams Worker deployment with receipts: mark the Element flow as live run and adjust model/runtime.
