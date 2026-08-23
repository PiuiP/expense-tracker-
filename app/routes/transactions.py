from aiohttp import web
from uuid import UUID
from app.models.transaction import TransactionCreate, TransactionResponse
from app.services.transaction import TransactionService
from app.repositories.fake_transaction import FakeTransactionRepository

routes = web.RouteTableDef()

#пока фейк потом на SQL
_repo = FakeTransactionRepository()
_service = TransactionService(_repo)


@routes.post('/transactions')
async def create_transaction_handler(request: web.Request) -> web.Response:
    """POST /transactions - создать транзакцию"""
    try:
        body = await request.json()
        
        category_ids_raw = body.pop('category_ids', [])
        category_ids = [UUID(cid) for cid in category_ids_raw]
        
        transaction_data = TransactionCreate(**body)
        
        result: TransactionResponse = await _service.create_transaction(transaction_data, category_ids)
        
        return web.json_response(
            data=result.model_dump(mode='json'),  #конвертирует UUID/datetime в строки
            status=201
        )
        
    except Exception as e:
        return web.json_response(
            data={'error': str(e)},
            status=400
        )


@routes.get('/transactions/{id}')
async def get_transaction_handler(request: web.Request) -> web.Response:
    """GET /transactions/{id} - получить транзакцию по ID"""
    try:
        transaction_id = UUID(request.match_info['id'])
        result = await _service.get_transaction_by_id(transaction_id)
        
        return web.json_response(
            data=result.model_dump(mode='json'),
            status=200
        )
        
    except ValueError:
        # невалидный UUID
        return web.json_response(
            data={'error': 'Invalid UUID format'},
            status=400
        )
    except Exception as e:
        return web.json_response(
            data={'error': str(e)},
            status=404
        )


@routes.get('/transactions')
async def get_all_transactions_handler(request: web.Request) -> web.Response:
    """GET /transactions - получить все транзакции"""
    try:
        result = await _service.get_all_transactions()
        
        return web.json_response(
            data=[t.model_dump(mode='json') for t in result],
            status=200
        )
        
    except Exception as e:
        return web.json_response(
            data={'error': str(e)},
            status=500
        )