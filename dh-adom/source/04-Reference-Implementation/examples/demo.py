from dh_adom.models import Agent, AgentType, AutonomyBudget, DelegationContract
from dh_adom.registry import AgentRegistry
from dh_adom.policy import DelegationPolicy
from dh_adom.audit import AuditLog
from dh_adom.agents import RootAgent, FeatureAgent, SpecialistAgent

registry=AgentRegistry(); audit=AuditLog(); policy=DelegationPolicy()
root=Agent("ROOT-001","Root",AgentType.ROOT,None,None,permissions=["repo.read","repo.write"],budget=AutonomyBudget(max_steps=100,max_cost_usd=10,max_delegation_depth=2))
feature=Agent("FEATURE-EVAL","Evaluation",AgentType.FEATURE,"ROOT-001","evaluation",permissions=["repo.read","repo.write"],budget=AutonomyBudget(max_steps=50,max_cost_usd=5,max_delegation_depth=1))
specialist=Agent("SPEC-TEST","Test Specialist",AgentType.SPECIALIST,"FEATURE-EVAL","evaluation",permissions=["repo.read"],budget=AutonomyBudget(max_steps=20,max_cost_usd=1,max_delegation_depth=0))
for a in (root,feature,specialist): registry.register(a)
root_agent=RootAgent(registry,policy,audit)
feature_agent=FeatureAgent(feature,registry,root_agent,audit)
root_agent.route_feature("evaluation")
contract=DelegationContract("DEL-DEMO","FEATURE-EVAL","SPEC-TEST","TASK-DEMO","validate evaluation behavior",["features/evaluation/**"],[],["repo.read"],AutonomyBudget(max_steps=10,max_cost_usd=1,max_delegation_depth=0),1)
root_agent.authorize_delegation(contract)
result=SpecialistAgent(specialist,audit).execute(contract,{"task_id":"TASK-DEMO"})
print("Result:", result)
print("Audit events:", len(audit.events))
