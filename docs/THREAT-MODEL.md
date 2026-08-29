# Threat Model

## Protected assets

- OpenAI API key and project budget;
- user input before and during provider transmission;
- integrity of advice shown in the browser;
- repository history and CI permissions.

## Trust boundaries

1. Browser input is untrusted.
2. The FastAPI server validates and locally redacts input.
3. Sanitized text crosses the OpenAI API boundary.
4. Model output returns as untrusted text and is rendered with `textContent`.
5. A human reviews the result before any decision or external action.

## Addressed threats

| Threat | Current control |
| --- | --- |
| Key exposed to browser | Key exists only in server environment settings |
| Secret accidentally committed | `.env*` ignored except empty example; CI uses no API key |
| Prompt injection in user text | User content is delimited and explicitly treated as data |
| Oversized or expensive input | Schema and combined character limits |
| Common credential or email leakage | Local pattern redaction before provider call |
| XSS from model output | Browser inserts response using `textContent`, not HTML |
| Framing and browser capability abuse | CSP, frame denial, restrictive permissions policy |
| Detailed provider errors leak internals | Generic 502 response with a request identifier |
| Workflow token overreach | CI declares read-only `contents` permission |
| Supply-chain drift in Actions | Actions are pinned to immutable commit SHAs |

## Accepted limitations

- Pattern redaction cannot identify every sensitive value or contextual identifier.
- In-memory controls are not a substitute for production rate limiting.
- No authentication or tenant separation exists.
- Provider processing and retention follow the account's OpenAI data controls.
- Advice may be wrong, biased, incomplete, or vulnerable to adversarial input.

Any production deployment, user accounts, stored data, file uploads, model tools, or
external writes require a new threat review.
