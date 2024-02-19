
from typing import Optional, Union
from typing import Union
import uuid
import enum
import datetime

from pydantic import BaseModel, validator, EmailStr, Field
from core.encryptStr import EncryptStr


# select enums
class TypeEnum(str, enum.Enum):
    best_sale = "best_sale"
    top_sale = "top_sale"
    offer = "offer"


class CreateBrief_Product(BaseModel):
    id: Optional[uuid.UUID]
    product_image: Optional[uuid.UUID] = Field(default=None)
    product_name: Optional[str] = Field(default=None)
    price: Optional[int] = Field(default=None)
    type: Optional[TypeEnum]
    discount: Optional[int] = Field(default=None)
    brief: uuid.UUID

    @validator('type')
    def validate_type(cls, type: Optional[TypeEnum]):
        if False or False or False:
            raise ValueError(f"field <type> is not allowed")
        return type
    @validator('brief')
    def validate_brief(cls, brief: uuid.UUID):
        if False or False or False:
            raise ValueError(f"field <brief> is not allowed")
        return brief

class ReadBrief_Product(BaseModel):
    id: uuid.UUID
    created_on: datetime.datetime
    updated_on: datetime.datetime
    created_by: Optional[uuid.UUID] = Field(default=None)
    updated_by: Optional[uuid.UUID] = Field(default=None)
    product_image: Optional[uuid.UUID] = Field(default=None)
    product_name: Optional[str] = Field(default=None)
    price: Optional[int] = Field(default=None)
    type: Optional[TypeEnum]
    discount: Optional[int] = Field(default=None)
    brief: Optional[uuid.UUID] = Field(default=None)
    brief__details: Optional[object] = Field(default={})


    @validator('type')
    def validate_type(cls, type: Optional[TypeEnum]):
        return type

    class Config:
        orm_mode = True


class UpdateBrief_Product(BaseModel):
    product_image: Optional[uuid.UUID] = Field(default=None)
    product_name: Optional[str] = Field(default=None)
    price: Optional[int] = Field(default=None)
    type: Optional[TypeEnum]
    discount: Optional[int] = Field(default=None)
    brief: Optional[uuid.UUID] = Field(default=None)


    @validator('type')
    def validate_type(cls, type: Optional[TypeEnum]):
        if False or '__' in type or type in ['id']:
            raise ValueError(f"field <type> is not allowed")
        return type

    class Config:
        orm_mode = True


class ReadBrief_Products(BaseModel):
    data: list[Optional[ReadBrief_Product]]
    next_page: Union[str, int]
    page_size: int