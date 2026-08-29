# AI Boundaries

## Green lane — allowed by default

- challenge synthetic product decisions;
- propose bounded options and testable assumptions;
- create a pre-mortem from non-sensitive context;
- run offline tests with a fake advisor.

## Amber lane — explicit review required

- changing the model or prompt;
- increasing input or output limits;
- introducing new data categories;
- enabling provider-side tools, retrieval, file inputs, or persistent storage;
- running a live smoke test that consumes API credits.

## Red lane — not part of this template

- putting a provider key in browser code or Git;
- autonomous merges, deployments, payments, messages, or account changes;
- processing credentials, personal data, customer data, or confidential source code;
- treating model output as approval or verified fact.

The accountable actor is always a human maintainer. The model may recommend; it does
not own permissions, decisions, or consequences.
