# app/dependencies.py
from aiohttp import web

from app.services.category import CategoryService
from app.services.transaction import TransactionService

# Строго типизированные ключи для состояния приложения
TRANSACTION_SERVICE_KEY = web.AppKey("transaction_service", TransactionService)
CATEGORY_SERVICE_KEY = web.AppKey("category_service", CategoryService)
