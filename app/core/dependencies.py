"""
FastAPI dependencies.
"""
from typing import Dict, List
from app.agents.base import BaseAgent


# Registry to store all available agents
_agent_registry: Dict[str, BaseAgent] = {}


def register_agent(agent: BaseAgent) -> None:
    """
    Register an agent in the registry.
    
    Args:
        agent: The agent instance to register
    """
    _agent_registry[agent.name] = agent


def get_agent(agent_name: str) -> BaseAgent:
    """
    Get an agent from the registry.
    
    Args:
        agent_name: Name of the agent to retrieve
        
    Returns:
        The agent instance
        
    Raises:
        KeyError: If agent is not found
    """
    if agent_name not in _agent_registry:
        raise KeyError(f"Agent '{agent_name}' not found in registry")
    return _agent_registry[agent_name]


def list_all_agents() -> Dict[str, BaseAgent]:
    """
    Get all registered agents.
    
    Returns:
        Dictionary of all registered agents
    """
    return _agent_registry.copy()


def get_agent_names() -> List[str]:
    """
    Get list of all registered agent names.
    
    Returns:
        List of agent names
    """
    return list(_agent_registry.keys())

