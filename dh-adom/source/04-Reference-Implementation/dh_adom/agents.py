from .models import Handoff

class RootAgent:
    def __init__(self, registry, policy, audit):
        self.registry=registry; self.policy=policy; self.audit=audit

    def route_feature(self, feature):
        agent=self.registry.feature_owner(feature)
        self.audit.record("ROOT", "route_feature", feature, "ALLOW", feature_owner=agent.agent_id)
        return agent

    def authorize_delegation(self, contract):
        parent=self.registry.get(contract.parent_agent)
        child=self.registry.get(contract.child_agent)
        self.policy.authorize(parent, child, contract)
        self.audit.record("ROOT", "authorize_delegation", contract.delegation_id, "ALLOW", child=child.agent_id)
        return True

class FeatureAgent:
    def __init__(self, agent, registry, root, audit):
        self.agent=agent; self.registry=registry; self.root=root; self.audit=audit

    def receive(self, task):
        self.audit.record(self.agent.agent_id, "receive_task", task["task_id"], "ALLOW")
        return task

    def handoff(self, delegation_id, summary, changed_files=None, tests=None, evidence=None, risks=None):
        return Handoff(
            delegation_id=delegation_id,
            status="HANDOFF",
            summary=summary,
            changed_files=changed_files or [],
            tests=tests or [],
            evidence=evidence or [],
            risks=risks or [],
        )

class SpecialistAgent:
    def __init__(self, agent, audit): self.agent=agent; self.audit=audit
    def execute(self, contract, task):
        self.audit.record(self.agent.agent_id, "execute", contract.delegation_id, "START")
        # Reference behavior: execution is represented, not a real model call.
        self.audit.record(self.agent.agent_id, "execute", contract.delegation_id, "COMPLETE")
        return {"status":"COMPLETE","task_id":task["task_id"]}
