"""
Application startup configuration.
This module handles initialization tasks like registering agents.
"""
from app.core.dependencies import register_agent
# Import agents here as you create them
# from app.agents.example_agent import ExampleAgent


def register_all_agents() -> None:
    """
    Register all available agents.
    Add agent registrations here as you create new agents.
    """
    # Example: Register the example agent
    # example_agent = ExampleAgent()
    # register_agent(example_agent)
    
    pass

