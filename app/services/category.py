from uuid import UUID

from app.models.category import CategoryCreate, CategoryResponse
from app.repositories.category import ICategoryRepository

class CategoryService():
    def __init__(self, repository: ICategoryRepository):
        self.repository = repository

    async def create_category(self, data: CategoryCreate) -> CategoryResponse:
        return await self.repository.create(data)

    async def get_category_by_id(self, category_id: UUID) -> CategoryResponse:
        return await self.repository.get_by_id(category_id)

    async def get_all_categories(self) -> list[CategoryResponse]:
        return await self.repository.get_all()

    async def update_category(self, category_id: UUID, new_data: dict) -> CategoryResponse:
            old_category = await self.repository.get_by_id(category_id)
            if old_category is None:
                raise ValueError(f"Category with id {category_id} not found")
        
            old_dict = old_category.model_dump()
    
            old_dict.update(new_data)
            old_dict.pop('id', None) #лишнее
            old_dict.pop('created_at', None) #лишнее
    
            new_category = CategoryCreate(**old_dict)
    
            return await self.repository.update(category_id, new_category)
    
    async def delete_category(self, category_id: UUID) -> bool:
        return await self.repository.delete(category_id)
