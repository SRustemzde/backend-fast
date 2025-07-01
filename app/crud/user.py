# app/crud/user.py

from typing import Optional
from beanie.odm.operators.update.general import Set # Set import edildi
from datetime import datetime # datetime import edildi

from app.models.user import UserDocument, UserPreferences, UserSecurity
from app.schemas.user import UserCreate, UserProfileUpdate, UserPreferencesUpdate, UserPasswordUpdate
from app.utils.security import get_password_hash, verify_password # verify_password eklendi

async def get_user_by_email(email: str) -> Optional[UserDocument]:
    return await UserDocument.find_one(UserDocument.email == email)

async def get_user_by_username(username: str) -> Optional[UserDocument]:
    return await UserDocument.find_one(UserDocument.username == username)

async def get_user_by_id(user_id: str) -> Optional[UserDocument]: # ID ile kullanıcı getirme
    return await UserDocument.get(user_id)

async def create_user(user_in: UserCreate) -> UserDocument:
    hashed_password = get_password_hash(user_in.password)
    
    user_data = user_in.model_dump(exclude={"password"})
    user_data["password"] = hashed_password
    
    db_user = UserDocument(**user_data)
    await db_user.insert()
    return db_user

async def update_user_profile(user: UserDocument, profile_in: UserProfileUpdate) -> UserDocument:
    update_data = {}
    
    for field, value in profile_in.model_dump(exclude_unset=True).items():
        if value is not None:
            update_data[field] = value
        
    if not update_data:
        return user

    update_data["updated_at"] = datetime.utcnow()
    
    await user.update(Set(update_data))
    return await UserDocument.get(user.id)

async def update_user_preferences(user: UserDocument, preferences_in: UserPreferencesUpdate) -> UserDocument:
    update_data = {}
    
    if preferences_in.preferences is not None:
        current_prefs = user.preferences.model_dump() if user.preferences else {}
        updated_prefs = preferences_in.preferences.model_dump(exclude_unset=True)
        current_prefs.update(updated_prefs)
        update_data["preferences"] = UserPreferences(**current_prefs)

    if not update_data:
        return user

    update_data["updated_at"] = datetime.utcnow()
    await user.update(Set(update_data))
    return await UserDocument.get(user.id)

async def update_user_password(user: UserDocument, password_in: UserPasswordUpdate) -> bool:
    if not verify_password(password_in.current_password, user.password):
        return False
    
    new_hashed_password = get_password_hash(password_in.new_password)
    await user.update(Set({
        "password": new_hashed_password,
        "updated_at": datetime.utcnow()
    }))
    return True