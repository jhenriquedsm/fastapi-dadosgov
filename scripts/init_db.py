"""
Script para inicializar o banco de dados
Cria as tabelas e usuário admin padrão
"""
import sys
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent))

from app.database.connection import Base, engine, SessionLocal
from app.models import User, UserRole, Produto
from app.utils.security import get_password_hash
from app.config import settings


def create_tables():
    """Cria todas as tabelas no banco de dados"""
    print("Criando tabelas...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tabelas criadas com sucesso!")


def create_admin_user():
    """Cria usuário admin padrão"""
    db = SessionLocal()
    try:
        # Verifica se admin já existe
        existing_admin = db.query(User).filter(User.username == settings.ADMIN_USERNAME).first()
        if existing_admin:
            print(f"✓ Usuário admin '{settings.ADMIN_USERNAME}' já existe")
            return
        
        # Cria admin
        admin = User(
            username=settings.ADMIN_USERNAME,
            email=settings.ADMIN_EMAIL,
            hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
            role=UserRole.ADMIN,
            is_active=1
        )
        db.add(admin)
        db.commit()
        print(f"✓ Usuário admin criado: {settings.ADMIN_USERNAME}")
        print(f"  Email: {settings.ADMIN_EMAIL}")
        print(f"  Senha: {settings.ADMIN_PASSWORD}")
        print("  ⚠️  ALTERE A SENHA PADRÃO EM PRODUÇÃO!")
    finally:
        db.close()


def create_default_produtos():
    """Cria produtos padrão (tipos de combustível)"""
    db = SessionLocal()
    try:
        produtos_padrao = [
            {"nome": "GASOLINA", "descricao": "Gasolina comum"},
            {"nome": "GASOLINA ADITIVADA", "descricao": "Gasolina com aditivos"},
            {"nome": "ETANOL", "descricao": "Etanol hidratado"},
            {"nome": "DIESEL", "descricao": "Diesel comum"},
            {"nome": "DIESEL S10", "descricao": "Diesel com baixo teor de enxofre"},
            {"nome": "GLP", "descricao": "Gás Liquefeito de Petróleo (botijão)"},
            {"nome": "GNV", "descricao": "Gás Natural Veicular"}
        ]
        
        produtos_criados = 0
        for produto_data in produtos_padrao:
            existing = db.query(Produto).filter(Produto.nome == produto_data["nome"]).first()
            if not existing:
                produto = Produto(**produto_data)
                db.add(produto)
                produtos_criados += 1
        
        db.commit()
        if produtos_criados > 0:
            print(f"✓ {produtos_criados} produtos criados")
        else:
            print("✓ Produtos padrão já existem")
    finally:
        db.close()


def main():
    """Executa inicialização completa"""
    print("=" * 50)
    print("Inicializando banco de dados...")
    print("=" * 50)
    
    create_tables()
    create_admin_user()
    create_default_produtos()
    
    print("=" * 50)
    print("✓ Inicialização concluída com sucesso!")
    print("=" * 50)
    print("\nPróximos passos:")
    print("1. Execute: uvicorn app.main:app --reload")
    print("2. Acesse: http://localhost:8000/docs")
    print(f"3. Faça login com: {settings.ADMIN_USERNAME} / {settings.ADMIN_PASSWORD}")


if __name__ == "__main__":
    main()