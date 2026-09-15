from uuid import UUID

from pydantic import BaseModel


class TransactionCategoryCreate(BaseModel):
    transaction_id: UUID
    category_ids: list[UUID]


class TransactionCategoryResponse(BaseModel):
    transaction_id: UUID
    category_ids: list[UUID]
