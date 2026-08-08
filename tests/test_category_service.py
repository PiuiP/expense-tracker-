import pytest
from uuid import UUID
from app.services.category import CategoryService
from app.repositories.fake_category import FakeCategoryRepository
from app.models.category import CategoryCreate

@pytest.mark.asyncio
async def test_create_category():
    repo = FakeCategoryRepository()
    service = CategoryService(repo)
    data = CategoryCreate(name="Еда", description="Продукты")

    result = await service.create_category(data)
    
    assert result.name == "Еда"
    assert result.description == "Продукты"
    assert isinstance(result.id, UUID) 

@pytest.mark.asyncio
async def test_get_category_by_id():
    repo = FakeCategoryRepository()
    service = CategoryService(repo)
    data = CategoryCreate(name="Еда", description="Продукты")
    data1 = CategoryCreate(name="Здоровье", description="Лекарства")

    result = []
    result.append(await service.create_category(data))
    result.append(await service.create_category(data1))

    assert result[0] == "Еда"
    assert result[1] == "Здоровье"
    assert isinstance(result.id, UUID)
    assert result[1].description == "Лекарства" 

