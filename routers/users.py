from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
from get_user import get_current_user  

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=schemas.User)
def get_current_user_profile(
    current_user: models.User = Depends(get_current_user)
):
    """
    Returns the currently authenticated user's profile.
    """
    return current_user


@router.get("/", response_model=list[schemas.User])
def get_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Returns all users.
    Later, you could restrict this to admins only.
    """
    return db.query(models.User).all()
