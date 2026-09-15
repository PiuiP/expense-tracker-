import os

import asyncpg
from aiohttp import web
from dotenv import load_dotenv

from app.dependencies import CATEGORY_SERVICE_KEY, TRANSACTION_SERVICE_KEY
from app.repositories.asyncpg_category import AsyncPGCategoryRepository
from app.repositories.asyncpg_transaction import AsyncPGTransactionRepository
from app.routes.categories import routes as category_routes
from app.routes.transactions import routes as transaction_routes
from app.services.category import CategoryService
from app.services.transaction import TransactionService

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


async def init_app(app: web.Application):
    """перед запуском сервера"""
    print("Подключение к PostgreSQL и создание пула соединений...")

    pool = await asyncpg.create_pool(DATABASE_URL)

    tx_repo = AsyncPGTransactionRepository(pool)
    cat_repo = AsyncPGCategoryRepository(pool)

    tx_service = TransactionService(tx_repo, cat_repo)
    cat_service = CategoryService(cat_repo)

    app["db_pool"] = pool
    app[TRANSACTION_SERVICE_KEY] = tx_service
    app[CATEGORY_SERVICE_KEY] = cat_service

    print("БД и сервисы успешно инициализированы!")


async def close_app(app: web.Application):
    """при корректной остановке приложения"""
    print("Закрытие соединений с БД...")
    await app["db_pool"].close()


def create_app() -> web.Application:
    app = web.Application()

    app.on_startup.append(init_app)
    app.on_cleanup.append(close_app)

    app.add_routes(transaction_routes)
    app.add_routes(category_routes)

    print("Начинаем работу!")

    return app


if __name__ == "__main__":
    app = create_app()
    web.run_app(app, host="0.0.0.0", port=8080)
