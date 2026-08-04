from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class CategoryCreate(BaseModel):
    name: str = Field(...,min_length=1, max_length=100) #'...' - обязательное поле, хотя без default оно и так типа обязательное
    description: str = Field(max_length=255, default=None)

class CategoryResponse(BaseModel):
    id: UUID
    name: str 
    description: str | None
    created_at: datetime



