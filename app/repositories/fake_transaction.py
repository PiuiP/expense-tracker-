from uuid import UUID, uuid4
from datetime import datetime
from decimal import Decimal

from app.repositories.transaction import ITransactionRepository
from app.models.transaction import TransactionResponse, TransactionCreate


class FakeTransactionRepository(ITransactionRepository):
    def __init__(self):
        self._storage_transaction: dict[UUID, TransactionResponse] = {}
        self._storage_trans_cat: dict[UUID, list[UUID]] = {} 

    async def create(self, model: TransactionCreate) -> TransactionResponse:
        new_uuid = uuid4()
        new_transaction = TransactionResponse(
            id=new_uuid,
            type_of_transaction=model.type_of_transaction,
            amount=model.amount,
            description=model.description,
            date_of_transaction=model.date_of_transaction,
            created_at=datetime.now()
        )
        self._storage_transaction[new_uuid] = new_transaction
        return self._storage_transaction[new_uuid]

    async def get_by_id(self, transaction_id: UUID) -> TransactionResponse:
        return self._storage_transaction.get(transaction_id)

    async def get_all(self) -> list[TransactionResponse]:
        return list(self._storage_transaction.values())

    async def update(self, transaction_id: UUID, model: TransactionCreate) -> TransactionResponse:
        if transaction_id not in self._storage_transaction:
            raise ValueError(f"Transaction with id {transaction_id} not found")
        
        original_created_at = self._storage_transaction[transaction_id].created_at
        
        updated_transaction = TransactionResponse(
            id=transaction_id,
            type_of_transaction=model.type_of_transaction,
            amount=model.amount,
            description=model.description,
            date_of_transaction=model.date_of_transaction,
            created_at=original_created_at
        )
        self._storage_transaction[transaction_id] = updated_transaction
        return updated_transaction
    
    async def delete(self, transaction_id: UUID) -> bool:
        if transaction_id in self._storage_transaction:
            del self._storage_transaction[transaction_id]
            if transaction_id in self._storage_trans_cat:
                del self._storage_trans_cat[transaction_id]
            return True
        return False
    
    async def add_categories(self, transaction_id: UUID, category_ids: list[UUID]) -> None:
        self._storage_trans_cat[transaction_id] = category_ids

    async def get_categories_by_transaction_id(self, transaction_id: UUID) -> list[UUID]:
        return self._storage_trans_cat.get(transaction_id, [])

    async def get_filtered(self, category_id: UUID | None, date_from: datetime, date_to: datetime) -> list[TransactionResponse]:
        result = []
        for transaction in self._storage_transaction.values():
            if not (date_from <= transaction.date_of_transaction <= date_to):
                continue
            
            if category_id is not None:
                cat_ids = self._storage_trans_cat.get(transaction.id, [])
                if category_id not in cat_ids:
                    continue
            
            result.append(transaction)

        return result
