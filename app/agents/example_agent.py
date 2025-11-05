"""
Example LangGraph agent implementation.
This file serves as a template for creating new agents.
"""
from typing import Dict, Any, TypedDict
from langgraph.graph import StateGraph, END
from app.agents.base import BaseAgent


class AgentState(TypedDict):
    """State schema for the example agent."""
    messages: list
    input: str
    output: str


class ExampleAgent(BaseAgent):
    """
    Example agent implementation.
    Replace this with your actual agent logic.
    """
    
    def __init__(self):
        """Initialize the example agent."""
        super().__init__(name="example_agent")
    
    def _build_graph(self) -> None:
        """
        Build the LangGraph state graph.
        This is a simple example - replace with your actual graph logic.
        """
        # Define the graph
        workflow = StateGraph(AgentState)
        
        # Add nodes (these are placeholder functions)
        workflow.add_node("process_input", self._process_input)
        workflow.add_node("generate_output", self._generate_output)
        
        # Define edges
        workflow.set_entry_point("process_input")
        workflow.add_edge("process_input", "generate_output")
        workflow.add_edge("generate_output", END)
        
        # Compile the graph
        self.graph = workflow.compile()
    
    def _process_input(self, state: AgentState) -> AgentState:
        """
        Process the input state.
        
        Args:
            state: Current state
            
        Returns:
            Updated state
        """
        # TODO: Implement input processing logic
        return state
    
    def _generate_output(self, state: AgentState) -> AgentState:
        """
        Generate output from processed input.
        
        Args:
            state: Current state
            
        Returns:
            Updated state with output
        """
        # TODO: Implement output generation logic
        state["output"] = f"Processed: {state.get('input', '')}"
        return state
    
    async def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invoke the agent with input data.
        
        Args:
            input_data: Input data for the agent
            
        Returns:
            Output data from the agent
        """
        # Prepare initial state
        initial_state: AgentState = {
            "messages": [],
            "input": input_data.get("input", ""),
            "output": ""
        }
        
        # Run the graph
        result = await self.graph.ainvoke(initial_state)
        
        # Return the output
        return {
            "output": result.get("output", ""),
            "state": result
        }

