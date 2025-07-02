# app/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional # Optional import edildi

class Settings(BaseSettings):
    # MongoDB Settings
    MONGO_URI: str = "mongodb://localhost:27017/netflix_clone_db"

    # JWT Settings
    SECRET_KEY: str = "a_very_secret_key_that_should_be_in_env_and_long" # Varsayılan değer
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 # Varsayılan 30 dakika

    # Seed Script için Admin Kullanıcı Bilgileri (YENİ)
    ADMIN_EMAIL: Optional[str] = None
    ADMIN_PASSWORD: Optional[str] = None

    @property
    def MONGO_DB_NAME(self) -> str:
        """Extract database name from MONGO_URI"""
        try:
            # Parse database name from URI
            if '/' in self.MONGO_URI:
                db_part = self.MONGO_URI.split('/')[-1]
                # Remove query parameters if any
                if '?' in db_part:
                    db_part = db_part.split('?')[0]
                return db_part or "netflix_clone_db"
            return "netflix_clone_db"
        except:
            return "netflix_clone_db"

    # .env dosyasını okumak için model_config ayarı
    # extra='ignore' bilinmeyen alanları yoksayar
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')


@lru_cache() # Settings nesnesinin sadece bir kez oluşturulmasını sağlar
def get_settings() -> Settings:
    # .env dosyasının varlığını kontrol et ve kullanıcıyı bilgilendir
    import os
    if not os.path.exists(".env"):
        print("WARNING: .env file not found. Using default settings or environment variables.")
    return Settings()

settings = get_settings() # Ayarları global olarak erişilebilir yapalım