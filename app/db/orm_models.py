"""
SQLAlchemy ORM models for database tables.
These are separate from Pydantic models which are used for API validation.
"""
from sqlalchemy import Column, String, Integer, Float, DateTime, Text, ARRAY, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta

# Colombia timezone (UTC-5, no daylight saving)
COLOMBIA_TZ = timezone(timedelta(hours=-5))

Base = declarative_base()


class UserProfileDB(Base):
    """User profile database table."""
    __tablename__ = "user_profiles"
    
    id = Column(String, primary_key=True, index=True)  # Telegram ID
    name = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    country = Column(String, nullable=True)
    job = Column(String, nullable=True)
    preferences = Column(Text, nullable=True)
    supervisor_prompt_override = Column(Text, nullable=True)
    interests = Column(ARRAY(String), default=[])
    created_at = Column(DateTime, default=lambda: datetime.now(COLOMBIA_TZ))
    
    # Relationships
    tasks = relationship("TaskDB", back_populates="user")
    expenses = relationship("ExpenseDB", back_populates="user")


class TaskDB(Base):
    """Task database table."""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    time_to_complete = Column(Integer, nullable=True)
    deadline = Column(DateTime, nullable=True)
    status = Column(String, default="not started")
    solutions = Column(ARRAY(String), default=[])
    user_id = Column(String, ForeignKey("user_profiles.id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(COLOMBIA_TZ))
    updated_at = Column(DateTime, default=lambda: datetime.now(COLOMBIA_TZ), onupdate=lambda: datetime.now(COLOMBIA_TZ))
    
    # Relationship
    user = relationship("UserProfileDB", back_populates="tasks")


class ExpenseDB(Base):
    """Expense database table."""
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, default="other")
    type = Column(String, default="Personal")
    user_id = Column(String, ForeignKey("user_profiles.id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(COLOMBIA_TZ))
    updated_at = Column(DateTime, default=lambda: datetime.now(COLOMBIA_TZ), onupdate=lambda: datetime.now(COLOMBIA_TZ))
    
    # Relationship
    user = relationship("UserProfileDB", back_populates="expenses")

