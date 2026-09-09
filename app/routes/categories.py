from aiohttp import web
from uuid import UUID

from app.models.category import CategoryResponse, CategoryCreate
from app.dependencies import CATEGORY_SERVICE_KEY

routes = web.RouteTableDef()


@routes.post('/categories')
async def create_category_handler(request: web.Request) -> web.Response:
    """POST /categories - create category"""
    service = request.app[CATEGORY_SERVICE_KEY]
    try:
        body = await request.json()
        category_data = CategoryCreate(**body)
        result: CategoryResponse = await service.create_category(category_data)
        return web.json_response(
            data=result.model_dump(mode='json'), 
            status=201
        )
    except Exception as e:
        return web.json_response(
            data={'error': str(e)},
            status=400
        )

@routes.get('/categories')
async def get_all_categories_handler(request: web.Request) -> web.Response:
    """GET /categories - получить все категории"""
    service = request.app[CATEGORY_SERVICE_KEY]
    try:
        result = await service.get_all_categories()

        return web.json_response(
            data=[t.model_dump(mode='json') for t in result],
            status=200
        )
    except Exception as e:
        return web.json_response(
            data={'error': str(e)},
            status=500
        )

@routes.get('/categories/{id}')
async def get_category_handler(request: web.Request) -> web.Response:
    """GET /categories/{id} - получить категорию по ID"""
    service = request.app[CATEGORY_SERVICE_KEY]
    try:
        category_id = UUID(request.match_info['id'])
        result = await service.get_category_by_id(category_id)

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

@routes.put('/categories/{id}')
async def update_category_handler(request: web.Request) -> web.Response:
    service = request.app[CATEGORY_SERVICE_KEY]
    try:
        category_id = UUID(request.match_info['id'])

    except ValueError:
        return web.json_response(
            data={'error': 'Invalid UUID format'}, 
            status=400
        )
    
    try:
        body = await request.json()

        result = await service.update_category(category_id, body)
        return web.json_response(
            data=result.model_dump(
                mode='json'), 
                status=200
            )
    
    except ValueError as e:
        return web.json_response(
            data={'error': str(e)}, 
            status=404
        )
    except Exception as e:
        return web.json_response(
            data={'error': str(e)}, 
            status=500
        )

@routes.delete('/categories/{id}')
async def delete_category_handler(request: web.Request) -> web.Response:
    service = request.app[CATEGORY_SERVICE_KEY]
    try:
        category_id = UUID(request.match_info['id'])
    except ValueError:
        return web.json_response(
            data={'error': 'Invalid UUID format'}, 
            status=400
        )
    
    try:
        deleted = await service.delete_category(category_id)
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
    except Exception as e:
        return web.json_response(
            data={'error': str(e)}, 
            status=500
        )
