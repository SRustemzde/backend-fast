# app/routers/category.py

from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.schemas.category import CategoryCreate, CategoryPublic, CategoryUpdate
from app.crud import category as crud_category
from app.dependencies import get_current_active_superuser # Güncellenmiş import
from app.schemas.user import UserPublic # UserPublic şemasını da import et

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

@router.post("/", response_model=CategoryPublic, status_code=status.HTTP_201_CREATED)
async def create_new_category(
    category_in: CategoryCreate,
    current_user: UserPublic = Depends(get_current_active_superuser) # Admin yetkisi
):
    db_category = await crud_category.get_category_by_name(name=category_in.name)
    if db_category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category already exists with this name")
    created_category = await crud_category.create_category(category_in=category_in)
    # Beanie dökümanından Pydantic modeline dönüşüm
    return CategoryPublic.model_validate(created_category)

@router.get("/", response_model=List[CategoryPublic])
async def read_categories(skip: int = 0, limit: int = 100):
    categories = await crud_category.get_categories(skip=skip, limit=limit)
    return [CategoryPublic.model_validate(cat) for cat in categories]

@router.get("/{category_id}", response_model=CategoryPublic)
async def read_category(category_id: str):
    category = await crud_category.get_category(category_id=category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return CategoryPublic.model_validate(category)

@router.put("/{category_id}", response_model=CategoryPublic)
async def update_existing_category(
    category_id: str,
    category_in: CategoryUpdate,
    current_user: UserPublic = Depends(get_current_active_superuser) # Admin yetkisi
):
    # İsim güncelleniyorsa, yeni ismin başka bir kategoride kullanılmadığını kontrol et
    if category_in.name:
        existing_category_with_name = await crud_category.get_category_by_name(name=category_in.name)
        if existing_category_with_name and str(existing_category_with_name.id) != category_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Another category with this name already exists")

    updated_category = await crud_category.update_category(category_id=category_id, category_in=category_in)
    if not updated_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found for update")
    return CategoryPublic.model_validate(updated_category)

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_category(
    category_id: str,
    current_user: UserPublic = Depends(get_current_active_superuser) # Admin yetkisi
):
    # İsteğe bağlı: Bu kategoriyi kullanan içerikler varsa ne yapılacağına karar ver (örn: silmeyi engelle, içeriklerden kaldır)
    deleted = await crud_category.delete_category(category_id=category_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found for deletion")
    return None