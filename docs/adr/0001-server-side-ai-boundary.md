# ADR 0001: Keep AI access behind the application server

## Status

Accepted for the private implementation candidate.

## Context

The template needs a real AI integration without teaching users to expose API keys in
browser code or to give a model autonomous permissions.

## Decision

The browser calls a narrow same-origin FastAPI endpoint. The server loads the API key
from an ignored environment file, validates and redacts input, calls the OpenAI
Responses API with storage disabled, and returns plain text marked for human review.
No model tools or external writes are configured.

## Consequences

- provider credentials never need to reach the browser;
- server deployment and abuse protection remain the application owner's duty;
- a fake advisor makes tests deterministic and credit-free;
- any future tool call, stored conversation, file upload, or autonomous action needs
  a new ADR and threat review.
