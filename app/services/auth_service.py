from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import timedelta
from app.models import User
from app.schemas import UserCreate, UserLogin, Token
from app.utils.security import verify_password, get_password_hash, create_access_token
from app.config import settings


class AuthService:
    """Serviço de autenticação"""
    
    @staticmethod
    def register_user(db: Session, user_data: UserCreate) -> User:
        """
        Registra um novo usuário
        
        Args:
            db: Sessão do banco
            user_data: Dados do usuário
        
        Returns:
            Usuário criado
        
        Raises:
            HTTPException: Se username ou email já existirem
        """
        # Verifica se username já existe
        if db.query(User).filter(User.username == user_data.username).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username já cadastrado"
            )
        
        # Verifica se email já existe
        if db.query(User).filter(User.email == user_data.email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado"
            )
        
        # Cria o usuário
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            role=user_data.role,
            is_active=1
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user
    
    @staticmethod
    def authenticate_user(db: Session, login_data: UserLogin) -> Token:
        """
        Autentica um usuário e retorna token JWT
        
        Args:
            db: Sessão do banco
            login_data: Credenciais de login
        
        Returns:
            Token JWT
        
        Raises:
            HTTPException: Se credenciais forem inválidas
        """
        # Busca usuário
        user = db.query(User).filter(User.username == login_data.username).first()
        
        if not user or not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuário inativo"
            )
        
        # Cria token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username, "role": user.role.value},
            expires_delta=access_token_expires
        )
        
        return Token(access_token=access_token, token_type="bearer")