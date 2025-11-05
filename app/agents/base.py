"""
Base agent class for LangGraph agents.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict
from langgraph.graph import StateGraph


class BaseAgent(ABC):
    """
    Base class for all LangGraph agents.
    """
    
    def __init__(self, name: str):
        """
        Initialize the base agent.
        
        Args:
            name: Name of the agent
        """
        self.name = name
        self.graph = None
        self._build_graph()
    
    @abstractmethod
    def _build_graph(self) -> None:
        """
        Build the LangGraph state graph for this agent.
        This method should be implemented by each specific agent.
        """
        pass
    
    @abstractmethod
    async def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invoke the agent with input data.
        
        Args:
            input_data: Input data for the agent
            
        Returns:
            Output data from the agent
        """
        pass
    
    def get_info(self) -> Dict[str, Any]:
        """
        Get information about this agent.
        
        Returns:
            Dictionary containing agent information
        """
        return {
            "name": self.name,
            "type": self.__class__.__name__,
            "description": self.__doc__ or "No description available"
        }

