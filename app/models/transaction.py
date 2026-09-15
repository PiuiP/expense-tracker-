from datetime import datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class TransactionCreate(BaseModel):
    type_of_transaction: Literal["income", "expense"]
    amount: Decimal = Field(..., gt=0)
    description: str = Field(max_length=255, default=None)
    date_of_transaction: datetime


class TransactionResponse(BaseModel):
    id: UUID
    type_of_transaction: Literal["income", "expense"]
    amount: Decimal
    description: str | None
    date_of_transaction: datetime
    created_at: datetime
