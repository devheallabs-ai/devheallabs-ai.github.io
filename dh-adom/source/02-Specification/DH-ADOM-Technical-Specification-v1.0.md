# DH-ADOM Technical Specification v1.0

Status: Normative
Version: 1.0.0
Date: 2026-10-06

## 1. Scope

DH-ADOM specifies a repository-level operating model for AI-native software engineering. It defines governance hierarchy, agent roles, domain ownership, bounded delegation, lifecycle integration, evidence, state, handoff, and conformance requirements.

## 2. Normative language

The terms MUST, MUST NOT, SHOULD, SHOULD NOT, MAY, and RECOMMENDED are normative.

## 3. Governance hierarchy

1. Engineering Constitution
2. AI-SDLC
3. ADLC
4. Root Agent
5. Feature Agent
6. Specialist Agent
7. Implementation

## 4. Agent roles

### 4.1 Root Agent

The Root Agent MUST own global orchestration and MUST NOT require itself to implement every feature.

### 4.2 Feature Agent

Every meaningful bounded domain SHOULD have one persistent Feature Agent. A Feature Agent MUST declare intent, ownership, capabilities, tools, permissions, autonomy, risks, state, and handoff.

### 4.3 Specialist Agent

A Specialist Agent MUST be created under a parent Feature Agent or explicitly authorized Root Agent. It MUST have a bounded purpose and task-scoped permissions.

## 5. Delegation Contract

Every delegation MUST identify parent, child, purpose, task, scope, permissions, budget, lifetime, evidence requirements, and acceptance criteria.

## 6. Delegation invariants

- Child scope MUST be a subset of authorized parent scope unless explicitly widened through governance.
- Delegation depth MUST be bounded.
- Parallel child execution MUST be bounded.
- Child permissions MUST NOT exceed delegated authority.
- Completion MUST return evidence and handoff.
- Uncontrolled recursive spawning MUST be blocked.

## 7. Feature ownership

Feature Agent ownership is an engineering boundary. Cross-feature changes require coordination through the Root Agent and MUST be traceable.

## 8. Identity and contract

Agent identity is distinct from model identity. Each agent MUST have an identity record and SHOULD have a machine-readable passport and contract.

## 9. AI-SDLC integration

All material work MUST map to intent, requirements, architecture, implementation, validation, evidence, release, and feedback.

## 10. ADLC integration

All agents MUST follow an agent lifecycle that includes intent, contract, identity, capabilities, permissions, autonomy, validation, promotion, monitoring, revalidation, and retirement.

## 11. Evidence

Meaningful tasks MUST emit auditable evidence of implementation and validation.

## 12. Handoff

A completed task MUST update state and create a machine-readable handoff sufficient for an independent AI session to continue work.

## 13. Security

Agents MUST follow least privilege. Production actions MUST be policy-controlled. Permission or autonomy escalation MUST NOT be self-authorized.

## 14. Conformance

An implementation conforms to DH-ADOM v1.0 only when all mandatory requirements in `CONFORMANCE-REQUIREMENTS.md` pass or have a formally accepted exception.
