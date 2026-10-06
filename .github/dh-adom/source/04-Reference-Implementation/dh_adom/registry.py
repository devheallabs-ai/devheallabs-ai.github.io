from .models import Agent

class AgentRegistry:
    def __init__(self):
        self._agents = {}

    def register(self, agent: Agent):
        if agent.agent_id in self._agents:
            raise ValueError(f"Duplicate agent: {agent.agent_id}")
        self._agents[agent.agent_id] = agent

    def get(self, agent_id: str) -> Agent:
        return self._agents[agent_id]

    def all(self):
        return list(self._agents.values())

    def feature_owner(self, feature: str):
        matches = [a for a in self._agents.values() if a.type.value == "FEATURE" and a.feature == feature]
        if len(matches) != 1:
            raise ValueError(f"Expected exactly one owner for feature {feature}, found {len(matches)}")
        return matches[0]
