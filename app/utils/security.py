# app/utils/security.py

from passlib.context import CryptContext

# Şifre hashleme context'i oluşturuyoruz, bcrypt algoritmasını kullanacağız
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verilen düz metin şifreyi, hashlenmiş şifreyle karşılaştırır."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Verilen şifreyi hashler."""
    return pwd_context.hash(password)