import pytest

from app.dependencies import CATEGORY_SERVICE_KEY, TRANSACTION_SERVICE_KEY
from app.main import create_app
from app.repositories.fake_category import FakeCategoryRepository
from app.repositories.fake_transaction import FakeTransactionRepository
from app.services.category import CategoryService
from app.services.transaction import TransactionService


@pytest.fixture
def app():
    """Приложение с фейковыми зависимостями для тестов"""
    application = create_app()

    # Перезаписываем сервисы на фейковые
    fake_tx_repo = FakeTransactionRepository()
    fake_cat_repo = FakeCategoryRepository()

    application[TRANSACTION_SERVICE_KEY] = TransactionService(
        fake_tx_repo, fake_cat_repo
    )
    application[CATEGORY_SERVICE_KEY] = CategoryService(fake_cat_repo)

    # ВАЖНО: очищаем хуки запуска, чтобы TestServer не пытался
    # подключиться к реальной PostgreSQL при старте
    application.on_startup.clear()
    application.on_cleanup.clear()

    return application
