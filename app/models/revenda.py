from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.connection import Base


class Revenda(Base):
    """Modelo de Revenda (Posto de Combustível)"""
    __tablename__ = "revendas"
    
    id = Column(Integer, primary_key=True, index=True)
    cnpj = Column(String(18), unique=True, index=True, nullable=False)
    nome = Column(String(200), nullable=False)
    municipio = Column(String(100), nullable=False, index=True)
    estado = Column(String(2), nullable=False, index=True)
    regiao_sigla = Column(String(2), nullable=False, index=True)
    bandeira = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamento
    coletas = relationship("ColetaPreco", back_populates="revenda", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Revenda(id={self.id}, nome='{self.nome}', municipio='{self.municipio}', estado='{self.estado}')>"