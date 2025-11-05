from pydantic import BaseModel, Field
from typing import Literal, TypedDict, Optional
from datetime import datetime

class UserProfile(BaseModel):
    id: str = Field(description="Unique Telegram identifier for the user")
    name: Optional[str] = Field(default=None, description="The name of the user")
    city: Optional[str] = Field(default=None, description="The city of the user")
    state: Optional[str] = Field(default=None, description="The state of the user")
    country: Optional[str] = Field(default=None, description="The country of the user")
    job: Optional[str] = Field(default=None, description="The job of the user")
    preferences: Optional[str] = Field(default=None, description="The preferences of the user")
    interests: list[str] = Field(default_factory=list, description="The interests of the user")
    created_at: datetime

class Task(BaseModel):
    title: str = Field(description="The title of the task")
    time_to_complete: Optional[int] = Field(default=None, description="The time to complete the task in minutes")
    deadline: Optional[datetime] = Field(default=None, description="The deadline of the task")
    status: Literal["not started", "in progress", "done", "archived"] = Field(
        description="Current status of the task",
        default="not started"
    )
    solutions: list[str] = Field(
        description="List of specific, actionable solutions (e.g., specific ideas, service providers, or concrete options relevant to completing the task)",
        min_items=1,
        default_factory=list
    )
    user_id: str = Field(description="The Telegram ID of the user associated with the task")
    user: UserProfile = Field(description="The user associated with the task")
    created_at: datetime = Field(default_factory=datetime.now, description="The creation date of the task")
    updated_at: datetime = Field(default_factory=datetime.now, description="The last update date of the task")

class Expense(BaseModel):
    description: str = Field(description="The description of the expense")
    amount: float = Field(description="The amount of the expense")
    category: Literal["food", "transport", "housing", "utilities", "entertainment", "other"] = Field(
        description="The category of the expense",
        default="other"
    )
    type: Literal["Personal", "Shared"] = Field(
        description="The type of the expense (Personal or Couple shared)",
        default="Personal"
    )
    user_id: str = Field(description="The Telegram ID of the user associated with the expense")
    created_at: datetime = Field(default_factory=datetime.now, description="The creation date of the expense")
    updated_at: datetime = Field(default_factory=datetime.now, description="The last update date of the expense")

class UpdateMemory(TypedDict):
    update_type: Literal["task", "expense", "user_profile"]
