import pytest
from aiohttp.test_utils import TestClient, TestServer
from uuid import uuid4

from tests.conftest import app


@pytest.fixture
def transaction_payload():
    return {
        "type_of_transaction": "expense",
        "amount": 500.00,
        "description": "Покупка продуктов",
        "date_of_transaction": "2026-09-08T10:00:00",
        "category_ids": [str(uuid4())]
    }


@pytest.fixture
def transaction_payload_income():
    return {
        "type_of_transaction": "income",
        "amount": 480.20,
        "description": "Salary",
        "date_of_transaction": "2026-10-08T10:00:00",
        "category_ids": [str(uuid4())]
    }


@pytest.fixture
def invalid_payload_no_amount():
    """без обязательного поля amount"""
    return {
        "type_of_transaction": "expense",
        "description": "Тест без суммы",
        "date_of_transaction": "2026-09-08T10:00:00",
        "category_ids": []
    }


@pytest.fixture
def invalid_payload_wrong_type():
    """с невалидным типом amount"""
    return {
        "type_of_transaction": "expense",
        "amount": "not_a_number",
        "description": "Тест с неправильным типом",
        "date_of_transaction": "2026-09-08T10:00:00",
        "category_ids": []
    }


@pytest.mark.asyncio
async def test_create_transaction_success(app, transaction_payload):
    async with TestClient(TestServer(app)) as client:
        async with client.post('/transactions', json=transaction_payload) as resp:
            assert resp.status == 201
            
            response_data = await resp.json()
            
            assert response_data["type_of_transaction"] == "expense"
            assert response_data["amount"] == "500.0"
            assert "id" in response_data


@pytest.mark.asyncio
async def test_create_transaction_invalid_missing_field(app, invalid_payload_no_amount):
    async with TestClient(TestServer(app)) as client:
        async with client.post('/transactions', json=invalid_payload_no_amount) as resp:
            assert resp.status == 400
            
            response_data = await resp.json()
            assert "error" in response_data


@pytest.mark.asyncio
async def test_create_transaction_invalid_wrong_type(app, invalid_payload_wrong_type):
    async with TestClient(TestServer(app)) as client:
        async with client.post('/transactions', json=invalid_payload_wrong_type) as resp:
            assert resp.status == 400
            
            response_data = await resp.json()
            assert "error" in response_data



@pytest.mark.asyncio
async def test_get_by_id_success(app, transaction_payload):
    async with TestClient(TestServer(app)) as client:
        async with client.post('/transactions', json=transaction_payload) as create_resp:
            assert create_resp.status == 201
            created_data = await create_resp.json()
            transaction_id = created_data["id"]

        async with client.get(f'/transactions/{transaction_id}') as get_resp:
            assert get_resp.status == 200
            
            response_data = await get_resp.json()
            
            assert response_data["id"] == transaction_id
            assert response_data["type_of_transaction"] == "expense"


@pytest.mark.asyncio
async def test_get_by_id_invalid_uuid(app):
    async with TestClient(TestServer(app)) as client:
        async with client.get('/transactions/1') as get_resp:
            assert get_resp.status == 400
            
            response_data = await get_resp.json()
            assert response_data['error'] == 'Invalid UUID format'


@pytest.mark.asyncio
async def test_get_by_id_not_found(app):
    async with TestClient(TestServer(app)) as client:
        fake_id = str(uuid4())
        
        async with client.get(f'/transactions/{fake_id}') as get_resp:
            assert get_resp.status == 404



@pytest.mark.asyncio
async def test_get_all_success(app, transaction_payload, transaction_payload_income):
    async with TestClient(TestServer(app)) as client:
        async with client.post('/transactions', json=transaction_payload) as resp1:
            assert resp1.status == 201
            data1 = await resp1.json()
        
        async with client.post('/transactions', json=transaction_payload_income) as resp2:
            assert resp2.status == 201
            data2 = await resp2.json()
        
        async with client.get('/transactions') as get_all_resp:
            assert get_all_resp.status == 200
            
            response_data = await get_all_resp.json()
            
            assert len(response_data) == 2
            
            ids = [t["id"] for t in response_data]
            assert data1["id"] in ids
            assert data2["id"] in ids


@pytest.mark.asyncio
async def test_get_all_empty(app):
    async with TestClient(TestServer(app)) as client:
        async with client.get('/transactions') as resp:
            assert resp.status == 200
            
            response_data = await resp.json()
            assert len(response_data) == 0


