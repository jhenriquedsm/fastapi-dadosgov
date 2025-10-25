from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import Produto
from app.schemas import ProdutoCreate, ProdutoUpdate


class ProdutoService:
    """Serviço de gestão de produtos"""
    
    @staticmethod
    def get_all(db: Session) -> list[Produto]:
        """Lista todos os produtos"""
        return db.query(Produto).all()
    
    @staticmethod
    def get_by_id(db: Session, produto_id: int) -> Produto:
        """Busca produto por ID"""
        produto = db.query(Produto).filter(Produto.id == produto_id).first()
        if not produto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produto não encontrado"
            )
        return produto
    
    @staticmethod
    def get_by_name(db: Session, nome: str) -> Produto:
        """Busca produto por nome"""
        produto = db.query(Produto).filter(Produto.nome == nome.upper()).first()
        if not produto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Produto '{nome}' não encontrado"
            )
        return produto
    
    @staticmethod
    def create(db: Session, produto_data: ProdutoCreate) -> Produto:
        """Cria um novo produto"""
        # Verifica se nome já existe
        existing = db.query(Produto).filter(
            Produto.nome == produto_data.nome.upper()
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Produto já cadastrado"
            )
        
        db_produto = Produto(
            nome=produto_data.nome.upper(),
            descricao=produto_data.descricao
        )
        db.add(db_produto)
        db.commit()
        db.refresh(db_produto)
        
        return db_produto
    
    @staticmethod
    def update(db: Session, produto_id: int, produto_data: ProdutoUpdate) -> Produto:
        """Atualiza um produto"""
        produto = ProdutoService.get_by_id(db, produto_id)
        
        update_data = produto_data.model_dump(exclude_unset=True)
        if 'nome' in update_data:
            update_data['nome'] = update_data['nome'].upper()
        
        for field, value in update_data.items():
            setattr(produto, field, value)
        
        db.commit()
        db.refresh(produto)
        
        return produto
    
    @staticmethod
    def delete(db: Session, produto_id: int) -> None:
        """Deleta um produto"""
        produto = ProdutoService.get_by_id(db, produto_id)
        db.delete(produto)
        db.commit()