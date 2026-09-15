from uuid import UUID

import asyncpg

from app.models.category import CategoryCreate, CategoryResponse
from app.repositories.category import ICategoryRepository


class AsyncPGCategoryRepository(ICategoryRepository):
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def create(self, model: CategoryCreate) -> CategoryResponse:
        query = """
            INSERT INTO categories (name, description)
            VALUES ($1, $2)
            RETURNING id, name, description, created_at
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, model.name, model.description)
        return self._row_to_response(row)

    async def get_by_id(self, category_id: UUID) -> CategoryResponse | None:
        query = "SELECT id, name, description, created_at FROM categories WHERE id = $1"
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, category_id)
        return self._row_to_response(row) if row else None

    async def get_all(self) -> list[CategoryResponse]:
        query = "SELECT id, name, description, created_at FROM categories ORDER BY name"
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query)
        return [self._row_to_response(row) for row in rows]

    async def update(
        self, category_id: UUID, model: CategoryCreate
    ) -> CategoryResponse:
        query = """
            UPDATE categories
            SET name = $1, description = $2
            WHERE id = $3
            RETURNING id, name, description, created_at
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, model.name, model.description, category_id)
        if not row:
            raise ValueError(f"Категория с id {category_id} не найдена")
        return self._row_to_response(row)

    async def delete(self, category_id: UUID) -> bool:
        query = "DELETE FROM categories WHERE id = $1 RETURNING id"
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, category_id)
        return row is not None

    def _row_to_response(self, row: asyncpg.Record) -> CategoryResponse:
        return CategoryResponse(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            created_at=row["created_at"],
        )
