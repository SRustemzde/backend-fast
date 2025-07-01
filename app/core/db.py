# app/core/db.py

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from .config import settings
from typing import List, Type
from pydantic import BaseModel

# Uygulamanızdaki tüm Beanie döküman modellerini (tabloları) buraya import edin
# Örnek: from app.models.user import User
# from app.models.content import Content

async def init_db(document_models: List[Type[BaseModel]]):
    """
    Initializes the Beanie ODM with the MongoDB client and document models.
    This should be called on application startup.
    """
    client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)
    
    # Veritabanı bağlantısını test et (opsiyonel ama iyi bir pratik)
    try:
        await client.admin.command('ping')
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"Could not connect to MongoDB: {e}")
        # Uygulamanın devam etmesini engelleyebilirsiniz veya hata loglayabilirsiniz
        raise

    # Döküman modellerini Beanie'ye tanıt
    await init_beanie(
        database=client[settings.MONGO_DB_NAME], # client.get_database() de kullanılabilir
        document_models=document_models
    )
    print(f"Beanie initialized with database: {settings.MONGO_DB_NAME} and models: {[model.__name__ for model in document_models]}")

# Veritabanı session'ı için bir dependency (Beanie'de doğrudan session yönetimi farklıdır,
# bu fonksiyon şimdilik gerekli değil, ama CRUD operasyonları için benzer yapılar kurulabilir.)
# Beanie doğrudan async metodlar sağlar.
# async def get_db_session():
#     pass