from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.models import domain as models
from app.core import security
from app.core.config import settings
from app.api.dependencies import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register-admin")
def register_admin(username: str, password: str, db: Session = Depends(get_db)):
    """Initial setup endpoint to register an administrative user."""
    # Check if user already exists
    existing_user = db.query(models.User).filter(models.User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Hash the password and save
    hashed_pass = security.get_password_hash(password)
    new_user = models.User(username=username, hashed_password=hashed_pass, role="admin")
    db.add(new_user)
    db.commit()
    
    return {"message": f"Admin user '{username}' registered successfully."}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Standard OAuth2 compatible token login, returning a JWT access token."""
    # Lookup user
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create the access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username, "role": user.role}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}