from uuid import UUID, uuid4
from datetime import datetime

from app.repositories.category import ICategoryRepository
from app.models.category import CategoryResponse, CategoryCreate

class FakeCategoryRepository(ICategoryRepository):
    def __init__(self):
        self._storage: dict[UUID, CategoryResponse] = {}

    async def create(self, model: CategoryCreate) -> CategoryResponse:
        new_uuid = uuid4()
        new_category = CategoryResponse(
            id= new_uuid,
            name= model.name,
            description= model.description,
            created_at= datetime.now()
            )
        self._storage[new_uuid] = new_category
        return self._storage[new_uuid]

    async def get_by_id(self, category_id: UUID) -> CategoryResponse:
        try:
            return self._storage[category_id]
        except KeyError:
            raise ValueError(f"Category with id {category_id} not found")

    async def get_all(self) -> list[CategoryResponse]:
        return list(self._storage.values())

    async def update(self, category_id: UUID, model: CategoryCreate) -> CategoryResponse:
        if category_id in self._storage:
            original_created_at = self._storage[category_id].created_at
            self._storage[category_id] = CategoryResponse(
                id= category_id,
                name= model.name,
                description= model.description,
                created_at= original_created_at
            )
        else:
            raise ValueError(f"Category with id {category_id} not found")

        return self._storage[category_id]

    async def delete(self, category_id: UUID) -> bool:
        if category_id in self._storage:
            del self._storage[category_id]
            return True
        return False