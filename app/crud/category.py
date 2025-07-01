# app/crud/category.py

from typing import List, Optional
from beanie.odm.operators.update.general import Set
from app.models.category import CategoryDocument
from app.schemas.category import CategoryCreate, CategoryUpdate

async def get_category(category_id: str) -> Optional[CategoryDocument]:
    return await CategoryDocument.get(category_id)

async def get_category_by_name(name: str) -> Optional[CategoryDocument]:
    return await CategoryDocument.find_one(CategoryDocument.name == name)

async def get_categories(skip: int = 0, limit: int = 100) -> List[CategoryDocument]:
    return await CategoryDocument.find_all(skip=skip, limit=limit).to_list()

async def create_category(category_in: CategoryCreate) -> CategoryDocument:
    category = CategoryDocument(**category_in.model_dump())
    await category.insert()
    return category

async def update_category(category_id: str, category_in: CategoryUpdate) -> Optional[CategoryDocument]:
    category = await CategoryDocument.get(category_id)
    if not category:
        return None
    
    update_data = category_in.model_dump(exclude_unset=True)
    if not update_data: # Eğer güncellenecek bir şey yoksa
        return category

    await category.update(Set(update_data))
    return await CategoryDocument.get(category_id) # Güncellenmiş dökümanı getir

async def delete_category(category_id: str) -> bool:
    category = await CategoryDocument.get(category_id)
    if category:
        await category.delete()
        return True
    return False