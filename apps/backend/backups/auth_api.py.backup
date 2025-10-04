from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import timedelta
import uuid
import json

from app.models.database import get_db, User
from app.models.auth import UserLogin, Token, UserResponse
from app.core.auth import (
    get_password_hash, verify_password, create_access_token, 
    get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter()

@router.post("/register", response_model=Token)
async def register(request: Request, db: Session = Depends(get_db)):
    try:
        # Get raw request body
        body = await request.body()
        data = json.loads(body.decode('utf-8'))
        email = data.get('email')
        full_name = data.get('full_name')
        password = data.get('password')
        role = data.get('role', 'customer')
        
        print(f"DEBUG: Registering user: {email}")
        
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        user_id = str(uuid.uuid4())
        hashed_password = get_password_hash(password)
        
        db_user = User(
            id=user_id,
            email=email,
            full_name=full_name,
            hashed_password=hashed_password,
            role=role
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        print(f"DEBUG: User created: {db_user.id}")
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": email, "role": role},
            expires_delta=access_token_expires
        )
        
        user_response = UserResponse(
            id=db_user.id,
            email=db_user.email,
            full_name=db_user.full_name,
            role=db_user.role,
            is_active=db_user.is_active,
            created_at=db_user.created_at
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            user=user_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"DEBUG: ERROR in register: {e}")
        import traceback
        print(f"DEBUG: Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role},
        expires_delta=access_token_expires
    )
    
    user_response = UserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        is_active=user.is_active,
        created_at=user.created_at
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=user_response
    )

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role,
        is_active=current_user.is_active,
        created_at=current_user.created_at
    )

@router.get("/test")
async def test_auth():
    return {"message": "Auth router is working"}