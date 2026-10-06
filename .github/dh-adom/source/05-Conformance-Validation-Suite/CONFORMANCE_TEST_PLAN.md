# DH-ADOM Conformance Test Plan

## Structural

- Required root governance files exist.
- Root Agent is identifiable.
- Feature Agent declarations exist for defined domains.
- Agent Registry is consistent.

## Behavioral

- Root routes to Feature Agent.
- Feature Agent can receive work.
- Specialist delegation requires a contract.
- Budget violations are rejected.
- Permission escalation is rejected.
- Cross-feature access is rejected unless authorized.

## Resumability

- A fresh session can reconstruct the active task from repository artifacts.

## Audit

- Delegation and material actions create audit events.

## End-to-end

- Requirement → Root → Feature → Specialist → evidence → handoff → Root review.
