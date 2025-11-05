"""
CRUD operations using SQLAlchemy ORM.
"""
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, exc
from app.db.database import SessionLocal
from app.db.orm_models import UserProfileDB, TaskDB, ExpenseDB
from app.db.models import Task, Expense, UserProfile
from datetime import datetime, timezone, timedelta

# Colombia timezone (UTC-5, no daylight saving)
COLOMBIA_TZ = timezone(timedelta(hours=-5))
import json


def get_db_session() -> Session:
    """Get a database session."""
    return SessionLocal()


def list_tasks(user_id: str) -> List[Task]:
    """
    Retrieves all Tasks from the database for a specific user.

    Args:
        user_id (str): The Telegram ID of the user.

    Returns:
        List[Task]: A list of Task objects.
    """
    db = get_db_session()
    try:
        tasks_db = db.query(TaskDB).filter(TaskDB.user_id == user_id).all()
        tasks = []
        for task_db in tasks_db:
            tasks.append(Task(
                title=task_db.title,
                time_to_complete=task_db.time_to_complete,
                deadline=task_db.deadline,
                status=task_db.status,
                solutions=task_db.solutions or [],
                user_id=task_db.user_id,
                user=UserProfile(id=task_db.user.id, name=task_db.user.name, city=task_db.user.city,
                                state=task_db.user.state, country=task_db.user.country, job=task_db.user.job,
                                preferences=json.loads(task_db.user.preferences) if task_db.user.preferences else {},
                                interests=task_db.user.interests or [],
                                created_at=task_db.user.created_at),
                created_at=task_db.created_at,
                updated_at=task_db.updated_at
            ))
        return tasks
    except Exception as e:
        print(f"Error retrieving tasks: {e}")
        return []
    finally:
        db.close()


def get_task(task_id: int) -> Optional[Task]:
    """
    Retrieves a Task from the database by its ID.

    Args:
        task_id (int): The ID of the task to retrieve.

    Returns:
        Task or None: A Task object if found, else None.
    """
    db = get_db_session()
    try:
        task_db = db.query(TaskDB).filter(TaskDB.id == task_id).first()
        if not task_db:
            return None
        
        return Task(
            title=task_db.title,
            time_to_complete=task_db.time_to_complete,
            deadline=task_db.deadline,
            status=task_db.status,
            solutions=task_db.solutions or [],
            user_id=task_db.user_id,
            user=UserProfile(id=task_db.user.id, name=task_db.user.name, city=task_db.user.city,
                            state=task_db.user.state, country=task_db.user.country, job=task_db.user.job,
                            preferences=json.loads(task_db.user.preferences) if task_db.user.preferences else {},
                            interests=task_db.user.interests or [],
                            created_at=task_db.user.created_at),
            created_at=task_db.created_at,
            updated_at=task_db.updated_at
        )
    except Exception as e:
        print(f"Error retrieving task: {e}")
        return None
    finally:
        db.close()


