from aiohttp import web

from app.routes.transactions import routes as transaction_routes
from app.routes.categories import routes as category_routes

from app.repositories.fake_transaction import FakeTransactionRepository
from app.repositories.fake_category import FakeCategoryRepository

from app.services.transaction import TransactionService
from app.services.category import CategoryService

from app.dependencies import TRANSACTION_SERVICE_KEY, CATEGORY_SERVICE_KEY

def create_app() -> web.Application:
    app = web.Application()

    tx_repo = FakeTransactionRepository()
    cat_repo = FakeCategoryRepository()
    
    tx_service = TransactionService(tx_repo, cat_repo)
    cat_service = CategoryService(cat_repo)
    
    app[TRANSACTION_SERVICE_KEY] = tx_service
    app[CATEGORY_SERVICE_KEY] = cat_service
    
    app.add_routes(transaction_routes)
    app.add_routes(category_routes)
    
    return app

if __name__ == '__main__':
    app = create_app()
    web.run_app(app, host='0.0.0.0', port=8080)