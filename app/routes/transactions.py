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

@routes.put('/transactions/{id}')
async def update_transaction_handler(request: web.Request) -> web.Response:
    """PUT /transactions/{id} - обновить транзакцию"""
    try:
        transaction_id = UUID(request.match_info['id'])
        
        body = await request.json()
        
        result = await _service.update_transaction(transaction_id, body)
        
        return web.json_response(
            data=result.model_dump(mode='json'),
            status=200
        )
        
    except ValueError:
        return web.json_response(
            data={'error': 'Invalid UUID format'},
            status=400
        )
    except Exception as e:
        return web.json_response(
            data={'error': str(e)},
            status=404
        )
        
@routes.delete('/transactions/{id}')
async def delete_transaction_handler(request: web.Request) -> web.Response:
    """DELETE /transactions/{id} - удалить транзакцию"""
    try:
        transaction_id = UUID(request.match_info['id'])

        result = await _service.delete_transaction(transaction_id) #-> bool
        
        if result:
            return web.json_response(
                data={'message': 'Transaction is deleted successfully'},
                status=200
            )
        else:
            return web.json_response(
                data={'error': 'Transaction is nto found'},
                status=404
            )
        
    except ValueError:
        return web.json_response(
            data={'error': 'Invalid UUID format'},
            status=400
        )


@routes.get('/transactions/filter')
async def filter_transactions_handler(request: web.Request) -> web.Response:
    """GET /transactions/filter?category_id=...&date_from=...&date_to=..."""
    try:
        category_id = request.query.get('category_id', None)
        date_from = request.query.get('date_from')
        date_to = request.query.get('date_to')

        cat_uuid = UUID(category_id) if category_id else None #if UUID(None) -> ERRRROR((((
        result = await _service.get_filtered_transactions(cat_uuid, date_from, date_to)

        #result - list -> model_dump for each element (!!!!!model_dump cannot be applied to lists, only pydentic-models!!!!!)
        return web.json_response(
            data=[t.model_dump(mode='json') for t in result], 
            status=200
        )
        
    except ValueError as e:
        return web.json_response(data={'error': str(e)}, status=400)

@routes.get('/transactions/stats')
async def get_stats_handler(request: web.Request) -> web.Response:
    """GET /transactions/stats - статистика по транзакциям"""
    try:
        stats = await _service.get_transaction_stats() #-> dict

        return web.json_response(
            data=stats,
            status=200
        )
    except Exception as e:
        return web.json_response(
            data={'error': str(e)},
            status=500
        )

@routes.get('/transactions/expenses')
async def get_expenses_by_category_handler(request: web.Request) -> web.Response:
    """GET /transactions/expenses - сумма трат по категориям"""
    try:
        expenses = await _service.get_expenses_by_category() #-> dict

        return web.json_response(
            data=expenses,
            status=200
        )
    except Exception as e:
        return web.json_response(
            data={'error': str(e)},
            status=500
        )

