# app/routers/users_profile.py

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import Optional
from datetime import datetime # datetime import edildi

from app.dependencies import get_current_user # get_current_user yeterli, UserDocument döndürüyor
from app.schemas.user import UserPublic, UserProfileUpdate, UserPreferencesUpdate, UserPasswordUpdate
from app.crud import user as crud_user
from app.models.user import UserDocument # UserDocument'ı import et
# Profil resmi yükleme için Cloudinary entegrasyonu (daha sonra eklenecek)
# from app.utils import cloudinary_service 

router = APIRouter(
    prefix="/users/me", # Mevcut kullanıcıya özel
    tags=["User Profile & Settings"]
)

@router.get("/profile", response_model=UserPublic)
async def read_my_profile(
    current_user_doc: UserDocument = Depends(get_current_user)
):
    """
    Mevcut kullanıcının tüm profil bilgilerini döndürür.
    """
    # UserDocument'tan UserPublic'e dönüşüm
    user_data = current_user_doc.model_dump()
    user_data["id"] = str(current_user_doc.id)
    return UserPublic.model_validate(user_data)

@router.put("/profile", response_model=UserPublic)
async def update_my_profile(
    profile_in: UserProfileUpdate,
    current_user_doc: UserDocument = Depends(get_current_user)
):
    """
    Mevcut kullanıcının profil bilgilerini (isim, profil resmi URL'si, telefon vb.) günceller.
    """
    updated_user = await crud_user.update_user_profile(user=current_user_doc, profile_in=profile_in)
    return UserPublic.model_validate(updated_user) # Pydantic v2'de .from_orm yerine

@router.put("/preferences", response_model=UserPublic)
async def update_my_preferences(
    preferences_in: UserPreferencesUpdate,
    current_user_doc: UserDocument = Depends(get_current_user)
):
    """
    Mevcut kullanıcının bildirim ve oynatma tercihlerini günceller.
    """
    updated_user = await crud_user.update_user_preferences(user=current_user_doc, preferences_in=preferences_in)
    return UserPublic.model_validate(updated_user)

@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_my_password(
    password_in: UserPasswordUpdate,
    current_user_doc: UserDocument = Depends(get_current_user)
):
    """
    Mevcut kullanıcının şifresini günceller.
    """
    success = await crud_user.update_user_password(user=current_user_doc, password_in=password_in)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password.",
        )
    return None # HTTP 204 No Content

# Profil resmi yükleme endpoint'i (basit örnek, dosya saklama/Cloudinary entegrasyonu eksik)
# @router.post("/profile/avatar", response_model=UserPublic)
# async def upload_my_profile_avatar(
#     file: UploadFile = File(...),
#     current_user_doc: UserDocument = Depends(get_current_user)
# ):
#     # Burada dosyayı kaydetme veya Cloudinary'e yükleme mantığı olacak
#     # Örnek:
#     # file_url = await cloudinary_service.upload_image(file, folder="avatars")
#     # if not file_url:
#     #     raise HTTPException(status_code=500, detail="Could not upload avatar")
#     
#     # profile_update_data = UserProfileUpdate(profile=UserProfileSchema(profile_picture_url=file_url))
#     # updated_user = await crud_user.update_user_profile(user=current_user_doc, profile_in=profile_update_data)
#     # return UserPublic.model_validate(updated_user)
#     raise HTTPException(status_code=501, detail="Avatar upload not yet implemented")