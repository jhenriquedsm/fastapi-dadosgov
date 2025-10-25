from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional
from app.database.connection import get_db
from app.models import User, UserRole
from app.utils.security import decode_access_token
from app.schemas import TokenData

# OAuth2 scheme para autenticação
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Obtém o usuário atual a partir do token JWT
    
    Args:
        token: Token JWT
        db: Sessão do banco de dados
    
    Returns:
        Usuário autenticado
    
    Raises:
        HTTPException: Se o token for inválido ou o usuário não existir
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Decodifica o token
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    username: Optional[str] = payload.get("sub")
    if username is None:
        raise credentials_exception
    
    # Busca o usuário no banco
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo"
        )
    
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Verifica se o usuário está ativo
    
    Args:
        current_user: Usuário atual
    
    Returns:
        Usuário ativo
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo"
        )
    return current_user


def require_admin(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Verifica se o usuário é admin
    
    Args:
        current_user: Usuário atual
    
    Returns:
        Usuário admin
    
    Raises:
        HTTPException: Se o usuário não for admin
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores"
        )
    return current_user