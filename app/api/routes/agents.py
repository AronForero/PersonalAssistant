"""
Agent endpoints for LangGraph agents.
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.models.schemas import AgentRequest, AgentResponse, UserProfileBase
from app.core.dependencies import get_agent, get_agent_names
from app.db import crud

router = APIRouter()

@router.post("/agents/{agent_name}/invoke", response_model=AgentResponse)
async def invoke_agent(
    agent_name: str,
    request: AgentRequest
) -> AgentResponse:
    """
    Invoke a specific LangGraph agent.
    
    Args:
        agent_name: Name of the agent to invoke
        request: Input data for the agent
        
    Returns:
        AgentResponse: Response from the agent
    """
    try:
        agent = get_agent(agent_name)
        user_id = request.user_id
        user_profile = crud.get_user_profile(user_id)
        if not user_profile:
            default_profile = UserProfileBase(id=user_id)
            user_profile = crud.create_user_profile(default_profile)
            output = await agent.invoke(request.input)
        else:
            extended_prompt = user_profile.preferences + request.input
        
        return AgentResponse(
            agent_name=agent_name,
            output=output,
            metadata=request.config
        )
    except KeyError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error invoking agent: {str(e)}"
        )


@router.get("/agents", response_model=List[str])
async def list_agents() -> List[str]:
    """
    List all available agents.
    
    Returns:
        List of available agent names
    """
    return get_agent_names()


@router.get("/agents/{agent_name}/info")
async def get_agent_info(agent_name: str) -> Dict[str, Any]:
    """
    Get information about a specific agent.
    
    Args:
        agent_name: Name of the agent
        
    Returns:
        Dictionary containing agent information
    """
    try:
        agent = get_agent(agent_name)
        return agent.get_info()
    except KeyError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

