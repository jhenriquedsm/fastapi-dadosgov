from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional
from app.models import Revenda
from app.schemas import RevendaCreate, RevendaUpdate


class RevendaService:
    """Serviço de gestão de revendas"""
    
    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        estado: Optional[str] = None,
        municipio: Optional[str] = None,
        bandeira: Optional[str] = None
    ) -> tuple[list[Revenda], int]:
        """Lista revendas com filtros opcionais"""
        query = db.query(Revenda)
        
        if estado:
            query = query.filter(Revenda.estado == estado.upper())
        if municipio:
            query = query.filter(Revenda.municipio.ilike(f"%{municipio}%"))
        if bandeira:
            query = query.filter(Revenda.bandeira.ilike(f"%{bandeira}%"))
        
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        
        return items, total
    
    @staticmethod
    def get_by_id(db: Session, revenda_id: int) -> Revenda:
        """Busca revenda por ID"""
        revenda = db.query(Revenda).filter(Revenda.id == revenda_id).first()
        if not revenda:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Revenda não encontrada"
            )
        return revenda
    
    @staticmethod
    def create(db: Session, revenda_data: RevendaCreate) -> Revenda:
        """Cria uma nova revenda"""
        # Verifica se CNPJ já existe
        existing = db.query(Revenda).filter(Revenda.cnpj == revenda_data.cnpj).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CNPJ já cadastrado"
            )
        
        db_revenda = Revenda(**revenda_data.model_dump())
        db.add(db_revenda)
        db.commit()
        db.refresh(db_revenda)
        
        return db_revenda
    
    @staticmethod
    def update(db: Session, revenda_id: int, revenda_data: RevendaUpdate) -> Revenda:
        """Atualiza uma revenda"""
        revenda = RevendaService.get_by_id(db, revenda_id)
        
        update_data = revenda_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(revenda, field, value)
        
        db.commit()
        db.refresh(revenda)
        
        return revenda
    
    @staticmethod
    def delete(db: Session, revenda_id: int) -> None:
        """Deleta uma revenda"""
        revenda = RevendaService.get_by_id(db, revenda_id)
        db.delete(revenda)
        db.commit()