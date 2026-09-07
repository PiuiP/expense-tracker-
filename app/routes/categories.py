from aiohttp import web
from uuid import UUID
from app.models.category import CategoryResponse, CategoryCreate
from app.services.category import CategoryService
from app.repositories.fake_category import FakeCategoryRepository

routes = web.RouteTableDef()

######fake -> sql
_repo = FakeCategoryRepository()
_service = CategoryService(_repo)

@routes.post('/categories')
async def create_category_handler(request: web.Request) -> web.Response:
    """POST /categories - create category"""
    try:
        body = await request.json()
        category_data = CategoryCreate(**body)
        result: CategoryResponse = await _service.create_category(category_data)
        return web.json_response(
            data=result.model_dump(mode='json'), 
            status=201
        )
    except Exception as e:
        return web.json_response(
            data={'error': str(e)},
            status=400
        )

@routes.get('/categories/{id}')
async def get_category_handler(request: web.Request) -> web.Response:
    """GET /categories/{id} - получить категорию по ID"""
    try:
        category_id = UUID(request.match_info['id'])
        result = await _service.get_category_by_id(category_id)

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

@routes.get('/categories')
async def get_all_categories_handler(request: web.Request) -> web.Response:
    """GET /categories - получить все категории"""
    try:
        result = await _service.get_all_categories()

        return web.json_response(
            data=[t.model_dump(mode='json') for t in result],
            status=200
        )
    except Exception as e:
        return web.json_response(
            data={'error': str(e)},
            status=500
        )

@routes.put('/categories/{id}')  # ← ВАЖНО: добавлен {id}
async def update_category_handler(request: web.Request) -> web.Response:
    """PUT /categories/{id} - обновить категорию"""
    try:
        category_id = UUID(request.match_info['id'])
        
        body = await request.json()
        
        result = await _service.update_category(category_id, body)
        
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


@routes.delete('/categories/{id}')
async def delete_category_handler(request: web.Request) -> web.Response:
    """DELETE /categories/{id} - удалить категорию"""
    try:
        category_id = UUID(request.match_info['id'])
        deleted = await _service.delete_category(category_id)
        
        if deleted:
            return web.json_response(
                data={'message': 'Category deleted successfully'},
                status=200
            )
        else:
            return web.json_response(
                data={'error': 'Category not found'},
                status=404
            )
        
    except ValueError:
        return web.json_response(
            data={'error': 'Invalid UUID format'},
            status=400
        )
    except Exception as e:
        return web.json_response(
            data={'error': str(e)},
            status=500
        )
