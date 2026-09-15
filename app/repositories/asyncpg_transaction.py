import asyncpg
from uuid import UUID
from decimal import Decimal
from datetime import datetime
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
        
        return self._row_to_response(row)

    async def get_by_id(self, transaction_id: UUID) -> TransactionResponse | None:
        query = """
            SELECT id, type_of_transaction, amount, description, date_of_transaction, created_at
            FROM transactions WHERE id = $1
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, transaction_id)
        return self._row_to_response(row) if row else None

    async def get_all(self) -> list[TransactionResponse]:
        query = """
            SELECT id, type_of_transaction, amount, description, date_of_transaction, created_at
            FROM transactions ORDER BY created_at DESC
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query)
        return [self._row_to_response(row) for row in rows]

    async def update(self, transaction_id: UUID, model: TransactionCreate) -> TransactionResponse:
        query = """
            UPDATE transactions
            SET type_of_transaction = $1, amount = $2, description = $3, date_of_transaction = $4
            WHERE id = $5
            RETURNING id, type_of_transaction, amount, description, date_of_transaction, created_at
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                query,
                model.type_of_transaction,
                float(model.amount),
                model.description,
                model.date_of_transaction,
                transaction_id
            )
        if not row:
            raise ValueError(f"Транзакция с id {transaction_id} не найдена")
        return self._row_to_response(row)

    async def delete(self, transaction_id: UUID) -> bool:
        #ON DELETE CASCADE в БД сам удалит записи из transaction_categories
        query = "DELETE FROM transactions WHERE id = $1 RETURNING id"
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, transaction_id)
        return row is not None

    async def add_categories(self, transaction_id: UUID, category_ids: list[UUID]) -> None:
        if not category_ids:
            return
        query = "INSERT INTO transaction_categories (transaction_id, category_id) VALUES ($1, $2)"
        async with self.pool.acquire() as conn:
            await conn.executemany(query, [(transaction_id, cat_id) for cat_id in category_ids])

    async def get_categories_by_transaction_id(self, transaction_id: UUID) -> list[UUID]:
        query = "SELECT category_id FROM transaction_categories WHERE transaction_id = $1"
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, transaction_id)
        return [row['category_id'] for row in rows]

    async def get_filtered(self, category_id: UUID | None, date_from: datetime, date_to: datetime) -> list[TransactionResponse]:
        query = """
            SELECT DISTINCT t.id, t.type_of_transaction, t.amount, t.description, t.date_of_transaction, t.created_at
            FROM transactions t
            LEFT JOIN transaction_categories tc ON t.id = tc.transaction_id
            WHERE t.date_of_transaction >= $1 AND t.date_of_transaction <= $2
        """
        params = [date_from, date_to]
        
        if category_id:
            query += " AND tc.category_id = $3"
            params.append(category_id)
            
        query += " ORDER BY t.created_at DESC"

        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, *params)
        return [self._row_to_response(row) for row in rows]

    #чтобы не дублировать код маппинга
    def _row_to_response(self, row: asyncpg.Record) -> TransactionResponse:
        return TransactionResponse(
            id=row['id'],
            type_of_transaction=row['type_of_transaction'],
            amount=Decimal(str(row['amount'])),
            description=row['description'],
            date_of_transaction=row['date_of_transaction'],
            created_at=row['created_at']
        )