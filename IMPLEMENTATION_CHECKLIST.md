# Implementation Checklist

This checklist mirrors the full product blueprint and the requested 80-point change list. Treat each checkbox as a build, review, and QA gate.

## Chunk 1: Identity, Auth, Tenant Binding, and Access Control

- [ ] 1. Add real authentication middleware for all business endpoints, not only rate limiting.
- [ ] 2. Add authorization checks (role-based) on every mission/task/integration endpoint.
- [ ] 3. Remove or lock down endpoints that accept freely supplied `user_id` query/body values without auth binding.
- [ ] 4. Replace `user_id` default patterns with authenticated principal mapping in request context.
- [ ] 5. Enforce tenant isolation in all reads/writes, not only by convention.

## Chunk 2: Governance and Approval Engine

- [ ] 6. Add approval policy engine configurable by risk and role.
- [ ] 7. Store approval decisions as immutable records with approver identity, timestamp, reason, and policy version.
- [ ] 8. Add rejection handling workflow with mandatory reason capture and re-plan logic.
- [ ] 9. Implement explicit mission state machine with locked transitions and audit trail.
- [ ] 10. Add policy compliance scoring per mission.
- [ ] 11. Add trace completeness scoring per mission.
- [x] 12. Add differentiation dashboard that compares governed execution vs suggestion-only output.
- [x] 13. Add exportable evidence bundles for procurement/pilot review.

## Chunk 3: Campus Workflow Packs

- [x] 14. Add accreditation workflow pack (NAAC/NBA/evidence lifecycle).
- [x] 15. Add faculty workload workflow pack and ownership tracking.
- [x] 16. Add campus IT incident workflow pack with triage, escalation, and post-incident report generation.

## Chunk 4: Execution Controls

- [x] 17. Add multi-approver rules for high-risk steps.
- [x] 18. Add manual override with mandatory justification and reviewer-only visibility.
- [x] 19. Add retry/fallback strategy metadata logging for each failed step.
- [x] 20. Add immutable evidence vault abstraction (artifact hash, origin, chain of custody).

## Chunk 5: Security Hardening

- [ ] 21. Harden CSP by removing `unsafe-eval` and reducing `unsafe-inline` where possible.
- [ ] 22. Remove hardcoded fallback AES key from vault code.
- [ ] 23. Enforce startup failure when encryption master key is absent in non-dev environments.
- [ ] 24. Rotate and revoke leaked Firebase credentials immediately, and replace with secret-manager loading.
- [ ] 25. Remove tracked secret files from git history and current index; regenerate keys.
- [ ] 26. Remove tracked environment file from git index.
- [ ] 27. Add pre-commit and CI secret scanning (gitleaks/trufflehog equivalent).
- [ ] 28. Make production boot fail on default secret placeholders, not just warn.
- [ ] 29. Add strict webhook signature verification for messaging endpoints.
- [ ] 30. Add anti-replay and timestamp validation for webhook callbacks.

## Chunk 6: API and Data Integrity

- [x] 31. Add endpoint-level idempotency keys for mission-triggering operations.
- [ ] 32. Add fine-grained audit event schema and retention policy for compliance export.
- [ ] 33. Add explicit data retention controls for logs, evidence, and generated artifacts.
- [ ] 34. Add PII classification and redaction policy in logs and responses.

## Chunk 7: Quality and Regression Coverage

- [ ] 35. Add comprehensive auth tests (unit + integration) for every protected route.
- [ ] 36. Add authorization matrix tests per role and per workflow action.
- [ ] 37. Add policy-engine tests for approval thresholds and edge cases.
- [ ] 38. Add immutable-audit tests (tamper attempts should fail).
- [ ] 39. Add integration failure chaos tests for fallback routing guarantees.
- [ ] 40. Add regression tests for mission state transition validity.
- [ ] 41. Add end-to-end tests for approval queue user journey.
- [ ] 42. Add end-to-end tests for evidence export correctness.

## Chunk 8: Frontend Product Surfaces

- [x] 43. Add frontend pages for approvals queue and governance controls.
- [x] 44. Add frontend mission timeline with policy checkpoints and blocker states.
- [x] 45. Add frontend evidence explorer with source links and artifact versions.
- [x] 46. Add frontend trust metrics dashboard (trace completeness, policy compliance).
- [x] 47. Ensure active UI path includes trust/governance widgets; currently active app is `main.jsx` loading `App.jsx`, while trust footer appears in non-active variant `AppClean.jsx`.
- [ ] 48. Remove dead/temporary patch scripts from root or move to tooling folder with ownership and purpose.

## Chunk 9: Architecture Consolidation

- [ ] 49. Consolidate duplicate/legacy agent paths to reduce ambiguity across brain/orchestrator implementations.
- [ ] 50. Define one canonical orchestration path and deprecate alternates with migration plan.
- [ ] 51. Add architecture decision records for security model and approval model.
- [ ] 52. Update README positioning from broad “do tasks” to “governed institutional execution.”
- [ ] 53. Add explicit “why us vs generic AI” section with measurable outcomes and proof protocol.
- [ ] 54. Add pilot readiness checklist with minimum control gates.
- [ ] 55. Add operations runbook for secret rotation and incident response.

## Chunk 10: Deployment and Observability

- [ ] 56. Add deployment guardrails blocking startup with insecure defaults in production.
- [ ] 57. Add CI gate requiring security tests and auth tests to pass before merge.
- [ ] 58. Add CI gate for minimum coverage on governance-critical modules.
- [x] 59. Add structured telemetry events for mission success, approval latency, and fallback frequency.
- [x] 60. Add baseline-and-delta reporting for pilot KPI evidence (time saved, trace completeness, approval compliance).
- [x] 61. Add product analytics for procurement proof (win/loss reason against generic AI).
- [ ] 62. Add explicit out-of-scope guardrails in UI and API to avoid appearing as generic chatbot-only product.
- [ ] 63. Add institution template onboarding wizard (tenant, roles, policies, integrations).
- [ ] 64. Add role provisioning UX for admin, operator, reviewer, auditor.
- [ ] 65. Add secure defaults for CORS per environment.

## Chunk 11: Logging, Validation, and Migrations

- [ ] 66. Remove debug prints and file-based debug logging in route handlers, replace with structured secure logging.
- [ ] 67. Add input schema hardening for all mission parameters and integration callbacks.
- [ ] 68. Add standardized error model that avoids leaking internal implementation details.
- [ ] 69. Add migration scripts for audit tables and policy tables with versioning.
- [ ] 70. Add versioned policy evaluation records tied to each executed mission step.

## Chunk 12: Small but Required UX and Production Fixes

- [ ] 71. Replace all “default user” sample links in production health/help responses with environment-safe guidance.
- [ ] 72. Ensure all user-facing OAuth prompts include tenant/user context checks before redirect.
- [ ] 73. Standardize naming (confirm vs approval) across backend and frontend for clarity.
- [ ] 74. Add simple UX copy updates so users understand “approval required due to policy” instead of generic confirm phrasing.
- [ ] 75. Add small UI badges on each action step for risk level and approval source.
- [ ] 76. Add one-click export buttons for trace and evidence in task detail panel.
- [ ] 77. Add pagination and filtering in integration/activity history screens.
- [ ] 78. Add basic keyboard accessibility improvements for approval actions.
- [ ] 79. Add empty-state designs for metrics dashboard and evidence explorer.
- [ ] 80. Add clear fallback-state messaging when integrations are disconnected.

## Verification Rule

- [ ] Every checkbox above must be linked to an implementation commit, a test, or a documented decision before the feature is considered complete.
