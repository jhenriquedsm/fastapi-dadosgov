from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.connection import Base


class Produto(Base):
    """Modelo de Produto (Tipo de Combustível)"""
    __tablename__ = "produtos"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), unique=True, index=True, nullable=False)
    descricao = Column(String(200), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamento
    coletas = relationship("ColetaPreco", back_populates="produto", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Produto(id={self.id}, nome='{self.nome}')>"