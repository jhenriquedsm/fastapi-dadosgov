from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ProdutoBase(BaseModel):
    """Schema base de Produto"""
    nome: str = Field(..., min_length=1, max_length=50)
    descricao: Optional[str] = Field(None, max_length=200)


class ProdutoCreate(ProdutoBase):
    """Schema para criação de Produto"""
    pass


class ProdutoUpdate(BaseModel):
    """Schema para atualização de Produto"""
    nome: Optional[str] = Field(None, min_length=1, max_length=50)
    descricao: Optional[str] = Field(None, max_length=200)


class ProdutoResponse(ProdutoBase):
    """Schema de resposta de Produto"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ProdutoListResponse(BaseModel):
    """Schema de listagem de Produtos"""
    items: list[ProdutoResponse]
    total: int