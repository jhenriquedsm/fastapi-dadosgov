from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import date
from typing import Optional
from app.models import ColetaPreco, Revenda, Produto
from app.schemas import ColetaPrecoCreate, ColetaPrecoUpdate


class ColetaService:
    """Serviço de gestão de coletas de preço"""
    
    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        estado: Optional[str] = None,
        municipio: Optional[str] = None,
        produto: Optional[str] = None,
        data_inicio: Optional[date] = None,
        data_fim: Optional[date] = None
    ) -> tuple[list[ColetaPreco], int]:
        """Lista coletas com filtros opcionais"""
        query = db.query(ColetaPreco).join(Revenda).join(Produto)
        
        if estado:
            query = query.filter(Revenda.estado == estado.upper())
        if municipio:
            query = query.filter(Revenda.municipio.ilike(f"%{municipio}%"))
        if produto:
            query = query.filter(Produto.nome == produto.upper())
        if data_inicio:
            query = query.filter(ColetaPreco.data_coleta >= data_inicio)
        if data_fim:
            query = query.filter(ColetaPreco.data_coleta <= data_fim)
        
        total = query.count()
        items = query.order_by(ColetaPreco.data_coleta.desc()).offset(skip).limit(limit).all()
        
        return items, total
    
    @staticmethod
    def get_by_id(db: Session, coleta_id: int) -> ColetaPreco:
        """Busca coleta por ID"""
        coleta = db.query(ColetaPreco).filter(ColetaPreco.id == coleta_id).first()
        if not coleta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Coleta não encontrada"
            )
        return coleta
    
    @staticmethod
    def create(db: Session, coleta_data: ColetaPrecoCreate) -> ColetaPreco:
        """Cria uma nova coleta de preço"""
        # Verifica se revenda existe
        revenda = db.query(Revenda).filter(Revenda.id == coleta_data.revenda_id).first()
        if not revenda:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Revenda não encontrada"
            )
        
        # Verifica se produto existe
        produto = db.query(Produto).filter(Produto.id == coleta_data.produto_id).first()
        if not produto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produto não encontrado"
            )
        
        db_coleta = ColetaPreco(**coleta_data.model_dump())
        db.add(db_coleta)
        db.commit()
        db.refresh(db_coleta)
        
        return db_coleta
    
    @staticmethod
    def update(db: Session, coleta_id: int, coleta_data: ColetaPrecoUpdate) -> ColetaPreco:
        """Atualiza uma coleta"""
        coleta = ColetaService.get_by_id(db, coleta_id)
        
        update_data = coleta_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(coleta, field, value)
        
        db.commit()
        db.refresh(coleta)
        
        return coleta
    
    @staticmethod
    def delete(db: Session, coleta_id: int) -> None:
        """Deleta uma coleta"""
        coleta = ColetaService.get_by_id(db, coleta_id)
        db.delete(coleta)
        db.commit()