def update_task(task_id: int, updated_task: Task) -> bool:
    """
    Updates a Task in the database by its ID.

    Args:
        task_id (int): The ID of the task to update.
        updated_task (Task): A Task object containing new values.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    db = get_db_session()
    try:
        task_db = db.query(TaskDB).filter(TaskDB.id == task_id).first()
        if not task_db:
            print("Update failed: Task not found.")
            return False
        
        task_db.title = updated_task.title
        task_db.time_to_complete = updated_task.time_to_complete
        task_db.deadline = updated_task.deadline
        task_db.status = updated_task.status
        task_db.solutions = updated_task.solutions
        task_db.updated_at = datetime.now(COLOMBIA_TZ)
        
        db.commit()
        print(f"Task with ID {task_id} updated.")
        return True
    except Exception as e:
        print(f"Error updating task: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def create_task(task: Task) -> Optional[int]:
    """
    Inserts a Task into the database.

    Args:
        task (Task): The Task object to insert.

    Returns:
        int or None: The new task's ID if successful, else None.
    """
    db = get_db_session()
    try:
        task_db = TaskDB(
            title=task.title,
            time_to_complete=task.time_to_complete,
            deadline=task.deadline,
            status=task.status,
            solutions=task.solutions or [],
            user_id=task.user_id,
            created_at=task.created_at or datetime.now(COLOMBIA_TZ),
            updated_at=task.updated_at or datetime.now(COLOMBIA_TZ)
        )
        db.add(task_db)
        db.commit()
        db.refresh(task_db)
        print(f"Task created with ID: {task_db.id}")
        return task_db.id
    except Exception as e:
        print(f"Error inserting task: {e}")
        db.rollback()
        return None
    finally:
        db.close()


def get_expense(expense_id: int) -> Optional[Expense]:
    """
    Retrieves an Expense from the database by its ID.

    Args:
        expense_id (int): The ID of the expense to retrieve.

    Returns:
        Expense or None: An Expense object if found, else None.
    """
    db = get_db_session()
    try:
        expense_db = db.query(ExpenseDB).filter(ExpenseDB.id == expense_id).first()
        if not expense_db:
            return None
        
        return Expense(
            description=expense_db.description,
            amount=expense_db.amount,
            category=expense_db.category,
            type=expense_db.type,
            user_id=expense_db.user_id,
            created_at=expense_db.created_at,
            updated_at=expense_db.updated_at
        )
    except Exception as e:
        print(f"Error retrieving expense: {e}")
        return None
    finally:
        db.close()


def create_expense(expense: Expense) -> Optional[int]:
    """
    Inserts an Expense into the database.

    Args:
        expense (Expense): The Expense object to insert.

    Returns:
        int or None: The new expense's ID if successful, else None.
    """
    db = get_db_session()
    try:
        expense_db = ExpenseDB(
            description=expense.description,
            amount=expense.amount,
            category=expense.category,
            type=expense.type,
            user_id=expense.user_id,
            created_at=expense.created_at or datetime.now(COLOMBIA_TZ),
            updated_at=expense.updated_at or datetime.now(COLOMBIA_TZ)
        )
        db.add(expense_db)
        db.commit()
        db.refresh(expense_db)
        print(f"Expense created with ID: {expense_db.id}")
        return expense_db.id
    except Exception as e:
        print(f"Error inserting expense: {e}")
        db.rollback()
        return None
    finally:
        db.close()


def update_expense(expense_id: int, update_data: Dict[str, Any]) -> bool:
    """
    Updates an Expense in the database.

    Args:
        expense_id (int): The ID of the expense to update.
        update_data (dict): The fields to update with their new values.

    Returns:
        bool: True if update was successful, False otherwise.
    """
    db = get_db_session()
    try:
        expense_db = db.query(ExpenseDB).filter(ExpenseDB.id == expense_id).first()
        if not expense_db:
            print("Expense not found.")
            return False
        
        for key, value in update_data.items():
            if hasattr(expense_db, key):
                setattr(expense_db, key, value)
        
        expense_db.updated_at = datetime.now(COLOMBIA_TZ)
        db.commit()
        print(f"Expense {expense_id} updated.")
        return True
    except Exception as e:
        print(f"Error updating expense: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def list_user_profiles() -> List[UserProfile]:
    """
    Retrieves all UserProfiles from the database.

    Returns:
        List[UserProfile]: A list of UserProfile objects.
    """
    db = get_db_session()
    try:
        profiles_db = db.query(UserProfileDB).all()
        if not profiles_db:
            return []
        
        profiles = []
        for profile in profiles_db:
            profiles.append(
                UserProfile(
                    id=profile.id,
                    name=profile.name,
                    city=profile.city,
                    state=profile.state,
                    country=profile.country,
                    job=profile.job,
                    interestes=profile.interests,
                    preferences=profile.preferences
                )
            )
        
        return profiles
    except Exception as e:
        print(f"Error retrieving user profiles: {e}")
        return []
    finally:
        db.close()


def get_user_profile(user_id: str) -> Optional[UserProfile]:
    """
    Retrieves a UserProfile from the database by its ID.

    Args:
        user_id (str): The Telegram ID of the user.

    Returns:
        UserProfile or None: The user profile if found, else None.
    """
    db = get_db_session()
    try:
        profile_db = db.query(UserProfileDB).filter(UserProfileDB.id == user_id).first()
        if not profile_db:
            return None
        
        preferences = json.loads(profile_db.preferences) if profile_db.preferences else {}
        
        return UserProfile(
            id=profile_db.id,
            name=profile_db.name,
            city=profile_db.city,
            state=profile_db.state,
            country=profile_db.country,
            job=profile_db.job,
            preferences=preferences,
            interests=profile_db.interests or [],
            created_at=profile_db.created_at
        )
    except Exception as e:
        print(f"Error retrieving user profile: {e}")
        return None
    finally:
        db.close()


def create_user_profile(profile: UserProfile) -> Optional[str]:
    """
    Inserts a UserProfile into the database.

    Args:
        profile (UserProfile): The UserProfile object to insert.

    Returns:
        str or None: The user's ID if successful, else None.
    """
    db = get_db_session()
    try:
        profile_db = UserProfileDB(
            id=profile.id,
            name=profile.name,
            city=profile.city,
            state=profile.state,
            country=profile.country,
            job=profile.job,
            preferences=json.dumps(profile.preferences) if isinstance(profile.preferences, dict) else profile.preferences,
            interests=profile.interests or [],
            created_at=profile.created_at or datetime.now(COLOMBIA_TZ)
        )
        db.add(profile_db)
        db.commit()
        db.refresh(profile_db)
        print(f"UserProfile created with ID: {profile_db.id}")
        return profile_db.id
    except Exception as e:
        print(f"Error inserting user profile: {e}")
        db.rollback()
        return None
    finally:
        db.close()


def update_user_profile(user_id: str, update_data: Dict[str, Any]) -> bool:
    """
    Updates a UserProfile in the database by user ID.

    Args:
        user_id (str): The Telegram ID of the user.
        update_data (dict): The fields to update.

    Returns:
        bool: True if update was successful, False otherwise.
    """
    db = get_db_session()
    try:
        profile_db = db.query(UserProfileDB).filter(UserProfileDB.id == user_id).first()
        if not profile_db:
            print("UserProfile not found.")
            return False
        
        for key, value in update_data.items():
            if hasattr(profile_db, key):
                # For JSON fields, serialize them
                if key in ["preferences"]:
                    setattr(profile_db, key, json.dumps(value) if isinstance(value, dict) else value)
                elif key in ["interests"]:
                    setattr(profile_db, key, value)
                else:
                    setattr(profile_db, key, value)
        
        db.commit()
        print(f"UserProfile {user_id} updated.")
        return True
    except Exception as e:
        print(f"Error updating user profile: {e}")
        db.rollback()
        return False
    finally:
        db.close()
