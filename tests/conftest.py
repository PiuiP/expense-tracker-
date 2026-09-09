import pytest

from app.main import create_app
from app.dependencies import TRANSACTION_SERVICE_KEY, CATEGORY_SERVICE_KEY
from app.repositories.fake_transaction import FakeTransactionRepository
from app.repositories.fake_category import FakeCategoryRepository
from app.services.transaction import TransactionService
from app.services.category import CategoryService

@pytest.fixture
def app():
    """приложение с фейковыми зависимостями для тестов"""
    application = create_app()
    
    # Перезаписываем сервисы на фейковые
    fake_tx_repo = FakeTransactionRepository()
    fake_cat_repo = FakeCategoryRepository()
    
    application[TRANSACTION_SERVICE_KEY] = TransactionService(fake_tx_repo, fake_cat_repo)
    application[CATEGORY_SERVICE_KEY] = CategoryService(fake_cat_repo)
    
    return application