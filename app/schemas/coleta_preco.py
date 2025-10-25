from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional


class ColetaPrecoBase(BaseModel):
    """Schema base de Coleta de Preço"""
    data_coleta: date
    valor_venda: float = Field(..., gt=0)
    valor_compra: Optional[float] = Field(None, gt=0)
    unidade_medida: str = Field(..., max_length=10)
    revenda_id: int
    produto_id: int


class ColetaPrecoCreate(ColetaPrecoBase):
    """Schema para criação de Coleta de Preço"""
    pass


class ColetaPrecoUpdate(BaseModel):
    """Schema para atualização de Coleta de Preço"""
    data_coleta: Optional[date] = None
    valor_venda: Optional[float] = Field(None, gt=0)
    valor_compra: Optional[float] = Field(None, gt=0)
    unidade_medida: Optional[str] = Field(None, max_length=10)


class ColetaPrecoResponse(ColetaPrecoBase):
    """Schema de resposta de Coleta de Preço"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ColetaPrecoDetailResponse(BaseModel):
    """Schema detalhado com informações de revenda e produto"""
    id: int
    data_coleta: date
    valor_venda: float
    valor_compra: Optional[float]
    unidade_medida: str
    revenda_id: int
    revenda_nome: str
    revenda_municipio: str
    revenda_estado: str
    produto_id: int
    produto_nome: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class ColetaPrecoListResponse(BaseModel):
    """Schema de listagem de Coletas de Preço"""
    items: list[ColetaPrecoResponse]
    total: int
    skip: int
    limit: int