# Secure Project Template

**A security-first, AI-ready starter for small, reviewable web applications.**

The included example is an **AI Decision Desk**: a user frames a decision, the
server asks OpenAI for a structured challenge, and a human remains responsible for
the outcome. The model cannot write to external systems, approve changes, or see the
API key.

> Repository status: private implementation candidate. Do not publish it until the
> [Publication Gate](docs/PUBLICATION-GATE.md) is complete.

## What makes this different

- AI output is advice, never an autonomous action.
- Input is bounded and likely secrets or email addresses are redacted locally.
- API requests are made only by the Python server with response storage disabled.
- The browser receives neither the API key nor provider credentials.
- Offline tests use a fake advisor and never spend API credits.
- CI starts with read-only repository permissions and pinned action commits.
- The threat model and limitations are part of the template, not an afterthought.

## Architecture

```text
Browser (same origin)
        |
        | POST /api/assist — bounded user text, no credentials
        v
FastAPI validation -> local redaction -> OpenAI Responses API
        |                                  |
        +---------- safe result <----------+
        |
        v
Human review — accept, revise, or reject
```

## Quick start

Requirements: Python 3.11 or newer.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install pip==26.2.1
python -m pip install -e ".[dev]"
python -m uvicorn secure_starter.app:app --reload
```

Open <http://127.0.0.1:8000>. The health endpoint at `/api/health` reports only
whether AI is configured; it never returns the key.

The local `.env.local` file is ignored by Git. New copies of this template should
start from `.env.example` and add their own project-scoped key locally.

## Safe first use

1. Use synthetic, non-sensitive text.
2. Confirm the UI safety checkbox only after checking the input.
3. Treat the response as an untrusted draft.
4. Verify factual claims independently.
5. Do not connect writes or external tools without a new threat review.

## Validation

```powershell
python -m ruff check .
python -m ruff format --check .
python -m pytest
```

Tests are offline by design. A live API smoke test is optional and must use synthetic
input, an explicit cost decision, and a project-scoped key.

## Reusing the template

Replace the Decision Desk prompt and schemas with one narrow domain task. Preserve
the server-side credential boundary, input constraints, fake test advisor, human
review flag, security headers, and publication gate until a documented threat review
justifies a change.

## Important limits

This is not a production platform. It does not include authentication, durable rate
limiting, multi-user data isolation, audit-log storage, billing controls, or a
deployment recipe. Local redaction is a safety net, not a guarantee that every
sensitive value will be detected. See the [Threat Model](docs/THREAT-MODEL.md) and
[AI Boundaries](docs/AI-BOUNDARIES.md).

## License

[MIT](LICENSE)
