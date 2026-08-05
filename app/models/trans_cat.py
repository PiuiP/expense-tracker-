from pydantic import BaseModel, Field
from uuid import UUID

class TransactionCategoryCreate(BaseModel):
    transaction_id: UUID
    category_ids: list[UUID] 

class TransactionCategoryResponse(BaseModel):
    transaction_id: UUID
    category_ids: list[UUID]