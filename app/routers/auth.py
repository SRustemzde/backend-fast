# app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm # Login formu için
from datetime import timedelta

from app.schemas.user import UserCreate, UserPublic, Token
from app.crud import user as crud_user # CRUD operasyonları
from app.utils import security, token # Yardımcı fonksiyonlar
from app.models.user import UserDocument # User modelimiz

router = APIRouter(
    prefix="/auth", # Bu router'daki tüm endpoint'ler /auth ile başlayacak
    tags=["Authentication"] # API dokümantasyonunda gruplama için
)

@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserCreate):
    """
    Yeni bir kullanıcı oluşturur.
    """
    # Email ve username kontrolü
    db_user = await crud_user.get_user_by_email(email=user_in.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu email adresi zaten kayıtlı.",
        )
    
    db_user = await crud_user.get_user_by_username(username=user_in.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu kullanıcı adı zaten kayıtlı.",
        )
        
    created_user = await crud_user.create_user(user_in=user_in)
    
    return UserPublic(
        id=str(created_user.id),
        username=created_user.username,
        email=created_user.email,
        first_name=created_user.first_name,
        last_name=created_user.last_name,
        avatar=created_user.avatar,
        subscription=created_user.subscription,
        preferences=created_user.preferences,
        is_verified=created_user.is_verified,
        is_active=created_user.is_active,
        security=created_user.security,
        devices=created_user.devices,
        created_at=created_user.created_at,
        updated_at=created_user.updated_at,
        version=created_user.version,
        last_login=created_user.last_login,
        country=created_user.country,
        phone=created_user.phone,
        birthdate=created_user.birthdate
    )

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Kullanıcı girişi yapar ve JWT access token döndürür.
    form_data.username email veya username olabilir.
    """
    # Email veya username ile giriş denemesi
    user = await crud_user.get_user_by_email(email=form_data.username)
    if not user:
        user = await crud_user.get_user_by_username(username=form_data.username)
    
    if not user or not security.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Kullanıcı adı/email veya şifre hatalı.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Last login güncelle
    from datetime import datetime
    from beanie.odm.operators.update.general import Set
    await user.update(Set({"last_login": datetime.utcnow()}))
    
    access_token_expires = timedelta(minutes=token.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}