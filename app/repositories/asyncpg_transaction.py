import asyncpg
from uuid import UUID
from decimal import Decimal
from app.models.transaction import TransactionCreate, TransactionResponse
from app.repositories.transaction import ITransactionRepository

class AsyncPGTransactionRepository(ITransactionRepository):
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def create(self, model: TransactionCreate) -> TransactionResponse:
        query = """
            INSERT INTO transactions (type_of_transaction, amount, description, date_of_transaction)
            VALUES ($1, $2, $3, $4)
            RETURNING id, type_of_transaction, amount, description, date_of_transaction, created_at
        """
        
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                query,
                model.type_of_transaction,
                float(model.amount),
                model.description,
                model.date_of_transaction
            )
        
        return TransactionResponse(
            id=row['id'],
            type_of_transaction=row['type_of_transaction'],
            amount=Decimal(str(row['amount'])),
            description=row['description'],
            date_of_transaction=row['date_of_transaction'],
            created_at=row['created_at']
        )

    async def get_by_id(self, transaction_id: UUID) -> TransactionResponse | None:
        query = """
            SELECT id, type_of_transaction, amount, description, date_of_transaction, created_at
            FROM transactions
            WHERE id = $1
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, transaction_id)
            
        if not row:
            return None
            
        return TransactionResponse(
            id=row['id'],
            type_of_transaction=row['type_of_transaction'],
            amount=Decimal(str(row['amount'])),
            description=row['description'],
            date_of_transaction=row['date_of_transaction'],
            created_at=row['created_at']
        )

    async def get_all(self) -> list[TransactionResponse]:
        query = """
            SELECT id, type_of_transaction, amount, description, date_of_transaction, created_at
            FROM transactions
            ORDER BY created_at DESC
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query)
            
        return [
            TransactionResponse(
                id=row['id'],
                type_of_transaction=row['type_of_transaction'],
                amount=Decimal(str(row['amount'])),
                description=row['description'],
                date_of_transaction=row['date_of_transaction'],
                created_at=row['created_at']
            )
            for row in rows
        ]


    async def update(self, transaction_id: UUID, model: TransactionCreate) -> TransactionResponse:
        raise NotImplementedError("Пока не реализовано")

    async def delete(self, transaction_id: UUID) -> bool:
        raise NotImplementedError("Пока не реализовано")
        
    async def add_categories(self, transaction_id: UUID, category_ids: list[UUID]) -> None:
        raise NotImplementedError("Пока не реализовано")
        
    async def get_categories_by_transaction_id(self, transaction_id: UUID) -> list[UUID]:
        return []
        
    async def get_filtered(self, category_id: UUID | None, date_from, date_to) -> list[TransactionResponse]:
        raise NotImplementedError("Пока не реализовано")