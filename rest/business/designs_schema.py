
from typing import Optional, Union
from typing import Union
import uuid
import enum
import datetime

from pydantic import BaseModel, validator, EmailStr, Field
from core.encryptStr import EncryptStr


# select enums
class TypeEnum(str, enum.Enum):
    local = "local"
    vistaCreate = "vistaCreate"


class CreateDesign(BaseModel):
    id: Optional[uuid.UUID]
    design_link: Optional[str] = Field(default=None)
    text_on_design: Optional[str] = Field(default=None)
    content_name: Optional[str] = Field(default=None)
    type: Optional[TypeEnum]
    included_offer: Optional[str] = Field(default=None)
    notes: Optional[str] = Field(default=None)
    customer: Optional[uuid.UUID] = Field(default=None)
    strategy_content: Optional[uuid.UUID] = Field(default=None)

    @validator('type')
    def validate_type(cls, type: Optional[TypeEnum]):
        if False or False or False:
            raise ValueError(f"field <type> is not allowed")
        return type
    @validator('customer')
    def validate_customer(cls, customer: Optional[uuid.UUID] = Field(default=None)):
        if False or False or False:
            raise ValueError(f"field <customer> is not allowed")
        return customer
    @validator('strategy_content')
    def validate_strategy_content(cls, strategy_content: Optional[uuid.UUID] = Field(default=None)):
        if False or False or False:
            raise ValueError(f"field <strategy_content> is not allowed")
        return strategy_content

class ReadDesign(BaseModel):
    id: uuid.UUID
    created_on: datetime.datetime
    updated_on: datetime.datetime
    created_by: Optional[uuid.UUID] = Field(default=None)
    updated_by: Optional[uuid.UUID] = Field(default=None)
    design_link: Optional[str] = Field(default=None)
    text_on_design: Optional[str] = Field(default=None)
    content_name: Optional[str] = Field(default=None)
    type: Optional[TypeEnum]
    included_offer: Optional[str] = Field(default=None)
    notes: Optional[str] = Field(default=None)
    customer: Optional[uuid.UUID] = Field(default=None)
    customer__details: Optional[object] = Field(default={})
    strategy_content: Optional[uuid.UUID] = Field(default=None)
    strategy_content__details: Optional[object] = Field(default={})


    @validator('type')
    def validate_type(cls, type: Optional[TypeEnum]):
        return type

    class Config:
        orm_mode = True


class UpdateDesign(BaseModel):
    design_link: Optional[str] = Field(default=None)
    text_on_design: Optional[str] = Field(default=None)
    content_name: Optional[str] = Field(default=None)
    type: Optional[TypeEnum]
    included_offer: Optional[str] = Field(default=None)
    notes: Optional[str] = Field(default=None)
    customer: Optional[uuid.UUID] = Field(default=None)
    strategy_content: Optional[uuid.UUID] = Field(default=None)


    @validator('type')
    def validate_type(cls, type: Optional[TypeEnum]):
        if False or '__' in type or type in ['id']:
            raise ValueError(f"field <type> is not allowed")
        return type

    class Config:
        orm_mode = True


class ReadDesigns(BaseModel):
    data: list[Optional[ReadDesign]]
    next_page: Union[str, int]
    page_size: int