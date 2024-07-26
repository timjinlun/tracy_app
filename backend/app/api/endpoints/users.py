from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.user import User, UserCreate
from app.crud.crud_user import create_user, get_user_by_email

router = APIRouter()

@router.post("/", response_model=User)
def create_user_route(user: UserCreate, db: Session = Depends(deps.get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)