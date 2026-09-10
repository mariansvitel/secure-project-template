# Publication Gate

Keep the repository private until every applicable item is true.

## Value and documentation

- [x] Purpose, audience, setup, status, and limitations are accurate.
- [x] A fresh clone can run without private context.
- [x] Examples and fixtures are synthetic.

## Secrets and data

- [x] Current files and complete reachable Git history were scanned for credentials.
- [x] No personal, employer, customer, or confidential data is present.
- [x] `.env.local` is ignored and absent from Git history.
- [x] A project-scoped key with appropriate limits can be rotated independently.

## Software and AI

- [x] Ruff, tests, coverage threshold, and CI pass.
- [x] Dependencies and GitHub Actions are reviewed and current.
- [x] Browser assets contain no provider key or direct provider API call.
- [x] Threat model and AI boundaries match the implementation.
- [x] No live smoke test was required; offline tests use synthetic inputs and a fake advisor.

## GitHub transition

- [x] Owner explicitly approved publication on 2026-09-10.
- [ ] Public metadata, license, issue form, and security policy render correctly.
- [ ] Secret scanning and push protection are enabled.
- [ ] Private vulnerability reporting is enabled immediately after publication.
- [x] Rollback to private is ready if a transition-only check fails.
