import pytest
from decimal import Decimal
from pydantic import ValidationError

from app.models.category import CategoryCreate
from app.models.transaction import TransactionCreate

# CategoryCreate

def test_category_create_name_too_long():
    """отклоняет слишком длинное имя"""
    with pytest.raises(ValidationError):
        CategoryCreate(name="A" * 101) # 101 символ, а лимит 100

def test_category_create_empty_name():
    """пустая строка в имени вызывает ошибку"""
    with pytest.raises(ValidationError):
        CategoryCreate(name="", description="Тест")

def test_category_create_missing_name():
    """отсутствие обязательного поля name вызывает ошибку"""
    with pytest.raises(ValidationError):
        # только description, name пропускаем
        CategoryCreate(description="Только описание")


#TransactionCreate

def test_transaction_create_negative_amount():
    """нельзя создать транзакцию с отрицательной суммой."""
    with pytest.raises(ValidationError):
        TransactionCreate(type_of_transaction="expense", amount=-50.0)

def test_transaction_create_invalid_type():
    """неверный тип транзакции вызывает ошибку."""
    with pytest.raises(ValidationError):
        TransactionCreate(
            type_of_transaction="salary", #в literal нет такого 
            amount=100.50,
            date_of_transaction="2026-08-05T12:00:00"
        )