from typing import List
from fastapi import APIRouter, HTTPException
from app.db import crud
from app.db.models import Expense

router = APIRouter(
    prefix="/expense",
    tags=["expense"]
)

@router.get("/", response_model=List[Expense])
def list_expenses():
    expenses = crud.list_expenses()
    if expenses is None:
        raise HTTPException(status_code=500, detail="Failed to fetch expenses")
    return expenses
    

@router.get("/{expense_id}", response_model=Expense)
def get_expense(expense_id: int):
    expense = crud.get_expense(expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

@router.post("/", response_model=int)
def create_expense(expense: Expense):
    expense_id = crud.create_expense(expense)
    if expense_id is None:
        raise HTTPException(status_code=500, detail="Failed to create expense")
    return expense_id

@router.put("/{expense_id}", response_model=bool)
def update_expense(expense_id: int, update_data: dict):
    updated = crud.update_expense(expense_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Expense not found or update failed")
    return updated
