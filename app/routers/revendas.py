from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database.connection import get_db
from app.schemas import RevendaCreate, RevendaUpdate, RevendaResponse, RevendaListResponse
from app.services import RevendaService
from app.utils.dependencies import get_current_active_user, require_admin
from app.models import User

router = APIRouter(prefix="/revendas", tags=["Revendas"])


@router.get("", response_model=RevendaListResponse)
def list_revendas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    estado: Optional[str] = Query(None, max_length=2),
    municipio: Optional[str] = Query(None, max_length=100),
    bandeira: Optional[str] = Query(None, max_length=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Lista todas as revendas com filtros opcionais
    
    - **skip**: Número de registros a pular (paginação)
    - **limit**: Número máximo de registros a retornar
    - **estado**: Filtrar por UF (ex: SP, RJ, MG)
    - **municipio**: Filtrar por município (busca parcial)
    - **bandeira**: Filtrar por bandeira do posto
    """
    items, total = RevendaService.get_all(db, skip, limit, estado, municipio, bandeira)
    return RevendaListResponse(items=items, total=total, skip=skip, limit=limit)


@router.get("/{revenda_id}", response_model=RevendaResponse)
def get_revenda(
    revenda_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Busca uma revenda específica por ID
    """
    return RevendaService.get_by_id(db, revenda_id)


@router.post("", response_model=RevendaResponse, status_code=status.HTTP_201_CREATED)
def create_revenda(
    revenda_data: RevendaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Cria uma nova revenda (apenas admin)
    
    - **cnpj**: CNPJ no formato XX.XXX.XXX/XXXX-XX
    - **nome**: Nome da revenda
    - **municipio**: Município
    - **estado**: UF com 2 caracteres
    - **regiao_sigla**: Sigla da região (N, NE, CO, SE, S)
    - **bandeira**: Bandeira do posto (opcional)
    """
    return RevendaService.create(db, revenda_data)


@router.put("/{revenda_id}", response_model=RevendaResponse)
def update_revenda(
    revenda_id: int,
    revenda_data: RevendaUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Atualiza uma revenda existente (apenas admin)
    """
    return RevendaService.update(db, revenda_id, revenda_data)


@router.delete("/{revenda_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_revenda(
    revenda_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Deleta uma revenda (apenas admin)
    """
    RevendaService.delete(db, revenda_id)
    return None