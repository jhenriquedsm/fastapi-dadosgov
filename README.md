# API de Preços de Combustíveis

API RESTful para consulta e análise de preços históricos de combustíveis no Brasil, utilizando dados públicos do portal dados.gov.br.

## 📊 Dataset

**Fonte**: [Série Histórica de Preços de Combustíveis e GLP](https://dados.gov.br/dados/conjuntos-dados/serie-historica-de-precos-de-combustiveis-e-de-glp)

O dataset contém informações sobre preços de combustíveis (Gasolina, Etanol, Diesel, GLP) coletados pela ANP (Agência Nacional do Petróleo, Gás Natural e Biocombustíveis) em postos de combustível em todo o Brasil.

## 🏗️ Arquitetura

### Tecnologias

- **FastAPI**: Framework web moderno e rápido
- **SQLAlchemy**: ORM para manipulação do banco de dados
- **SQLite**: Banco de dados relacional
- **JWT**: Autenticação e autorização
- **Pydantic**: Validação de dados

### Modelagem de Dados

A API foi modelada com 4 entidades principais:

1. **User**: Usuários do sistema com autenticação
2. **Revenda**: Postos de combustível/revendedores
3. **Produto**: Tipos de combustíveis
4. **ColetaPreco**: Registro de preços coletados

**Relacionamentos**:
- Revenda (1) → (N) ColetaPreco
- Produto (1) → (N) ColetaPreco

## 🚀 Instalação e Execução

### Pré-requisitos

- Python 3.10+
- pip

### Passo a Passo

1. **Clone o repositório**

```bash
git clone <repository-url>
cd fastapi-dadosgov
```

2. **Crie e ative um ambiente virtual**

```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

3. **Instale as dependências**

```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**

```bash
cp .env.example .env
```

5. **Inicialize o banco de dados**

```bash
python scripts/init_db.py
```

6. **Carregue os dados (opcional)**

```bash
# Baixe o CSV do portal dados.gov.br e coloque em data/
python scripts/load_data.py
```

7. **Execute a aplicação**

```bash
uvicorn app.main:app --reload
```

A API estará disponível em: `http://localhost:8000`

## 📚 Documentação

### Swagger UI (Interativa)

Acesse: `http://localhost:8000/docs`

### ReDoc

Acesse: `http://localhost:8000/redoc`

## 🔐 Autenticação

A API utiliza JWT (JSON Web Tokens) para autenticação.

### Obter Token

```bash
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

### Usar Token

Inclua o token no header `Authorization`:

```bash
Authorization: Bearer <seu-token>
```

## 📋 Endpoints Principais

### Autenticação

- `POST /api/v1/auth/register` - Registrar novo usuário
- `POST /api/v1/auth/login` - Fazer login

### Revendas

- `GET /api/v1/revendas` - Listar revendas
- `GET /api/v1/revendas/{id}` - Detalhes de uma revenda
- `POST /api/v1/revendas` - Criar revenda (admin)
- `PUT /api/v1/revendas/{id}` - Atualizar revenda (admin)
- `DELETE /api/v1/revendas/{id}` - Deletar revenda (admin)

### Produtos

- `GET /api/v1/produtos` - Listar produtos
- `GET /api/v1/produtos/{id}` - Detalhes de um produto
- `POST /api/v1/produtos` - Criar produto (admin)

### Coletas de Preço

- `GET /api/v1/coletas` - Listar coletas (com filtros)
- `GET /api/v1/coletas/{id}` - Detalhes de uma coleta
- `POST /api/v1/coletas` - Registrar coleta (admin)

### Parâmetros de Query

```bash
# Filtrar por estado
GET /api/v1/coletas?estado=SP

# Filtrar por produto
GET /api/v1/coletas?produto=GASOLINA

# Filtrar por período
GET /api/v1/coletas?data_inicio=2024-01-01&data_fim=2024-12-31

# Paginação
GET /api/v1/coletas?skip=0&limit=50
```

## 🧪 Testes

### Testes Unitários

```bash
pytest
```

### Testes com Postman

Importe a collection `postman_collection.json` no Postman e execute os testes.

## 📁 Estrutura do Projeto

```
fuel-prices-api/
├── app/
│   ├── models/          # Modelos SQLAlchemy
│   ├── schemas/         # Schemas Pydantic
│   ├── routers/         # Rotas da API
│   ├── services/        # Lógica de negócio
│   ├── database/        # Configuração DB
│   └── utils/           # Utilitários
├── scripts/             # Scripts auxiliares
├── tests/               # Testes
├── data/                # Banco de dados
└── docs/                # Documentação
```

## 👥 Perfis de Usuário

- **admin**: Acesso total (CRUD completo)
- **leitor**: Apenas leitura (GET endpoints)

## 🔄 Git Flow

- `main`: Versão de produção
- `develop`: Versão de desenvolvimento
- `feature/*`: Branches de funcionalidades
- `hotfix/*`: Correções urgentes

## 📝 Licença

Este projeto foi desenvolvido para fins educacionais.

## 📞 Contato

Para dúvidas ou sugestões, abra uma issue no repositório.