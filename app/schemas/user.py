from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from app.models.user import UserRole


# Schemas de entrada
class UserCreate(BaseModel):
    """Schema para criação de usuário"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: UserRole = UserRole.LEITOR


class UserLogin(BaseModel):
    """Schema para login"""
    username: str
    password: str


class UserUpdate(BaseModel):
    """Schema para atualização de usuário"""
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


# Schemas de saída
class UserResponse(BaseModel):
    """Schema de resposta de usuário"""
    id: int
    username: str
    email: str
    role: UserRole
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Token schemas
class Token(BaseModel):
    """Schema de token JWT"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema de dados do token"""
    username: Optional[str] = None
    role: Optional[str] = None