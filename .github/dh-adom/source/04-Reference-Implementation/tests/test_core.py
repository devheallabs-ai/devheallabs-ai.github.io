import unittest
from dh_adom.models import Agent, AgentType, AutonomyBudget, DelegationContract
from dh_adom.registry import AgentRegistry
from dh_adom.policy import DelegationPolicy
from dh_adom.audit import AuditLog
from dh_adom.agents import RootAgent, SpecialistAgent

class DHADOMTests(unittest.TestCase):
    def setUp(self):
        self.registry=AgentRegistry(); self.audit=AuditLog(); self.policy=DelegationPolicy()
        root=Agent("ROOT-001","Root",AgentType.ROOT,None,None,permissions=["repo.read","repo.write"],budget=AutonomyBudget(max_steps=100,max_cost_usd=10,max_delegation_depth=2))
        feature=Agent("FEATURE-EVAL","Evaluation",AgentType.FEATURE,"ROOT-001","evaluation",permissions=["repo.read","repo.write"],budget=AutonomyBudget(max_steps=50,max_cost_usd=5,max_delegation_depth=1))
        specialist=Agent("SPEC-TEST","Test Specialist",AgentType.SPECIALIST,"FEATURE-EVAL","evaluation",permissions=["repo.read"],budget=AutonomyBudget(max_steps=20,max_cost_usd=1,max_delegation_depth=0))
        for a in (root,feature,specialist): self.registry.register(a)
        self.root=RootAgent(self.registry,self.policy,self.audit)

    def test_feature_owner_is_unique(self):
        self.assertEqual(self.root.route_feature("evaluation").agent_id,"FEATURE-EVAL")

    def test_valid_delegation(self):
        contract=DelegationContract("DEL-1","FEATURE-EVAL","SPEC-TEST","TASK-1","test","[features/evaluation]" if False else ["features/evaluation/**"],[],["repo.read"],AutonomyBudget(max_steps=10,max_cost_usd=1,max_delegation_depth=0),1)
        self.assertTrue(self.root.authorize_delegation(contract))

    def test_permission_escalation_is_blocked(self):
        contract=DelegationContract("DEL-2","FEATURE-EVAL","SPEC-TEST","TASK-2","bad","[x]" if False else ["features/evaluation/**"],[],["repo.write"],AutonomyBudget(max_steps=10,max_cost_usd=1,max_delegation_depth=0),1)
        with self.assertRaises(PermissionError): self.root.authorize_delegation(contract)

if __name__ == "__main__": unittest.main()
