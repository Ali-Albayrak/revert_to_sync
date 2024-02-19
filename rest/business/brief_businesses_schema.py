
from typing import Optional, Union
from typing import Union
import uuid
import enum
import datetime

from pydantic import BaseModel, validator, EmailStr, Field
from core.encryptStr import EncryptStr


# select enums
class AccordingToEnum(str, enum.Enum):
    weekly = "weekly"
    monthly = "monthly"
    yearly = "yearly"


class CreateBrief_Business(BaseModel):
    id: Optional[uuid.UUID]
    key: Optional[str] = Field(default=None)
    value: Optional[int] = Field(default=None)
    according_to: Optional[AccordingToEnum]
    brief: uuid.UUID

    @validator('according_to')
    def validate_according_to(cls, according_to: Optional[AccordingToEnum]):
        if False or False or False:
            raise ValueError(f"field <according_to> is not allowed")
        return according_to
    @validator('brief')
    def validate_brief(cls, brief: uuid.UUID):
        if False or False or False:
            raise ValueError(f"field <brief> is not allowed")
        return brief

class ReadBrief_Business(BaseModel):
    id: uuid.UUID
    created_on: datetime.datetime
    updated_on: datetime.datetime
    created_by: Optional[uuid.UUID] = Field(default=None)
    updated_by: Optional[uuid.UUID] = Field(default=None)
    key: Optional[str] = Field(default=None)
    value: Optional[int] = Field(default=None)
    according_to: Optional[AccordingToEnum]
    brief: Optional[uuid.UUID] = Field(default=None)
    brief__details: Optional[object] = Field(default={})


    @validator('according_to')
    def validate_according_to(cls, according_to: Optional[AccordingToEnum]):
        return according_to

    class Config:
        orm_mode = True


class UpdateBrief_Business(BaseModel):
    key: Optional[str] = Field(default=None)
    value: Optional[int] = Field(default=None)
    according_to: Optional[AccordingToEnum]
    brief: Optional[uuid.UUID] = Field(default=None)


    @validator('according_to')
    def validate_according_to(cls, according_to: Optional[AccordingToEnum]):
        if False or '__' in according_to or according_to in ['id']:
            raise ValueError(f"field <according_to> is not allowed")
        return according_to

    class Config:
        orm_mode = True


class ReadBrief_Businesses(BaseModel):
    data: list[Optional[ReadBrief_Business]]
    next_page: Union[str, int]
    page_size: int