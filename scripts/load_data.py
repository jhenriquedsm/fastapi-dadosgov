"""
Script para carregar dados do CSV do portal dados.gov.br
"""
import sys
from pathlib import Path
import pandas as pd
from datetime import datetime

# Adicionar diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent))

from app.database.connection import SessionLocal
from app.models import Revenda, Produto, ColetaPreco


def normalize_cnpj(cnpj):
    """Normaliza CNPJ para formato padrão"""
    if pd.isna(cnpj):
        return None
    cnpj_str = str(cnpj).strip()
    # Remove caracteres não numéricos
    cnpj_nums = ''.join(filter(str.isdigit, cnpj_str))
    if len(cnpj_nums) != 14:
        return None
    # Formata: XX.XXX.XXX/XXXX-XX
    return f"{cnpj_nums[:2]}.{cnpj_nums[2:5]}.{cnpj_nums[5:8]}/{cnpj_nums[8:12]}-{cnpj_nums[12:]}"


def load_csv_data(csv_path: str, limit: int = None):
    """
    Carrega dados do CSV para o banco
    
    Args:
        csv_path: Caminho para o arquivo CSV
        limit: Limitar número de registros (para testes)
    """
    db = SessionLocal()
    
    try:
        print(f"Carregando CSV: {csv_path}")
        
        # Lê CSV (ajuste os nomes das colunas conforme o dataset real)
        df = pd.read_csv(csv_path, sep=';', encoding='utf-8', nrows=limit)
        print(f"✓ {len(df)} registros encontrados no CSV")
        
        # Mapear colunas do CSV (ajuste conforme estrutura real)
        # Exemplo de colunas esperadas:
        # Data da Coleta, Produto, CNPJ da Revenda, Nome da Revenda,
        # Município, Estado, Região, Bandeira, Valor de Venda, Unidade de Medida
        
        produtos_cache = {}
        revendas_cache = {}
        
        coletas_inseridas = 0
        erros = 0
        
        for idx, row in df.iterrows():
            try:
                # 1. Processar Produto
                produto_nome = str(row.get('Produto', '')).strip().upper()
                if produto_nome not in produtos_cache:
                    produto = db.query(Produto).filter(Produto.nome == produto_nome).first()
                    if not produto:
                        produto = Produto(nome=produto_nome)
                        db.add(produto)
                        db.flush()
                    produtos_cache[produto_nome] = produto.id
                
                # 2. Processar Revenda
                cnpj = normalize_cnpj(row.get('CNPJ da Revenda'))
                if not cnpj:
                    continue
                
                if cnpj not in revendas_cache:
                    revenda = db.query(Revenda).filter(Revenda.cnpj == cnpj).first()
                    if not revenda:
                        revenda = Revenda(
                            cnpj=cnpj,
                            nome=str(row.get('Nome da Revenda', 'N/A'))[:200],
                            municipio=str(row.get('Município', 'N/A'))[:100],
                            estado=str(row.get('Estado', 'N/A'))[:2].upper(),
                            regiao_sigla=str(row.get('Região Sigla', 'N/A'))[:2].upper(),
                            bandeira=str(row.get('Bandeira', None))[:100] if pd.notna(row.get('Bandeira')) else None
                        )
                        db.add(revenda)
                        db.flush()
                    revendas_cache[cnpj] = revenda.id
                
                # 3. Processar Coleta
                data_coleta_str = row.get('Data da Coleta')
                if pd.notna(data_coleta_str):
                    # Ajuste o formato da data conforme o CSV
                    data_coleta = pd.to_datetime(data_coleta_str).date()
                else:
                    continue
                
                valor_venda = float(row.get('Valor de Venda', 0))
                valor_compra = float(row.get('Valor de Compra', 0)) if pd.notna(row.get('Valor de Compra')) else None
                
                coleta = ColetaPreco(
                    data_coleta=data_coleta,
                    valor_venda=valor_venda,
                    valor_compra=valor_compra,
                    unidade_medida=str(row.get('Unidade de Medida', 'R$/litro'))[:10],
                    revenda_id=revendas_cache[cnpj],
                    produto_id=produtos_cache[produto_nome]
                )
                db.add(coleta)
                coletas_inseridas += 1
                
                # Commit a cada 1000 registros
                if coletas_inseridas % 1000 == 0:
                    db.commit()
                    print(f"  {coletas_inseridas} coletas inseridas...")
            
            except Exception as e:
                erros += 1
                if erros < 10:  # Mostra apenas os primeiros 10 erros
                    print(f"  ⚠️ Erro na linha {idx}: {str(e)}")
                continue
        
        # Commit final
        db.commit()
        
        print("=" * 50)
        print(f"✓ Importação concluída!")
        print(f"  Coletas inseridas: {coletas_inseridas}")
        print(f"  Revendas únicas: {len(revendas_cache)}")
        print(f"  Produtos únicos: {len(produtos_cache)}")
        if erros > 0:
            print(f"  ⚠️ Erros: {erros}")
        print("=" * 50)
    
    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao carregar dados: {str(e)}")
        raise
    
    finally:
        db.close()


def main():
    """Executa carga de dados"""
    csv_path = "data/combustiveis.csv"  # Ajuste o caminho
    
    if not Path(csv_path).exists():
        print(f"❌ Arquivo não encontrado: {csv_path}")
        print("\nBaixe o dataset de: https://dados.gov.br/dados/conjuntos-dados/serie-historica-de-precos-de-combustiveis-e-de-glp")
        print("E salve em: data/combustiveis.csv")
        sys.exit(1)
    
    print("=" * 50)
    print("Carregando dados do CSV...")
    print("=" * 50)
    
    # Para testes, limite a 10000 registros
    # Para produção, remova o limit
    load_csv_data(csv_path, limit=10000)


if __name__ == "__main__":
    main()