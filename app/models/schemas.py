"""
Pydantic schemas for API requests and responses.
"""
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional
from datetime import datetime


class TaskBase(BaseModel):
    title: str
    time_to_complete: Optional[int] = None
    deadline: Optional[datetime] = None
    status: Optional[str] = None
    solutions: Optional[List[str]] = []
    user_id: str = None


class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class Task(TaskBase):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class ExpenseBase(BaseModel):
    description: str
    amount: float
    category: Optional[str] = None
    type: Optional[str] = None

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseUpdate(ExpenseBase):
    pass

class Expense(ExpenseBase):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class UserProfileBase(BaseModel):
    id: str = Field(description="Unique Telegram identifier for the user")
    name: str
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    job: Optional[str] = None
    preferences: Optional[str] = None
    interests: Optional[List[str]] = []

class UserProfileCreate(UserProfileBase):
    pass

class UserProfileUpdate(UserProfileBase):
    pass

class UserProfile(UserProfileBase):
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class AgentRequest(BaseModel):
    user_id: str = Field(description="Telegram ID of the user making the agent request")
    input: str = Field(description="Input prompt or query to the agent")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Optional extra context for agent")
    history: Optional[List[Dict[str, Any]]] = Field(default_factory=list, description="Optional chat or message history")

class AgentResponse(BaseModel):
    output: str = Field(description="The main output text from the agent")
    actions: Optional[List[Dict[str, Any]]] = Field(default_factory=list, description="List of actions the agent took or recommends, if any")
    info: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Any additional agent information or metadata")
