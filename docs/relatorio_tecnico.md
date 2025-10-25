# Relatório Técnico - Entrega 1
## API de Preços de Combustíveis

**Disciplina**: Projeto de Linguagens de Programação
**Entrega**: ENTREGA 1 – ESTRUTURA INICIAL DA API COM SQLITE 
**Aluno**: José Henrique da Silva Mata
**RGM**: 1430525187

---

## 1. Justificativa da Escolha do Dataset

### Dataset Selecionado
**Série Histórica de Preços de Combustíveis e GLP**  
**Fonte**: [dados.gov.br](https://dados.gov.br/dados/conjuntos-dados/serie-historica-de-precos-de-combustiveis-e-de-glp)

### Motivação da Escolha

O dataset de preços de combustíveis da ANP foi escolhido pelos seguintes motivos:

1. **Relevância Social**: Os preços dos combustíveis impactam diretamente o cotidiano da população brasileira e a economia do país.

2. **Volume de Dados**: Dataset robusto com milhões de registros, permitindo análises significativas e testes de performance.

3. **Estrutura Adequada**: Os dados possuem características que permitem uma modelagem relacional clara, com entidades distintas e relacionamentos bem definidos.

4. **Atualização Regular**: A ANP atualiza os dados periodicamente, garantindo relevância temporal.

5. **Diversidade de Análises**: Permite análises por região, município, tipo de combustível, período temporal e bandeira, oferecendo múltiplas perspectivas.

---

## 2. Modelagem do Banco de Dados

### 2.1 Entidades e Relacionamentos

O banco de dados foi normalizado em **4 entidades principais**:

#### **User**
- **Propósito**: Gerenciar autenticação e autorização
- **Campos principais**: `id`, `username`, `email`, `hashed_password`, `role`
- **Roles**: `admin` (acesso completo) e `leitor` (apenas leitura)

#### **Revenda**
- **Propósito**: Representar postos de combustível/revendedores
- **Campos principais**: `id`, `cnpj`, `nome`, `municipio`, `estado`, `regiao_sigla`, `bandeira`
- **Características**: CNPJ único, indexação por estado e município para consultas eficientes

#### **Produto**
- **Propósito**: Catalogar tipos de combustível
- **Campos principais**: `id`, `nome`, `descricao`
- **Exemplos**: GASOLINA, ETANOL, DIESEL S10, GLP, GNV
- **Normalização**: Evita repetição de nomes de produtos em milhões de registros

#### **ColetaPreco**
- **Propósito**: Registrar o fato (preço coletado)
- **Campos principais**: `id`, `data_coleta`, `valor_venda`, `valor_compra`, `unidade_medida`, `revenda_id`, `produto_id`
- **Relacionamentos**: 
  - N:1 com Revenda (muitas coletas pertencem a uma revenda)
  - N:1 com Produto (muitas coletas pertencem a um produto)

### 2.2 Diagrama ER

```
USER (1) ----gerencia----> (N) COLETA_PRECO
REVENDA (1) ----possui----> (N) COLETA_PRECO
PRODUTO (1) ----refere-se-> (N) COLETA_PRECO
```

Ver diagrama completo em `docs/modelagem_er.png`

### 2.3 Justificativa da Normalização

**Problema Original**: O dataset é uma única tabela "fato" (CSV gigante) com muita redundância.

**Solução Aplicada**:
- **Evita redundância**: Nome do produto não é repetido milhões de vezes
- **Facilita manutenção**: Alterar informações de uma revenda atualiza automaticamente todas as coletas
- **Melhora performance**: Índices em chaves estrangeiras aceleram consultas
- **Garante integridade**: Relacionamentos garantem que não existam coletas órfãs

---

## 3. Estrutura da API

### 3.1 Arquitetura em Camadas

A API foi desenvolvida seguindo o padrão de **arquitetura em camadas**:

```
┌─────────────────────────────────────┐
│         Routers (Endpoints)         │  ← Interface HTTP
├─────────────────────────────────────┤
│      Services (Lógica de Negócio)   │  ← Regras de negócio
├─────────────────────────────────────┤
│    Models (ORM - SQLAlchemy)        │  ← Mapeamento objeto-relacional
├─────────────────────────────────────┤
│      Database (SQLite)              │  ← Persistência
└─────────────────────────────────────┘
```

**Benefícios**:
- **Separação de responsabilidades**: Cada camada tem função específica
- **Facilita testes**: Camadas podem ser testadas isoladamente
- **Manutenibilidade**: Mudanças em uma camada não afetam as outras
- **Reutilização**: Services podem ser usados por múltiplos routers

### 3.2 Tecnologias Utilizadas

| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| Python | 3.10+ | Linguagem base |
| FastAPI | 0.115.0 | Framework web |
| SQLAlchemy | 2.0.35 | ORM |
| SQLite | 3.x | Banco de dados |
| Pydantic | 2.9.2 | Validação de dados |
| JWT | - | Autenticação |
| Bcrypt | - | Hash de senhas |

### 3.3 Endpoints Implementados

#### **Autenticação** (`/api/v1/auth`)
- `POST /register` - Registrar usuário
- `POST /login` - Obter token JWT

#### **Revendas** (`/api/v1/revendas`)
- `GET /` - Listar revendas (com filtros)
- `GET /{id}` - Buscar por ID
- `POST /` - Criar (admin)
- `PUT /{id}` - Atualizar (admin)
- `DELETE /{id}` - Deletar (admin)

#### **Produtos** (`/api/v1/produtos`)
- `GET /` - Listar produtos
- `GET /{id}` - Buscar por ID
- `POST /` - Criar (admin)
- `PUT /{id}` - Atualizar (admin)
- `DELETE /{id}` - Deletar (admin)

#### **Coletas de Preço** (`/api/v1/coletas`)
- `GET /` - Listar coletas (com filtros)
- `GET /{id}` - Buscar por ID
- `POST /` - Criar (admin)
- `PUT /{id}` - Atualizar (admin)
- `DELETE /{id}` - Deletar (admin)

### 3.4 Recursos Implementados

**Autenticação JWT**:
- Token expira em 30 minutos (configurável)
- Senha com hash bcrypt
- Middleware de autorização por role

**Filtros Avançados**:
- Coletas: estado, município, produto, data_inicio, data_fim
- Revendas: estado, município, bandeira
- Paginação: skip e limit em todos os endpoints de listagem

**Validação de Dados**:
- Pydantic schemas validam entrada/saída
- CNPJ no formato correto
- Estados com 2 caracteres
- Valores monetários positivos

**Documentação Automática**:
- Swagger UI em `/docs`
- ReDoc em `/redoc`
- Schemas OpenAPI 3.0

---

## 4. Evidências de Testes

### 4.1 Testes Manuais via Postman

A collection do Postman (`postman_collection.json`) contém:
- ✅ 2 testes de autenticação
- ✅ 3 testes de produtos
- ✅ 5 testes de revendas
- ✅ 4 testes de coletas

**Total**: 14 casos de teste

### 4.2 Fluxo de Teste Executado

1. **Setup Inicial**
   ```bash
   python scripts/init_db.py
   uvicorn app.main:app --reload
   ```

2. **Autenticação**
   - ✅ Registro de usuário leitor
   - ✅ Login com admin (token salvo em variável)

3. **CRUD de Produtos**
   - ✅ Listagem de produtos (7 produtos padrão)
   - ✅ Criação de novo produto
   - ✅ Busca por ID

4. **CRUD de Revendas**
   - ✅ Listagem com filtros (estado=SP)
   - ✅ Criação de revenda
   - ✅ Busca por ID
   - ✅ Atualização de bandeira
   - ✅ Validação de CNPJ duplicado

5. **CRUD de Coletas**
   - ✅ Listagem com múltiplos filtros
   - ✅ Criação de coleta
   - ✅ Validação de relacionamentos (revenda e produto devem existir)

### 4.3 Testes de Autorização

- ✅ Usuário leitor consegue acessar endpoints GET
- ✅ Usuário leitor **não** consegue acessar POST/PUT/DELETE (403 Forbidden)
- ✅ Admin consegue acessar todos os endpoints
- ✅ Token inválido retorna 401 Unauthorized

---

## 5. Instruções de Execução

### 5.1 Pré-requisitos
- Python 3.10 ou superior
- pip (gerenciador de pacotes)

### 5.2 Instalação

```bash
# 1. Clone o repositório
git clone <repository-url>
cd fuel-prices-api

# 2. Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 3. Instale dependências
pip install -r requirements.txt

# 4. Configure variáveis de ambiente
cp .env.example .env

# 5. Inicialize o banco de dados
python scripts/init_db.py
```

### 5.3 Executar a API

```bash
uvicorn app.main:app --reload
```

Acessar:
- API: http://localhost:8000
- Documentação: http://localhost:8000/docs

### 5.4 Carregar Dados (Opcional)

```bash
# Baixe o CSV do portal dados.gov.br
# Salve em: data/combustiveis.csv
python scripts/load_data.py
```

---

## 6. Versionamento Git

### 6.1 Branches

```
main (produção)
  └── develop (desenvolvimento)
       ├── feature/initial-setup
       ├── feature/database-models
       ├── feature/authentication
       ├── feature/crud-endpoints
       ├── feature/data-loading
       └── feature/testing
```

### 6.2 Commits Semânticos

Padrão utilizado:
- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Documentação
- `chore:` Tarefas gerais
- `test:` Testes

Exemplos:
```
feat: add User model with authentication fields
feat: implement JWT token generation
docs: add ER diagram
chore: add dependencies and requirements
```

---

## 7. Próximos Passos (Entrega 2)

Para a próxima entrega, planeja-se:

1. **Migração para PostgreSQL**: Substituir SQLite por banco mais robusto
2. **Endpoints de Análise**: Estatísticas e agregações
3. **Cache Redis**: Melhorar performance de consultas frequentes
4. **Testes Automatizados**: Pytest com cobertura > 80%
5. **CI/CD**: GitHub Actions para deploy automatizado
6. **Containerização**: Docker e Docker Compose

---

## 8. Conclusão

A Entrega 1 estabeleceu com sucesso a estrutura base da API, implementando:

✅ Modelagem relacional com 4 entidades  
✅ API RESTful completa com FastAPI  
✅ Autenticação JWT com roles  
✅ CRUD completo para todas as entidades  
✅ Filtros e paginação  
✅ Documentação automática  
✅ Versionamento com Git Flow  
✅ Testes via Postman  

A aplicação está funcional, estável e pronta para evoluir nas próximas entregas.