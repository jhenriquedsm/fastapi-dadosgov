from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class RevendaBase(BaseModel):
    """Schema base de Revenda"""
    cnpj: str = Field(..., pattern=r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$')
    nome: str = Field(..., min_length=1, max_length=200)
    municipio: str = Field(..., min_length=1, max_length=100)
    estado: str = Field(..., pattern=r'^[A-Z]{2}$')
    regiao_sigla: str = Field(..., pattern=r'^[A-Z]{1,2}$')
    bandeira: Optional[str] = Field(None, max_length=100)


class RevendaCreate(RevendaBase):
    """Schema para criação de Revenda"""
    pass


class RevendaUpdate(BaseModel):
    """Schema para atualização de Revenda"""
    nome: Optional[str] = Field(None, min_length=1, max_length=200)
    municipio: Optional[str] = Field(None, min_length=1, max_length=100)
    estado: Optional[str] = Field(None, pattern=r'^[A-Z]{2}$')
    regiao_sigla: Optional[str] = Field(None, pattern=r'^[A-Z]{1,2}$')
    bandeira: Optional[str] = Field(None, max_length=100)


class RevendaResponse(RevendaBase):
    """Schema de resposta de Revenda"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class RevendaListResponse(BaseModel):
    """Schema de listagem de Revendas"""
    items: list[RevendaResponse]
    total: int
    skip: int
    limit: int