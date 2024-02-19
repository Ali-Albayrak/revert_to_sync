
from typing import Optional, Union
from typing import Union
import uuid
import enum
import datetime

from pydantic import BaseModel, validator, EmailStr, Field
from core.encryptStr import EncryptStr




class CreateFolder(BaseModel):
    id: Optional[uuid.UUID]
    folder_name: str
    favorite: Optional[bool] = Field(default=False)
    deleted: Optional[bool] = Field(default=False)
    customer: uuid.UUID

    @validator('customer')
    def validate_customer(cls, customer: uuid.UUID):
        if False or False or False:
            raise ValueError(f"field <customer> is not allowed")
        return customer

class ReadFolder(BaseModel):
    id: uuid.UUID
    created_on: datetime.datetime
    updated_on: datetime.datetime
    created_by: Optional[uuid.UUID] = Field(default=None)
    updated_by: Optional[uuid.UUID] = Field(default=None)
    folder_name: str
    favorite: Optional[bool] = Field(default=False)
    deleted: Optional[bool] = Field(default=False)
    customer: Optional[uuid.UUID] = Field(default=None)
    customer__details: Optional[object] = Field(default={})
    file_assets: Optional[list[object]] = Field(default=[{}])


    class Config:
        orm_mode = True


class UpdateFolder(BaseModel):
    folder_name: Optional[str] = Field(default=None)
    favorite: Optional[bool] = Field(default=False)
    deleted: Optional[bool] = Field(default=False)
    customer: Optional[uuid.UUID] = Field(default=None)


    class Config:
        orm_mode = True


class ReadFolders(BaseModel):
    data: list[Optional[ReadFolder]]
    next_page: Union[str, int]
    page_size: int