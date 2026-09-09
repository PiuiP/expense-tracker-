import pytest
from aiohttp.test_utils import TestClient, TestServer
from uuid import uuid4

from tests.conftest import app


@pytest.fixture
def category_payload():
    return {
        "name": "Groceries",
        "description": "Food and drinks"
    }


@pytest.fixture
def category_payload_2():
    return {
        "name": "Transport",
        "description": "Bus and taxi"
    }


@pytest.fixture
def invalid_payload_no_name():
    return {
        "description": "Test without name"
    }


@pytest.fixture
def invalid_payload_wrong_type():
    return {
        "name": 123,
        "description": "Test with wrong type"
    }


@pytest.mark.asyncio
async def test_create_category_success(app, category_payload):
    async with TestClient(TestServer(app)) as client:
        async with client.post('/categories', json=category_payload) as resp:
            assert resp.status == 201
            response_data = await resp.json()
            assert response_data["name"] == "Groceries"
            assert response_data["description"] == "Food and drinks"
            assert "id" in response_data


@pytest.mark.asyncio
async def test_create_category_invalid_missing_field(app, invalid_payload_no_name):
    async with TestClient(TestServer(app)) as client:
        async with client.post('/categories', json=invalid_payload_no_name) as resp:
            assert resp.status == 400
            response_data = await resp.json()
            assert "error" in response_data


@pytest.mark.asyncio
async def test_create_category_invalid_wrong_type(app, invalid_payload_wrong_type):
    async with TestClient(TestServer(app)) as client:
        async with client.post('/categories', json=invalid_payload_wrong_type) as resp:
            assert resp.status == 400
            response_data = await resp.json()
            assert "error" in response_data


@pytest.mark.asyncio
async def test_get_category_by_id_success(app, category_payload):
    async with TestClient(TestServer(app)) as client:
        async with client.post('/categories', json=category_payload) as create_resp:
            assert create_resp.status == 201
            created_data = await create_resp.json()
            category_id = created_data["id"]

        async with client.get(f'/categories/{category_id}') as get_resp:
            assert get_resp.status == 200
            response_data = await get_resp.json()
            assert response_data["id"] == category_id
            assert response_data["name"] == "Groceries"


@pytest.mark.asyncio
async def test_get_category_by_id_invalid_uuid(app):
    async with TestClient(TestServer(app)) as client:
        async with client.get('/categories/1') as get_resp:
            assert get_resp.status == 400
            response_data = await get_resp.json()
            assert response_data['error'] == 'Invalid UUID format'


@pytest.mark.asyncio
async def test_get_category_by_id_not_found(app):
    async with TestClient(TestServer(app)) as client:
        fake_id = str(uuid4())
        async with client.get(f'/categories/{fake_id}') as get_resp:
            assert get_resp.status == 404


@pytest.mark.asyncio
async def test_get_all_categories_success(app, category_payload, category_payload_2):
    async with TestClient(TestServer(app)) as client:
        async with client.post('/categories', json=category_payload) as resp1:
            assert resp1.status == 201
            data1 = await resp1.json()
        
        async with client.post('/categories', json=category_payload_2) as resp2:
            assert resp2.status == 201
            data2 = await resp2.json()
        
        async with client.get('/categories') as get_all_resp:
            assert get_all_resp.status == 200
            response_data = await get_all_resp.json()
            assert len(response_data) == 2
            ids = [t["id"] for t in response_data]
            assert data1["id"] in ids
            assert data2["id"] in ids


@pytest.mark.asyncio
async def test_get_all_categories_empty(app):
    async with TestClient(TestServer(app)) as client:
        async with client.get('/categories') as resp:
            assert resp.status == 200
            response_data = await resp.json()
            assert len(response_data) == 0


@pytest.mark.asyncio
async def test_update_category_success(app, category_payload):
    async with TestClient(TestServer(app)) as client:
        async with client.post('/categories', json=category_payload) as create_resp:
            assert create_resp.status == 201
            created_data = await create_resp.json()
            category_id = created_data["id"]
        
        update_data = {
            "description": "Updated description"
        }
        
        async with client.put(f'/categories/{category_id}', json=update_data) as update_resp:
            assert update_resp.status == 200
            response_data = await update_resp.json()
            assert response_data["description"] == "Updated description"
            assert response_data["name"] == "Groceries"


@pytest.mark.asyncio
async def test_update_category_not_found(app):
    async with TestClient(TestServer(app)) as client:
        fake_id = str(uuid4())
        update_data = {"description": "Test"}
        async with client.put(f'/categories/{fake_id}', json=update_data) as resp:
            assert resp.status == 404


@pytest.mark.asyncio
async def test_update_category_invalid_uuid(app):
    async with TestClient(TestServer(app)) as client:
        async with client.put('/categories/invalid-uuid', json={"description": "Test"}) as resp:
            assert resp.status == 400


@pytest.mark.asyncio
async def test_delete_category_success(app, category_payload):
    async with TestClient(TestServer(app)) as client:
        async with client.post('/categories', json=category_payload) as create_resp:
            assert create_resp.status == 201
            created_data = await create_resp.json()
            category_id = created_data["id"]
        
        async with client.delete(f'/categories/{category_id}') as delete_resp:
            assert delete_resp.status == 200
            response_data = await delete_resp.json()
            assert "message" in response_data
        
        async with client.get(f'/categories/{category_id}') as get_resp:
            assert get_resp.status == 404


@pytest.mark.asyncio
async def test_delete_category_not_found(app):
    async with TestClient(TestServer(app)) as client:
        fake_id = str(uuid4())
        async with client.delete(f'/categories/{fake_id}') as resp:
            assert resp.status == 404


@pytest.mark.asyncio
async def test_delete_category_invalid_uuid(app):
    async with TestClient(TestServer(app)) as client:
        async with client.delete('/categories/invalid') as resp:
            assert resp.status == 400