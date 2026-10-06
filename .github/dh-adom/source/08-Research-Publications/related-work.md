# Related Work

## Orchestrator-worker agent patterns
Anthropic documents orchestrator-worker workflows in which a central model dynamically breaks down tasks, delegates to workers, and synthesizes results. This is a direct precedent for the Root orchestration primitive, but does not itself define persistent repository feature ownership. 

## Multi-agent frameworks
Microsoft Research's AutoGen provides a framework for composing multi-agent applications. DH-ADOM is not a replacement for such a runtime; it is a repository governance and ownership model that can sit above or alongside a runtime.

## AI-SDLC
The public AI-SDLC Framework defines an autonomous software development lifecycle with an orchestrator, quality gates, progressive autonomy, codebase intelligence, and tamper-evident audit logging. DH-ADOM overlaps with this governance direction but focuses specifically on persistent Feature Agent ownership and a Root → Feature → Specialist engineering hierarchy.

## ADLC
Salesforce publishes an Agent Development Lifecycle adapted to agents' non-deterministic behavior, spanning ideation/design, development, testing/validation, deployment, and continuous monitoring/tuning.

## Hierarchical SWE agents
BOAD studies hierarchical software engineering agents and uses specialized sub-agents coordinated by an orchestrator. DH-ADOM aligns with the value of hierarchy but extends the model toward repository-level ownership, explicit delegation contracts, durable state, and lifecycle governance.

## Agent identity / security
NIST is actively working on identity and authorization for software and AI agents, including authentication, authorization, auditing, non-repudiation, and prompt-injection-related controls. DH-ADOM treats identity and authorization as prerequisites for bounded delegation.

## Agentic security
OWASP's 2026 Agentic Applications Top 10 frames agentic systems as a distinct security domain. DH-ADOM maps those concerns into agent hierarchy, permission boundaries, delegation, and audit controls.
