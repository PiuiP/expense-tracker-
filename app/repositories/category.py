from abc import ABC, abstractmethod
from uuid import UUID
from app.models.category import CategoryCreate, CategoryResponse

class ICategoryRepository(ABC):
    
    @abstractmethod
    async def create(self, model: CategoryCreate) -> CategoryResponse:
        pass 

    @abstractmethod
    async def get_by_id(self, id: UUID) -> CategoryResponse:
        pass

    @abstractmethod
    async def get_all(self) -> list[CategoryResponse]:
        pass
    
    @abstractmethod
    async def update(self, id: UUID, model: CategoryCreate) -> CategoryResponse:
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        pass