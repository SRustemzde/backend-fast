# app/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional # Optional import edildi

class Settings(BaseSettings):
    # MongoDB Settings
    MONGO_INITDB_ROOT_USERNAME: Optional[str] = None
    MONGO_INITDB_ROOT_PASSWORD: Optional[str] = None
    MONGO_HOST: str = "localhost"
    MONGO_PORT: int = 27017
    MONGO_DB_NAME: str = "netflix_clone_db"

    # JWT Settings
    SECRET_KEY: str = "a_very_secret_key_that_should_be_in_env_and_long" # Varsayılan değer
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 # Varsayılan 30 dakika

    # Seed Script için Admin Kullanıcı Bilgileri (YENİ)
    ADMIN_EMAIL: Optional[str] = None
    ADMIN_PASSWORD: Optional[str] = None

    @property
    def MONGO_CONNECTION_STRING(self) -> str:
        if self.MONGO_INITDB_ROOT_USERNAME and self.MONGO_INITDB_ROOT_PASSWORD:
            # authSource=admin genellikle root kullanıcıları için gereklidir.
            # Eğer uygulamanız için özel bir kullanıcı oluşturduysanız ve o kullanıcı
            # kendi veritabanında (MONGO_DB_NAME) tanımlıysa, authSource'u o veritabanı yapabilir
            # veya hiç belirtmeyebilirsiniz (MongoDB sürücüsü genellikle doğru olanı bulur).
            return (
                f"mongodb://{self.MONGO_INITDB_ROOT_USERNAME}:{self.MONGO_INITDB_ROOT_PASSWORD}"
                f"@{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DB_NAME}?authSource=admin"
            )
        return f"mongodb://{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DB_NAME}"

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