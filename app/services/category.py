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

