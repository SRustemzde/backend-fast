# app/dependencies.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from typing import Optional

from app.utils import token as token_utils # JWT yardımcı fonksiyonlarımız
from app.schemas.user import TokenData, UserPublic # Pydantic şemalarımız
from app.crud import user as crud_user # Kullanıcı CRUD operasyonları
from app.models.user import UserDocument # User modelimiz

# OAuth2PasswordBearer, token'ı "Authorization: Bearer <token>" header'ından alır.
# tokenUrl, frontend'in token almak için gideceği endpoint'i belirtir.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Optional[UserDocument]:
    """
    Token'ı doğrular ve mevcut kullanıcıyı döndürür.
    Eğer token geçersizse veya kullanıcı bulunamazsa HTTPException fırlatır.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = token_utils.decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    email: Optional[str] = payload.get("sub")
    if email is None:
        raise credentials_exception
    
    token_data = TokenData(email=email)
    
    user = await crud_user.get_user_by_email(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: UserDocument = Depends(get_current_user)) -> UserPublic:
    """
    Mevcut kullanıcının aktif olup olmadığını kontrol eder.
    Eğer aktif değilse HTTPException fırlatır.
    UserPublic şemasında döner (hassas bilgiler olmadan).
    """
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    
    # UserDocument'tan UserPublic'e dönüşüm
    return UserPublic(
        id=str(current_user.id),
        email=current_user.email,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        is_superuser=current_user.is_superuser,
        time_created=current_user.time_created,
        time_updated=current_user.time_updated
    )

async def get_current_active_superuser(current_user: UserDocument = Depends(get_current_user)) -> UserPublic:
    """
    Mevcut kullanıcının aktif ve süper kullanıcı (admin) olup olmadığını kontrol eder.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return UserPublic.model_validate(current_user) # Pydantic v2'de from_orm yerine model_validate