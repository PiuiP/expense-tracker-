from aiohttp import web

from app.routes.transactions import routes as transaction_routes
from app.routes.categories import routes as category_routes

from app.repositories.fake_transaction import FakeTransactionRepository
from app.repositories.fake_category import FakeCategoryRepository

from app.services.transaction import TransactionService
from app.services.category import CategoryService


def create_app() -> web.Application:
    app = web.Application()

    tx_repo = FakeTransactionRepository()
    tx_service = TransactionService(tx_repo)
    
    cat_repo = FakeCategoryRepository()
    cat_service = CategoryService(cat_repo)
    
    app['transaction_service'] = tx_service
    app['category_service'] = cat_service
    
    app.add_routes(transaction_routes)
    app.add_routes(category_routes)
    
    return app

if __name__ == '__main__':
    app = create_app()
    web.run_app(app, host='0.0.0.0', port=8080)