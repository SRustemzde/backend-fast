# app/routers/content.py

from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List, Optional
from app.schemas.content import ContentCreate, ContentPublic, ContentUpdate, ContentPublicShort
from app.crud import content as crud_content
from app.crud import category as crud_category
from app.dependencies import get_current_active_superuser # Dependency import
from app.schemas.user import UserPublic # UserPublic import
from app.models.category import CategoryDocument # Kategori modeli import edildi

router = APIRouter(
    prefix="/content",
    tags=["Content"]
)

@router.post("/", response_model=ContentPublic, status_code=status.HTTP_201_CREATED)
async def create_new_content(
    content_in: ContentCreate,
    current_user: UserPublic = Depends(get_current_active_superuser)
):
    if content_in.category_ids:
        for cat_id_str in content_in.category_ids:
            category_doc = await crud_category.get_category(cat_id_str)
            if not category_doc:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Category with id {cat_id_str} not found")
    
    created_content = await crud_content.create_content(content_in=content_in)
    return ContentPublic.model_validate(created_content)


@router.get("/", response_model=List[ContentPublicShort])
async def read_all_content(
    skip: int = 0,
    limit: int = 20,
    category: Optional[str] = Query(None, description="Filter by category name (case-insensitive)"),
    type: Optional[str] = Query(None, description="Filter by content type (MOVIE, TV_SHOW) (case-insensitive)"),
    featured: Optional[bool] = Query(None, description="Filter by featured content"),
    trending: Optional[bool] = Query(None, description="Filter by trending content"),
    sort_by: Optional[str] = Query(None, description="Sort by field (e.g., rating, -release_date, $textScore for search relevance)"),
    q: Optional[str] = Query(None, min_length=2, description="Search query for title or description (case-insensitive, min 2 chars)")
):
    # CRUD fonksiyonu artık arama ve kategori filtrelemesini (Python tarafında) yapıyor
    contents_from_db = await crud_content.get_contents(
        skip=skip, limit=limit, category_name=category, content_type=type, sort_by=sort_by,
        search_query=q, featured=featured, trending=trending
    )
            
    # Convert ObjectId to string for each content item
    result = []
    for c in contents_from_db:
        content_dict = c.model_dump()
        content_dict["id"] = str(c.id)  # Convert ObjectId to string
        result.append(ContentPublicShort.model_validate(content_dict))
    return result

@router.get("/{content_id}", response_model=ContentPublicShort)
async def read_single_content(content_id: str):
    content = await crud_content.get_content(content_id=content_id)
    if not content:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found")
    content_dict = content.model_dump()
    content_dict["id"] = str(content.id)  # Convert ObjectId to string
    return ContentPublicShort.model_validate(content_dict)


@router.get("/source/{source_name}/{source_id}", response_model=ContentPublic)
async def read_content_by_source(source_name: str, source_id: int):
    content = await crud_content.get_content_by_source_details(source_name=source_name, source_id=source_id)
    if not content:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found by source details")
    content_dict = content.model_dump()
    content_dict["id"] = str(content.id)  # Convert ObjectId to string
    return ContentPublic.model_validate(content_dict)


@router.put("/{content_id}", response_model=ContentPublic)
async def update_existing_content(
    content_id: str,
    content_in: ContentUpdate,
    current_user: UserPublic = Depends(get_current_active_superuser)
):
    if content_in.category_ids:
        for cat_id_str in content_in.category_ids:
            if not await crud_category.get_category(cat_id_str):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Category with id {cat_id_str} not found for update")

    updated_content = await crud_content.update_content(content_id=content_id, content_in=content_in)
    if not updated_content:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found for update")
    return ContentPublic.model_validate(updated_content)


@router.delete("/{content_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_content(
    content_id: str,
    current_user: UserPublic = Depends(get_current_active_superuser)
):
    deleted = await crud_content.delete_content(content_id=content_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found for deletion")
    return None