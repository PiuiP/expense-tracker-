from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from app.models.transaction import TransactionCreate
from app.repositories.fake_category import FakeCategoryRepository
from app.repositories.fake_transaction import FakeTransactionRepository
from app.services.transaction import TransactionService


async def test_create_transaction_with_categories():
    tx_repo = FakeTransactionRepository()
    cat_repo = FakeCategoryRepository()
    service = TransactionService(tx_repo, cat_repo)

    data = TransactionCreate(
        type_of_transaction="expense",
        amount=Decimal("500.00"),
        description="Продукты",
        date_of_transaction=datetime.now(),
    )

    category_ids = [uuid4(), uuid4()]

    result = await service.create_transaction(data, category_ids)

    assert result.type_of_transaction == "expense"
    assert result.amount == Decimal("500.00")
    assert result.description == "Продукты"
    assert isinstance(result.id, UUID)

    fetched_categories = await tx_repo.get_categories_by_transaction_id(result.id)
    assert len(fetched_categories) == 2
    assert category_ids[0] in fetched_categories
    assert category_ids[1] in fetched_categories


async def test_get_transaction_by_id():
    tx_repo = FakeTransactionRepository()
    cat_repo = FakeCategoryRepository()
    service = TransactionService(tx_repo, cat_repo)

    data = TransactionCreate(
        type_of_transaction="income",
        amount=Decimal("1000.00"),
        description="Зарплата",
        date_of_transaction=datetime.now(),
    )

    created_transaction = await service.create_transaction(data, [])
    target_id = created_transaction.id

    result = await service.get_transaction_by_id(target_id)

    assert result.id == target_id
    assert result.type_of_transaction == "income"
    assert result.amount == Decimal("1000.00")
    assert result.description == "Зарплата"


async def test_get_all_transactions():
    tx_repo = FakeTransactionRepository()
    cat_repo = FakeCategoryRepository()
    service = TransactionService(tx_repo, cat_repo)

    data1 = TransactionCreate(
        type_of_transaction="expense",
        amount=Decimal("100.00"),
        description="Кофе",
        date_of_transaction=datetime.now(),
    )
    data2 = TransactionCreate(
        type_of_transaction="expense",
        amount=Decimal("200.00"),
        description="Обед",
        date_of_transaction=datetime.now(),
    )

    await service.create_transaction(data1, [])
    await service.create_transaction(data2, [])

    result = await service.get_all_transactions()
    assert len(result) == 2

    fetched_ids = [t.id for t in result]
    assert len(fetched_ids) == 2
