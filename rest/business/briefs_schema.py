
from typing import Optional, Union
from typing import Union
import uuid
import enum
import datetime

from pydantic import BaseModel, validator, EmailStr, Field
from core.encryptStr import EncryptStr


# select enums
class StatusEnum(str, enum.Enum):
    pending = "pending"
    todo = "todo"
    completed = "completed"


class CreateBrief(BaseModel):
    id: Optional[uuid.UUID]
    customer: Optional[uuid.UUID] = Field(default=None)
    extra_details: Optional[str] = Field(default=None)
    status: Optional[StatusEnum]

    @validator('customer')
    def validate_customer(cls, customer: Optional[uuid.UUID] = Field(default=None)):
        if False or False or False:
            raise ValueError(f"field <customer> is not allowed")
        return customer
    @validator('status')
    def validate_status(cls, status: Optional[StatusEnum]):
        if False or False or False:
            raise ValueError(f"field <status> is not allowed")
        return status

class ReadBrief(BaseModel):
    id: uuid.UUID
    created_on: datetime.datetime
    updated_on: datetime.datetime
    created_by: Optional[uuid.UUID] = Field(default=None)
    updated_by: Optional[uuid.UUID] = Field(default=None)
    customer: Optional[uuid.UUID] = Field(default=None)
    customer__details: Optional[object] = Field(default={})
    brief_platforms: Optional[list[object]] = Field(default=[{}])
    brief_competitors: Optional[list[object]] = Field(default=[{}])
    brief_products: Optional[list[object]] = Field(default=[{}])
    brief_audiences: Optional[list[object]] = Field(default=[{}])
    brief_personas: Optional[list[object]] = Field(default=[{}])
    brief_swots: Optional[list[object]] = Field(default=[{}])
    brief_marketings: Optional[list[object]] = Field(default=[{}])
    brief_objectives: Optional[list[object]] = Field(default=[{}])
    brief_businesses: Optional[list[object]] = Field(default=[{}])
    brief_extras: Optional[list[object]] = Field(default=[{}])
    extra_details: Optional[str] = Field(default=None)
    status: Optional[StatusEnum]


    @validator('status')
    def validate_status(cls, status: Optional[StatusEnum]):
        return status

    class Config:
        orm_mode = True


class UpdateBrief(BaseModel):
    customer: Optional[uuid.UUID] = Field(default=None)
    extra_details: Optional[str] = Field(default=None)
    status: Optional[StatusEnum]


    @validator('status')
    def validate_status(cls, status: Optional[StatusEnum]):
        if False or '__' in status or status in ['id']:
            raise ValueError(f"field <status> is not allowed")
        return status

    class Config:
        orm_mode = True


class ReadBriefs(BaseModel):
    data: list[Optional[ReadBrief]]
    next_page: Union[str, int]
    page_size: int