from dataclasses import dataclass, field
from typing import Optional, List, Dict
from enum import Enum

class AgentType(str, Enum):
    ROOT = "ROOT"
    FEATURE = "FEATURE"
    SPECIALIST = "SPECIALIST"

@dataclass
class AutonomyBudget:
    level: str = "A2"
    max_steps: int = 50
    max_tool_calls: int = 25
    max_runtime_seconds: int = 900
    max_cost_usd: float = 2.0
    max_parallel_agents: int = 2
    max_delegation_depth: int = 1

@dataclass
class Agent:
    agent_id: str
    name: str
    type: AgentType
    parent_agent: Optional[str]
    feature: Optional[str]
    scope: List[str] = field(default_factory=list)
    permissions: List[str] = field(default_factory=list)
    budget: AutonomyBudget = field(default_factory=AutonomyBudget)

@dataclass
class DelegationContract:
    delegation_id: str
    parent_agent: str
    child_agent: str
    task_id: str
    purpose: str
    include_scope: List[str]
    exclude_scope: List[str]
    permissions: List[str]
    budget: AutonomyBudget
    max_depth: int = 1

@dataclass
class Handoff:
    delegation_id: str
    status: str
    summary: str
    changed_files: List[str] = field(default_factory=list)
    tests: List[str] = field(default_factory=list)
    evidence: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)

@dataclass
class AuditEvent:
    event_id: str
    actor: str
    action: str
    resource: str
    result: str
    delegation_id: Optional[str] = None
    details: Dict = field(default_factory=dict)
