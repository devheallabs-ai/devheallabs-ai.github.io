from .models import DelegationContract

class DelegationPolicy:
    def authorize(self, parent, child, contract: DelegationContract):
        if contract.parent_agent != parent.agent_id:
            raise PermissionError("Parent mismatch")
        if contract.child_agent != child.agent_id:
            raise PermissionError("Child mismatch")
        if contract.max_depth > parent.budget.max_delegation_depth:
            raise PermissionError("Delegation depth exceeds parent budget")
        if contract.budget.max_steps > parent.budget.max_steps:
            raise PermissionError("Step budget exceeds parent budget")
        if contract.budget.max_cost_usd > parent.budget.max_cost_usd:
            raise PermissionError("Cost budget exceeds parent budget")
        if not set(contract.permissions).issubset(set(parent.permissions)):
            raise PermissionError("Delegated permission exceeds parent authority")
        if not set(contract.permissions).issubset(set(child.permissions)):
            raise PermissionError("Delegated permission exceeds child grant")
        if set(contract.include_scope) & set(contract.exclude_scope):
            raise PermissionError("Scope contains both include and exclude entry")
        return True
