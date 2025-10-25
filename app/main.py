from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import auth, revendas, produtos, coletas

# Criar aplicação FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(revendas.router, prefix=settings.API_V1_PREFIX)
app.include_router(produtos.router, prefix=settings.API_V1_PREFIX)
app.include_router(coletas.router, prefix=settings.API_V1_PREFIX)


@app.get("/")
def root():
    """Endpoint raiz da API"""
    return {
        "message": "API de Preços de Combustíveis",
        "version": settings.VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    """Verifica status da API"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)