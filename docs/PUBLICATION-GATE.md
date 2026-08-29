# Publication Gate

Keep the repository private until every applicable item is true.

## Value and documentation

- [ ] Purpose, audience, setup, status, and limitations are accurate.
- [ ] A fresh clone can run without private context.
- [ ] Examples and fixtures are synthetic.

## Secrets and data

- [ ] Current files and complete reachable Git history were scanned for credentials.
- [ ] No personal, employer, customer, or confidential data is present.
- [ ] `.env.local` is ignored and absent from Git history.
- [ ] A project-scoped key with appropriate limits can be rotated independently.

## Software and AI

- [ ] Ruff, tests, coverage threshold, and CI pass.
- [ ] Dependencies and GitHub Actions are reviewed and current.
- [ ] Browser assets contain no provider key or direct provider API call.
- [ ] Threat model and AI boundaries match the implementation.
- [ ] A synthetic live smoke test, if run, reveals no sensitive data or detailed error.

## GitHub transition

- [ ] Owner explicitly approves publication.
- [ ] Public metadata, license, issue form, and security policy render correctly.
- [ ] Secret scanning and push protection are enabled.
- [ ] Private vulnerability reporting is enabled immediately after publication.
- [ ] Rollback to private is ready if a transition-only check fails.
