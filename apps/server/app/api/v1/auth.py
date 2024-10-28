from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserResponse
from app.api.deps import get_current_active_user  # 添加这行导入

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user_in: UserCreate) -> Any:
    """
    注册新用户
    """
    # 检查用户名是否已存在
    user = await User.find_one({"username": user_in.username})
    if user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    
    # 检查邮箱是否已存在
    user = await User.find_one({"email": user_in.email})
    if user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # 创建新用户
    user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password)
    )
    await user.insert()
    
    # 确保返回的是字符串形式的id
    return UserResponse(
        id=str(user.id),
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at
    )

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    OAuth2 compatible token login
    """
    user = await User.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=str(user.id), expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/test-token", response_model=UserResponse)  # 改为 GET 请求
async def test_token(current_user: User = Depends(get_current_active_user)) -> Any:
    """
    测试token是否有效
    """
    return current_user

# 在文件末尾添加
@router.post("/create-superuser", response_model=UserResponse)
async def create_superuser(user_in: UserCreate) -> Any:
    """
    创建超级用户 (仅在没有任何用户时可用)
    """
    # 检查是否已存在用户
    users_count = await User.count()
    if users_count > 0:
        raise HTTPException(
            status_code=400,
            detail="Superuser can only be created when there are no users in the system"
        )
    
    # 创建超级用户
    user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        is_superuser=True
    )
    await user.insert()
    
    return UserResponse(
        id=str(user.id),
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at
    )
