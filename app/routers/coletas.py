from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional
from app.database.connection import get_db
from app.schemas import ColetaPrecoCreate, ColetaPrecoUpdate, ColetaPrecoResponse, ColetaPrecoListResponse
from app.services import ColetaService
from app.utils.dependencies import get_current_active_user, require_admin
from app.models import User

router = APIRouter(prefix="/coletas", tags=["Coletas de Preço"])


@router.get("", response_model=ColetaPrecoListResponse)
def list_coletas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    estado: Optional[str] = Query(None, max_length=2),
    municipio: Optional[str] = Query(None, max_length=100),
    produto: Optional[str] = Query(None, max_length=50),
    data_inicio: Optional[date] = Query(None),
    data_fim: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Lista todas as coletas de preço com filtros opcionais
    
    - **skip**: Número de registros a pular (paginação)
    - **limit**: Número máximo de registros a retornar
    - **estado**: Filtrar por UF (ex: SP, RJ, MG)
    - **municipio**: Filtrar por município
    - **produto**: Filtrar por tipo de combustível (ex: GASOLINA, ETANOL)
    - **data_inicio**: Data inicial do período
    - **data_fim**: Data final do período
    """
    items, total = ColetaService.get_all(
        db, skip, limit, estado, municipio, produto, data_inicio, data_fim
    )
    return ColetaPrecoListResponse(items=items, total=total, skip=skip, limit=limit)


@router.get("/{coleta_id}", response_model=ColetaPrecoResponse)
def get_coleta(
    coleta_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Busca uma coleta específica por ID
    """
    return ColetaService.get_by_id(db, coleta_id)


@router.post("", response_model=ColetaPrecoResponse, status_code=status.HTTP_201_CREATED)
def create_coleta(
    coleta_data: ColetaPrecoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Registra uma nova coleta de preço (apenas admin)
    
    - **data_coleta**: Data da coleta
    - **valor_venda**: Preço de venda (R$)
    - **valor_compra**: Preço de compra (opcional)
    - **unidade_medida**: Unidade (ex: R$/litro, R$/kg)
    - **revenda_id**: ID da revenda
    - **produto_id**: ID do produto
    """
    return ColetaService.create(db, coleta_data)


@router.put("/{coleta_id}", response_model=ColetaPrecoResponse)
def update_coleta(
    coleta_id: int,
    coleta_data: ColetaPrecoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Atualiza uma coleta existente (apenas admin)
    """
    return ColetaService.update(db, coleta_id, coleta_data)


@router.delete("/{coleta_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_coleta(
    coleta_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Deleta uma coleta (apenas admin)
    """
    ColetaService.delete(db, coleta_id)
    return None