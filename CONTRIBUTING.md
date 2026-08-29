# Contributing

Keep changes small, reversible, and linked to a defined outcome.

1. Open a Safe Experiment issue without private or sensitive data.
2. Create one focused branch from `main`.
3. Add tests for success and relevant failure behavior.
4. Run Ruff and pytest locally.
5. Explain new dependencies, permissions, data flows, or AI behavior in the PR.
6. Merge only after CI and the human review gate pass.

Never commit a populated environment file. Use synthetic fixtures. AI-generated code
or prose must receive the same review as human-generated work.
