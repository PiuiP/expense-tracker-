import pytest
from uuid import UUID
from app.services.category import CategoryService
from app.repositories.fake_category import FakeCategoryRepository
from app.models.category import CategoryCreate

async def test_create_category():
    repo = FakeCategoryRepository()
    service = CategoryService(repo)
    data = CategoryCreate(name="Еда", description="Продукты")

    result = await service.create_category(data)
    
    assert result.name == "Еда"
    assert result.description == "Продукты"
    assert isinstance(result.id, UUID) 

async def test_get_category_by_id():
    repo = FakeCategoryRepository()
    service = CategoryService(repo)

    data1 = CategoryCreate(name="Еда", description="Продукты")
    data2 = CategoryCreate(name="Здоровье", description="Лекарства")

    created_cat1 = await service.create_category(data1) #Хранит ссылку на объект CategoryResponse в словаре self._storage
    created_cat2 = await service.create_category(data2) #Аналогично. У нас метод create_category возвращает фул объект Response

    fetched_cat1 = await service.get_category_by_id(created_cat1.id)
    assert fetched_cat1.id == created_cat1.id
    assert fetched_cat1.name == "Еда"
    assert fetched_cat1.description == "Продукты"

    fetched_cat2 = await service.get_category_by_id(created_cat2.id)
    assert fetched_cat2.id == created_cat2.id
    assert fetched_cat2.name == "Здоровье"
    assert fetched_cat2.description == "Лекарства"

async def test_get_all_categories():
    repo = FakeCategoryRepository()
    service = CategoryService(repo)

    data1 = CategoryCreate(name="Еда", description="Продукты")
    data2 = CategoryCreate(name="Здоровье", description="Лекарства")

    created_cat1 = await service.create_category(data1)
    created_cat2 = await service.create_category(data2)

    fetched_cat_list = await service.get_all_categories()
    assert len(fetched_cat_list) == 2
    assert fetched_cat_list[0] == created_cat1
    assert fetched_cat_list[1] == created_cat2


