
from typing import Optional, Union
from typing import Union
import uuid
import enum
import datetime

from pydantic import BaseModel, validator, EmailStr, Field
from core.encryptStr import EncryptStr




class CreateBrief_Extra(BaseModel):
    id: Optional[uuid.UUID]
    extra_details: Optional[str] = Field(default=None)
    brief: uuid.UUID

    @validator('brief')
    def validate_brief(cls, brief: uuid.UUID):
        if False or False or False:
            raise ValueError(f"field <brief> is not allowed")
        return brief

class ReadBrief_Extra(BaseModel):
    id: uuid.UUID
    created_on: datetime.datetime
    updated_on: datetime.datetime
    created_by: Optional[uuid.UUID] = Field(default=None)
    updated_by: Optional[uuid.UUID] = Field(default=None)
    extra_details: Optional[str] = Field(default=None)
    brief: Optional[uuid.UUID] = Field(default=None)
    brief__details: Optional[object] = Field(default={})


    class Config:
        orm_mode = True


class UpdateBrief_Extra(BaseModel):
    extra_details: Optional[str] = Field(default=None)
    brief: Optional[uuid.UUID] = Field(default=None)


    class Config:
        orm_mode = True


class ReadBrief_Extras(BaseModel):
    data: list[Optional[ReadBrief_Extra]]
    next_page: Union[str, int]
    page_size: int