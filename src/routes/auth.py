from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.auth import authenticate_user, create_user, get_user
from src.database import get_db
from src.schemas import UserCreate, Token, User
from src.security import create_access_token

router = APIRouter()


@router.post("/token", response_model=Token, tags=["Authentication"],
             description="Generate a JWT token for user authentication.")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = await authenticate_user(db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# src/routes/auth.py
@router.post("/register", response_model=User, tags=["Authentication"], description="Register a new user.")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user(db, user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,  # Ensure this status code is 400
            detail="Username already registered",
        )
    db_user = create_user(db=db, user=user)
    return db_user