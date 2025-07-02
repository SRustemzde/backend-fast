# app/main.py

from fastapi import FastAPI, APIRouter # APIRouter import edildi
from fastapi.middleware.cors import CORSMiddleware # CORS için import edildi
from contextlib import asynccontextmanager

from app.core.db import init_db
from app.models import get_document_models

# Router'ları import et
from app.routers import auth
from app.routers import category
from app.routers import content
from app.routers import users_interactions
from app.routers import users_profile

# Uygulama başlangıcında ve bitişinde çalışacak olay yöneticisi
@asynccontextmanager
async def lifespan(app_instance: FastAPI): # FastAPI instance'ını app_instance olarak adlandıralım
    # Uygulama başlarken yapılacaklar
    print("Application startup...")
    document_models = get_document_models() # Modelleri al
    await init_db(document_models=document_models) # Veritabanını ve Beanie'yi başlat
    yield
    # Uygulama kapanırken yapılacaklar
    print("Application shutdown...")

# FastAPI uygulamasını oluştur
app = FastAPI(
    title="Netflix Clone API (MongoDB)",
    description="API for the Netflix Clone application, built with FastAPI and MongoDB.",
    version="0.1.0",
    lifespan=lifespan # lifespan olay yöneticisini uygulamaya bağla
)

# CORS Middleware Ayarları
# Frontend'inizin çalıştığı adres(ler). Geliştirme için localhost:3000 yaygındır.
# Üretimde kendi domain adınızı eklemelisiniz.
origins = [
    "http://localhost:3000",  # React uygulamasının varsayılan portu
    "http://localhost:3001",  # Farklı bir portta çalışıyorsa
    "https://your-frontend-domain.com",  # Frontend deploy edildiğinde buraya ekle
    "*",  # Geliştirme aşamasında tüm origin'lere izin ver
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # İzin verilen kaynaklar (frontend domainleri)
    allow_credentials=True, # Cookie tabanlı kimlik doğrulama için (eğer kullanılacaksa)
    allow_methods=["*"],    # İzin verilen HTTP metodları (GET, POST, PUT, DELETE vb.)
    allow_headers=["*"],    # İzin verilen HTTP başlıkları
)


# API endpoint'leri için genel bir prefix (/api) oluşturmak iyi bir pratiktir.
# Bu, API versiyonlaması veya base path yönetimi için de faydalı olabilir.
api_router_v1 = APIRouter(prefix="/api/v1") # v1 gibi bir versiyonlama da eklenebilir

# Router'ları api_router_v1'e dahil et
api_router_v1.include_router(auth.router)
api_router_v1.include_router(category.router)
api_router_v1.include_router(content.router)
api_router_v1.include_router(users_interactions.router)
api_router_v1.include_router(users_profile.router)

# Ana router'ı (api_router_v1) uygulamaya dahil et
app.include_router(api_router_v1)


# Temel endpoint'ler (genellikle API prefix'i dışında kalabilir veya API içinde de olabilir)
@app.get("/") # Bu, API prefix'i dışında kalacak (http://localhost:8000/)
async def read_root():
    """
    Root endpoint that returns a welcome message.
    """
    return {"message": "Welcome to the Netflix Clone API (MongoDB)! Go to /docs for API documentation."}

@app.get("/health") # Bu da API prefix'i dışında kalacak (http://localhost:8000/health)
async def health_check():
    """
    Health check endpoint to verify if the API is running.
    """
    return {"status": "healthy", "message": "API is up and running!"}