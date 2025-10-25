from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas import UserCreate, UserLogin, UserResponse, Token
from app.services import AuthService

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Registra um novo usuário
    
    - **username**: Nome de usuário único (3-50 caracteres)
    - **email**: Email válido e único
    - **password**: Senha (mínimo 6 caracteres)
    - **role**: Papel do usuário (admin ou leitor)
    """
    return AuthService.register_user(db, user_data)


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Autentica um usuário e retorna um token JWT
    
    - **username**: Nome de usuário
    - **password**: Senha
    
    Retorna um token de acesso que deve ser incluído no header Authorization
    como "Bearer {token}" para acessar endpoints protegidos.
    """
    login_data = UserLogin(username=form_data.username, password=form_data.password)
    return AuthService.authenticate_user(db, login_data)