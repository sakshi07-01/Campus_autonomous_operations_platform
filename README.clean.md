# Super Manager

Super Manager is a governed execution workspace: a FastAPI backend plus React/Vite frontend that turns user intent into mission-based actions, with approvals, evidence, audit events, and trust metrics around the work that needs control.

## Navigation

1. [Overview](#overview)
2. [Why this is different from generic AI](#why-this-is-different-from-generic-ai)
3. [Governed execution model](#governed-execution-model)
4. [Evidence and trust layer](#evidence-and-trust-layer)
5. [User access points](#user-access-points)
6. [Implementation status](#implementation-status)
7. [Where to start in code](#where-to-start-in-code)

## Overview

Super Manager is not a generic chatbot. It is a chat-first execution system that:

- accepts requests through the web app or API
- routes work through chat, mission, approval, evidence, and analytics surfaces
- keeps the execution record in Supabase-backed tables
- shows progress and control points in the UI

## Why this is different from generic AI

| Generic AI | Super Manager |
| --- | --- |
| Gives advice | Routes requests into executable chat and mission flows |
| Is mostly stateless | Persists sessions, missions, approvals, evidence, and trust data |
| Treats integrations as optional extras | Exposes integrations and OAuth as first-class app surfaces |
| Has little or no proof trail | Stores evidence artifacts, audit events, and trust metrics |
| Handles risky actions loosely | Uses approval decisions and mission state transitions |

## Governed execution model

- Core chat path: [backend/routes/api.py](backend/routes/api.py) and [backend/routes/streaming.py](backend/routes/streaming.py)
- Mission governance: [backend/routes/governance.py](backend/routes/governance.py)
- Evidence storage: [backend/routes/evidence.py](backend/routes/evidence.py)
- Trust analytics: [backend/routes/analytics.py](backend/routes/analytics.py)
- Schema backing the model: [backend/database_supabase.py](backend/database_supabase.py)

The app bootstrap in [backend/main.py](backend/main.py) conditionally mounts routers for governance, evidence, analytics, identity, OAuth, automation, integrations, messaging, and teaching when those modules load successfully.

## Evidence and trust layer

The current codebase stores and exposes the operational record around a mission:

- mission lifecycle state in [backend/core/mission_state.py](backend/core/mission_state.py)
- policy classification in [backend/core/policy_engine.py](backend/core/policy_engine.py)
- mission, approval, and trust aggregation in [backend/core/governance_store.py](backend/core/governance_store.py)
- artifact custody and bundle export in [backend/core/evidence_vault.py](backend/core/evidence_vault.py)
- mission and approval telemetry in [backend/core/telemetry.py](backend/core/telemetry.py)

The Supabase schema includes dedicated tables for missions, mission steps, approval decisions, mission state transitions, evidence artifacts, audit events, trust metrics, and policy rules.

## User access points

The active UI surfaces are centered around the chat shell and task workspace:

- main chat and action handling in [frontend/src/App.jsx](frontend/src/App.jsx)
- adaptive workspace and mission controls in [frontend/src/TaskAdaptiveWorkspace.jsx](frontend/src/TaskAdaptiveWorkspace.jsx)
- task progress, substeps, and notifications in [frontend/src/components/TaskPanel.jsx](frontend/src/components/TaskPanel.jsx)
- integrations management in [frontend/src/components/IntegrationsHub.jsx](frontend/src/components/IntegrationsHub.jsx)
- AI identity setup in [frontend/src/components/AISettings.jsx](frontend/src/components/AISettings.jsx)
- governance approvals, evidence, trust, and policies in [frontend/src/components/GovernanceHub.jsx](frontend/src/components/GovernanceHub.jsx)

## Implementation status

Implemented today:

- authenticated principals and tenant-scoped request binding in [backend/core/auth.py](backend/core/auth.py)
- governance, evidence, policy, and analytics routes
- mission state, approvals, evidence custody, and trust summaries
- tightened security headers and webhook signature verification
- secret scanning in pre-commit and CI
- governance access in the active frontend shell

Still in progress:

- workflow packs for accreditation, faculty workload, and IT incidents
- README/ADR consolidation beyond this top-level positioning
- broader E2E coverage for governance journeys

## Where to start in code

- [backend/main.py](backend/main.py) for router wiring and app bootstrap
- [backend/core/auth.py](backend/core/auth.py) for request principal resolution
- [backend/core/governance_store.py](backend/core/governance_store.py) for mission and approval persistence
- [backend/core/evidence_vault.py](backend/core/evidence_vault.py) for artifact custody
- [frontend/src/components/GovernanceHub.jsx](frontend/src/components/GovernanceHub.jsx) for the governance UI
- [backend/database_supabase.py](backend/database_supabase.py) for schema and persistence changes

## Getting started

The repository is designed for local development with dev principal headers and guarded backend defaults. Refer to the backend and frontend entry points above for the supported flow.

## Product materials

- [PRD](prd.md)
- [Implementation Blueprint](PRODUCT_IMPLEMENTATION_BLUEPRINT.md)
- [Implementation Checklist](IMPLEMENTATION_CHECKLIST.md)
- [Master Checklist](MASTER_IMPLEMENTATION_CHECKLIST.md)
