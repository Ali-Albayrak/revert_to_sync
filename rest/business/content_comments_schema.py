
from typing import Optional, Union
from typing import Union
import uuid
import enum
import datetime

from pydantic import BaseModel, validator, EmailStr, Field
from core.encryptStr import EncryptStr


# select enums
class TypeEnum(str, enum.Enum):
    content = "content"
    design = "design"


class CreateContent_Comment(BaseModel):
    id: Optional[uuid.UUID]
    comment: Optional[str] = Field(default=None)
    type: Optional[TypeEnum]
    strategy_content: Optional[uuid.UUID] = Field(default=None)

    @validator('type')
    def validate_type(cls, type: Optional[TypeEnum]):
        if False or False or False:
            raise ValueError(f"field <type> is not allowed")
        return type
    @validator('strategy_content')
    def validate_strategy_content(cls, strategy_content: Optional[uuid.UUID] = Field(default=None)):
        if False or False or False:
            raise ValueError(f"field <strategy_content> is not allowed")
        return strategy_content

class ReadContent_Comment(BaseModel):
    id: uuid.UUID
    created_on: datetime.datetime
    updated_on: datetime.datetime
    created_by: Optional[uuid.UUID] = Field(default=None)
    updated_by: Optional[uuid.UUID] = Field(default=None)
    comment: Optional[str] = Field(default=None)
    type: Optional[TypeEnum]
    strategy_content: Optional[uuid.UUID] = Field(default=None)
    strategy_content__details: Optional[object] = Field(default={})


    @validator('type')
    def validate_type(cls, type: Optional[TypeEnum]):
        return type

    class Config:
        orm_mode = True


class UpdateContent_Comment(BaseModel):
    comment: Optional[str] = Field(default=None)
    type: Optional[TypeEnum]
    strategy_content: Optional[uuid.UUID] = Field(default=None)


    @validator('type')
    def validate_type(cls, type: Optional[TypeEnum]):
        if False or '__' in type or type in ['id']:
            raise ValueError(f"field <type> is not allowed")
        return type

    class Config:
        orm_mode = True


class ReadContent_Comments(BaseModel):
    data: list[Optional[ReadContent_Comment]]
    next_page: Union[str, int]
    page_size: int