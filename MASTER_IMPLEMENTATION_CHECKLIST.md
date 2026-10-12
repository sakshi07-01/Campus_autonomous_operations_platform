# Master Implementation Checklist

Source references:
- Product blueprint: [PRODUCT_IMPLEMENTATION_BLUEPRINT.md](PRODUCT_IMPLEMENTATION_BLUEPRINT.md)
- Product requirements: [prd.md](prd.md)

Usage:
- Mark each item done only when code, tests, and UX validation pass.
- Every item should include evidence (PR link, test name, screenshot, or log excerpt).

## Layer A: Identity, Access, and Tenant Controls

- [ ] C001: Add real authentication middleware for all business endpoints, not only rate limiting.
- [ ] C002: Add role-based authorization checks on every mission/task/integration endpoint.
- [ ] C003: Remove or lock down endpoints accepting freely supplied user_id query/body values.
- [ ] C004: Replace user_id default patterns with authenticated principal mapping in request context.
- [ ] C005: Enforce tenant isolation in all reads/writes.

## Layer B: Governance and Approval Engine

- [ ] C006: Add approval policy engine configurable by risk and role.
- [ ] C007: Store approval decisions as immutable records with approver id, timestamp, reason, policy version.
- [ ] C008: Add rejection workflow with mandatory reason capture and re-plan logic.
- [ ] C009: Implement explicit mission state machine with locked transitions and audit trail.
- [ ] C010: Add policy compliance scoring per mission.
- [ ] C011: Add trace completeness scoring per mission.
- [x] C017: Add multi-approver rules for high-risk steps.
- [x] C018: Add manual override with mandatory justification and reviewer-only visibility.
- [x] C019: Add retry/fallback strategy metadata logging for each failed step.

## Layer C: Evidence, Trust, and Differentiation

- [x] C012: Add differentiation dashboard comparing governed execution vs suggestion-only output.
- [x] C013: Add exportable evidence bundles for procurement/pilot review.
- [x] C020: Add immutable evidence vault abstraction (artifact hash, origin, chain of custody).
- [ ] C032: Add fine-grained audit event schema and retention policy for compliance export.
- [ ] C033: Add explicit data retention controls for logs, evidence, generated artifacts.
- [x] C059: Add structured telemetry events for mission success, approval latency, fallback frequency.
- [x] C060: Add baseline-and-delta reporting for pilot KPI evidence.
- [x] C061: Add product analytics for procurement proof (win/loss reasons vs generic AI).

## Layer D: Domain Workflow Packs

- [x] C014: Add accreditation workflow pack (NAAC/NBA/evidence lifecycle).
- [x] C015: Add faculty workload workflow pack with ownership tracking.
- [x] C016: Add campus IT incident workflow pack with triage, escalation, post-incident report.

## Layer E: Security Hardening

- [ ] C021: Harden CSP by removing unsafe-eval and reducing unsafe-inline where possible.
- [ ] C022: Remove hardcoded fallback AES key from vault code.
- [ ] C023: Enforce startup failure when encryption master key is absent in non-dev.
- [ ] C024: Rotate and revoke leaked Firebase credentials; replace with secret-manager loading.
- [ ] C025: Remove tracked secret files from git history and index; regenerate keys.
- [ ] C026: Remove tracked .env from git index.
- [ ] C027: Add pre-commit and CI secret scanning.
- [ ] C028: Make production boot fail on default secret placeholders, not just warn.
- [ ] C029: Add strict webhook signature verification for messaging endpoints.
- [ ] C030: Add anti-replay and timestamp validation for webhook callbacks.
- [ ] C034: Add PII classification and redaction policy in logs and responses.
- [ ] C056: Add deployment guardrails blocking startup with insecure defaults in production.
- [ ] C065: Add secure defaults for CORS per environment.
- [ ] C066: Remove debug prints and file-based debug logging; use structured secure logging.
- [ ] C067: Harden input schemas for mission parameters and integration callbacks.
- [ ] C068: Add standardized error model that avoids leaking internal details.

## Layer F: Reliability, API Safety, and Data Integrity

- [x] C031: Add endpoint-level idempotency keys for mission-triggering operations.
- [ ] C069: Add migration scripts for audit tables and policy tables with versioning.
- [ ] C070: Add versioned policy evaluation records tied to each mission step.

## Layer G: Testing and Quality Gates

- [ ] C035: Add comprehensive auth tests (unit + integration) for every protected route.
- [ ] C036: Add authorization matrix tests per role and workflow action.
- [ ] C037: Add policy-engine tests for thresholds and edge cases.
- [ ] C038: Add immutable-audit tests (tamper attempts fail).
- [ ] C039: Add integration-failure chaos tests for fallback guarantees.
- [ ] C040: Add regression tests for mission state transition validity.
- [ ] C041: Add end-to-end tests for approval queue journey.
- [ ] C042: Add end-to-end tests for evidence export correctness.
- [ ] C057: Add CI gate requiring security + auth tests to pass before merge.
- [ ] C058: Add CI gate for minimum coverage on governance-critical modules.

## Layer H: Frontend Governance UX

- [x] C043: Add frontend approvals queue and governance controls pages.
- [x] C044: Add mission timeline with policy checkpoints and blocker states.
- [x] C045: Add evidence explorer with source links and artifact versions.
- [x] C046: Add trust metrics dashboard (trace completeness, policy compliance).
- [x] C047: Ensure active UI path includes trust/governance widgets.
- [ ] C062: Add explicit out-of-scope guardrails in UI and API.
- [ ] C063: Add institution template onboarding wizard (tenant, roles, policies, integrations).
- [ ] C064: Add role provisioning UX for admin/operator/reviewer/auditor.

## Layer I: Architecture and Product Positioning

- [ ] C048: Remove dead/temporary patch scripts from root or move to tooling folder with ownership.
- [ ] C049: Consolidate duplicate/legacy agent paths to reduce ambiguity.
- [ ] C050: Define one canonical orchestration path and deprecate alternates with migration plan.
- [ ] C051: Add ADRs for security model and approval model.
- [ ] C052: Update README positioning to governed institutional execution.
- [ ] C053: Add explicit why-us-vs-generic-AI section with measurable outcomes and proof protocol.
- [ ] C054: Add pilot readiness checklist with minimum control gates.
- [ ] C055: Add operations runbook for secret rotation and incident response.

## Layer J: Micro-Level UX and Safety Fixes

- [ ] C071: Replace default-user sample links in production status/help responses.
- [ ] C072: Ensure all OAuth prompts enforce tenant/user context checks before redirect.
- [ ] C073: Standardize naming (confirm vs approval) across backend/frontend.
- [ ] C074: Update UX copy to explain approval required due to policy.
- [ ] C075: Add risk-level and approval-source badges on each action step.
- [ ] C076: Add one-click export buttons for trace/evidence in task details.
- [ ] C077: Add pagination/filtering in integration/activity history.
- [ ] C078: Add keyboard accessibility improvements for approval actions.
- [ ] C079: Add empty states for metrics dashboard and evidence explorer.
- [ ] C080: Add clear fallback-state messaging when integrations are disconnected.

## Verification fields for each completed item

For each item marked done, append:
- Code evidence:
- Test evidence:
- UX evidence:
- Security review note:
- Date:
- Owner:
