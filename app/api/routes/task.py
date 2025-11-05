from typing import List
from fastapi import APIRouter, HTTPException
from app.models.schemas import Task, TaskCreate, TaskUpdate
from app.db import crud

router = APIRouter(
    prefix="/todo",
    tags=["todo", "task"]
)

@router.get("/", response_model=List[Task])
def list_tasks(user_id: str):
    tasks = crud.list_tasks(user_id)
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")
    return tasks

@router.get("/{task_id}", response_model=Task)
def read_task(task_id: int):
    task = crud.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/", response_model=int)
def create_task(task: TaskCreate):
    task_id = crud.create_task(task)
    task_id = 1
    if task_id is None:
        raise HTTPException(status_code=500, detail="Failed to create task")
    return task_id

@router.put("/{task_id}", response_model=bool)
def update_task(task_id: int, task_update: TaskUpdate):
    updated = crud.update_task(task_id, task_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found or update failed")
    return updated
