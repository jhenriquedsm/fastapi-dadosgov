from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.connection import Base


class ColetaPreco(Base):
    """Modelo de Coleta de Preço"""
    __tablename__ = "coletas_preco"
    
    id = Column(Integer, primary_key=True, index=True)
    data_coleta = Column(Date, nullable=False, index=True)
    valor_venda = Column(Float, nullable=False)
    valor_compra = Column(Float, nullable=True)
    unidade_medida = Column(String(10), nullable=False)  # R$/litro, R$/kg, etc
    
    # Foreign Keys
    revenda_id = Column(Integer, ForeignKey("revendas.id"), nullable=False, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False, index=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    revenda = relationship("Revenda", back_populates="coletas")
    produto = relationship("Produto", back_populates="coletas")
    
    def __repr__(self):
        return f"<ColetaPreco(id={self.id}, data='{self.data_coleta}', valor={self.valor_venda}, revenda_id={self.revenda_id})>"