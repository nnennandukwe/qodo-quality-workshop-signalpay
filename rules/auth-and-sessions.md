# Auth and Session Rules

Use these rules when changing token validation, scopes, or mutation handlers.

## PAY-002: Auth and required scope checks happen before mutation

- Trigger: adding or changing any endpoint that reads or mutates payment data.
- Required behavior: validate the bearer session token and required scope
  before changing state, writing idempotency results, or emitting events.
- Verification signal: tests cover a token without the required scope and
  assert that no payment state or event state changed.

## Session Handling Notes

- Use the existing `verify_session` helper for local workshop tokens.
- Keep the audience check set to `payments-api` for payment API routes.
- Return clear `401` errors for missing, unknown, or wrong-audience tokens.
- Return clear `403` errors for known tokens that lack the required scope.
