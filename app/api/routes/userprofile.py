from fastapi import APIRouter, HTTPException
from app.models.schemas import UserProfile, UserProfileCreate, UserProfileUpdate
from app.db import crud

router = APIRouter(
    prefix="/userprofile",
    tags=["userprofile"]
)

@router.get("/", response_model=list[UserProfile])
def list_user_profiles():
    profiles = crud.list_user_profiles()
    if not profiles:
        raise HTTPException(status_code=404, detail="No user profiles found")
    return profiles

@router.get("/{user_id}", response_model=UserProfile)
def read_user_profile(user_id: int):
    profile = crud.get_user_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    return profile

@router.post("/", response_model=int)
def create_user_profile(profile: UserProfileCreate):
    user_id = crud.create_user_profile(profile)
    if user_id is None:
        raise HTTPException(status_code=500, detail="Failed to create user profile")
    return user_id

@router.put("/{user_id}", response_model=bool)
def update_user_profile(user_id: int, profile_update: UserProfileUpdate):
    updated = crud.update_user_profile(user_id, profile_update.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="User profile not found or update failed")
    return updated