@pytest.mark.asyncio
async def test_update_transaction_success(app, transaction_payload):
    async with TestClient(TestServer(app)) as client:
        async with client.post('/transactions', json=transaction_payload) as create_resp:
            assert create_resp.status == 201
            created_data = await create_resp.json()
            transaction_id = created_data["id"]
        
        update_data = {
            "description": "Обновлённое описание",
            "amount": 600.00
        }
        
        async with client.put(f'/transactions/{transaction_id}', json=update_data) as update_resp:
            assert update_resp.status == 200
            
            response_data = await update_resp.json()
            assert response_data["description"] == "Обновлённое описание"
            assert response_data["amount"] == "600.0"


@pytest.mark.asyncio
async def test_update_transaction_not_found(app):
    async with TestClient(TestServer(app)) as client:
        fake_id = str(uuid4())
        update_data = {"description": "Тест"}
        
        async with client.put(f'/transactions/{fake_id}', json=update_data) as resp:
            assert resp.status == 404


@pytest.mark.asyncio
async def test_update_transaction_invalid_uuid(app):
    async with TestClient(TestServer(app)) as client:
        async with client.put('/transactions/invalid-uuid', json={"description": "Тест"}) as resp:
            assert resp.status == 400


@pytest.mark.asyncio
async def test_delete_transaction_success(app, transaction_payload):
    async with TestClient(TestServer(app)) as client:
        async with client.post('/transactions', json=transaction_payload) as create_resp:
            assert create_resp.status == 201
            created_data = await create_resp.json()
            transaction_id = created_data["id"]

        async with client.delete(f'/transactions/{transaction_id}') as delete_resp:
            assert delete_resp.status == 200
            
            response_data = await delete_resp.json()
            assert "message" in response_data
        
        async with client.get(f'/transactions/{transaction_id}') as get_resp:
            assert get_resp.status == 404


@pytest.mark.asyncio
async def test_delete_transaction_not_found(app):
    async with TestClient(TestServer(app)) as client:
        fake_id = str(uuid4())
        
        async with client.delete(f'/transactions/{fake_id}') as resp:
            assert resp.status == 404


@pytest.mark.asyncio
async def test_delete_transaction_invalid_uuid(app):
    async with TestClient(TestServer(app)) as client:
        async with client.delete('/transactions/invalid') as resp:
            assert resp.status == 400


@pytest.mark.asyncio
async def test_filter_transactions_success(app, transaction_payload, transaction_payload_income):
    async with TestClient(TestServer(app)) as client:
        async with client.post('/transactions', json=transaction_payload) as resp1:
            assert resp1.status == 201
        
        async with client.post('/transactions', json=transaction_payload_income) as resp2:
            assert resp2.status == 201
        
        async with client.get('/transactions/filter?date_from=2026-09-01&date_to=2026-09-30') as filter_resp:
            assert filter_resp.status == 200
            
            response_data = await filter_resp.json()
            assert len(response_data) == 1
            assert response_data[0]["type_of_transaction"] == "expense"


@pytest.mark.asyncio
async def test_filter_transactions_missing_dates(app):
    async with TestClient(TestServer(app)) as client:
        async with client.get('/transactions/filter') as resp:
            assert resp.status == 400
            
            response_data = await resp.json()
            assert "error" in response_data


@pytest.mark.asyncio
async def test_get_stats_success(app, transaction_payload, transaction_payload_income):
    async with TestClient(TestServer(app)) as client:
        async with client.post('/transactions', json=transaction_payload) as resp1:
            assert resp1.status == 201
        
        async with client.post('/transactions', json=transaction_payload_income) as resp2:
            assert resp2.status == 201
        
        async with client.get('/transactions/stats') as stats_resp:
            assert stats_resp.status == 200
            
            response_data = await stats_resp.json()
            
            assert "total_income" in response_data
            assert "total_expense" in response_data
            assert "balance" in response_data
            assert response_data["total_income"] == "480.2"
            assert response_data["total_expense"] == "500.0"


@pytest.mark.asyncio
async def test_get_expenses_by_category_success(app, transaction_payload):
    async with TestClient(TestServer(app)) as client:
        async with client.post('/transactions', json=transaction_payload) as resp:
            assert resp.status == 201
        
        async with client.get('/transactions/expenses') as expenses_resp:
            assert expenses_resp.status == 200
            
            response_data = await expenses_resp.json()
            assert isinstance(response_data, dict)