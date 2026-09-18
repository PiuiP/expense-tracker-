from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from app.models.transaction import TransactionCreate, TransactionResponse


class ITransactionRepository(ABC):

    @abstractmethod
    async def create(self, model: TransactionCreate) -> TransactionResponse:
        pass

    @abstractmethod
    async def get_by_id(self, transaction_id: UUID) -> TransactionResponse:
        pass

    @abstractmethod
    async def get_all(self) -> list[TransactionResponse]:
        pass

    @abstractmethod
    async def update(
        self, transaction_id: UUID, model: TransactionCreate
    ) -> TransactionResponse:
        pass

    @abstractmethod
    async def delete(self, transaction_id: UUID) -> bool:
        pass

    # методы для связи с категориями

    @abstractmethod
    async def add_categories(
        self, transaction_id: UUID, category_ids: list[UUID]
    ) -> None:
        pass

    @abstractmethod
    async def get_categories_by_transaction_id(
        self, transaction_id: UUID
    ) -> list[UUID]:
        pass

    @abstractmethod
    async def get_filtered(
        self, category_id: UUID | None, date_from: datetime, date_to: datetime
    ) -> list[TransactionResponse]:
        pass

    @abstractmethod
    async def get_transaction_stats(self) -> dict[str, Decimal]:
        """Возвращает словарь {type_of_transaction: total_amount}"""
        pass

    @abstractmethod
    async def get_expenses_by_category(self) -> dict[str, Decimal]:
        """Возвращает словарь {category_name: total_expense}"""
        pass
