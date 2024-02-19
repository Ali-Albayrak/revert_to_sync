
from typing import Optional, Union
from typing import Union
import uuid
import enum
import datetime

from pydantic import BaseModel, validator, EmailStr, Field
from core.encryptStr import EncryptStr




class CreateBrief_Swot(BaseModel):
    id: Optional[uuid.UUID]
    strength_keywords: Optional[str] = Field(default=None)
    strength_description: Optional[str] = Field(default=None)
    weakness_keywords: Optional[str] = Field(default=None)
    weakness_description: Optional[str] = Field(default=None)
    opportunities_keywords: Optional[str] = Field(default=None)
    opportunities_description: Optional[str] = Field(default=None)
    threats_keywords: Optional[str] = Field(default=None)
    threats_description: Optional[str] = Field(default=None)
    usps: Optional[str] = Field(default=None)
    challenges: Optional[str] = Field(default=None)
    your_reputation: Optional[str] = Field(default=None)
    occasions_of_best_sale: Optional[str] = Field(default=None)
    brief: uuid.UUID

    @validator('brief')
    def validate_brief(cls, brief: uuid.UUID):
        if False or False or False:
            raise ValueError(f"field <brief> is not allowed")
        return brief

class ReadBrief_Swot(BaseModel):
    id: uuid.UUID
    created_on: datetime.datetime
    updated_on: datetime.datetime
    created_by: Optional[uuid.UUID] = Field(default=None)
    updated_by: Optional[uuid.UUID] = Field(default=None)
    strength_keywords: Optional[str] = Field(default=None)
    strength_description: Optional[str] = Field(default=None)
    weakness_keywords: Optional[str] = Field(default=None)
    weakness_description: Optional[str] = Field(default=None)
    opportunities_keywords: Optional[str] = Field(default=None)
    opportunities_description: Optional[str] = Field(default=None)
    threats_keywords: Optional[str] = Field(default=None)
    threats_description: Optional[str] = Field(default=None)
    usps: Optional[str] = Field(default=None)
    challenges: Optional[str] = Field(default=None)
    your_reputation: Optional[str] = Field(default=None)
    occasions_of_best_sale: Optional[str] = Field(default=None)
    brief: Optional[uuid.UUID] = Field(default=None)
    brief__details: Optional[object] = Field(default={})


    class Config:
        orm_mode = True


class UpdateBrief_Swot(BaseModel):
    strength_keywords: Optional[str] = Field(default=None)
    strength_description: Optional[str] = Field(default=None)
    weakness_keywords: Optional[str] = Field(default=None)
    weakness_description: Optional[str] = Field(default=None)
    opportunities_keywords: Optional[str] = Field(default=None)
    opportunities_description: Optional[str] = Field(default=None)
    threats_keywords: Optional[str] = Field(default=None)
    threats_description: Optional[str] = Field(default=None)
    usps: Optional[str] = Field(default=None)
    challenges: Optional[str] = Field(default=None)
    your_reputation: Optional[str] = Field(default=None)
    occasions_of_best_sale: Optional[str] = Field(default=None)
    brief: Optional[uuid.UUID] = Field(default=None)


    class Config:
        orm_mode = True


class ReadBrief_Swots(BaseModel):
    data: list[Optional[ReadBrief_Swot]]
    next_page: Union[str, int]
    page_size: int