from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas import ProdutoCreate, ProdutoUpdate, ProdutoResponse, ProdutoListResponse
from app.services import ProdutoService
from app.utils.dependencies import get_current_active_user, require_admin
from app.models import User

router = APIRouter(prefix="/produtos", tags=["Produtos"])


@router.get("", response_model=ProdutoListResponse)
def list_produtos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Lista todos os produtos (tipos de combustível)
    """
    items = ProdutoService.get_all(db)
    return ProdutoListResponse(items=items, total=len(items))


@router.get("/{produto_id}", response_model=ProdutoResponse)
def get_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Busca um produto específico por ID
    """
    return ProdutoService.get_by_id(db, produto_id)


@router.post("", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def create_produto(
    produto_data: ProdutoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Cria um novo produto (apenas admin)
    
    - **nome**: Nome do produto (ex: GASOLINA, ETANOL, DIESEL S10)
    - **descricao**: Descrição opcional do produto
    """
    return ProdutoService.create(db, produto_data)


@router.put("/{produto_id}", response_model=ProdutoResponse)
def update_produto(
    produto_id: int,
    produto_data: ProdutoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Atualiza um produto existente (apenas admin)
    """
    return ProdutoService.update(db, produto_id, produto_data)


@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Deleta um produto (apenas admin)
    """
    ProdutoService.delete(db, produto_id)
    return None