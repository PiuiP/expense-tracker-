from uuid import UUID

from app.models.transaction import TransactionCreate, TransactionResponse
from app.repositories.transaction import ITransactionRepository

class TransactionService():
    def __init__(self, repository: ITransactionRepository):
        self.repository = repository

    async def create_transaction(self, data: TransactionCreate, category_ids: list[UUID]) -> TransactionResponse:
        transaction = await self.repository.create(data)
        await self.repository.add_categories(transaction.id, category_ids)
        return transaction

    async def get_transaction_by_id(self, transaction_id: UUID) -> TransactionResponse:
        return await self.repository.get_by_id(transaction_id)

    async def get_all_transactions(self) -> list[TransactionResponse]:
        return await self.repository.get_all()
