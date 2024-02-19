
from typing import Optional, Union
from typing import Union
import uuid
import enum
import datetime

from pydantic import BaseModel, validator, EmailStr, Field
from core.encryptStr import EncryptStr




class CreateFile_Asset(BaseModel):
    id: Optional[uuid.UUID]
    file_name: str
    asset: uuid.UUID
    file_size: Optional[int] = Field(default=None)
    favorite: Optional[bool] = Field(default=False)
    deleted: Optional[bool] = Field(default=False)
    extension: Optional[str] = Field(default=None)
    open_time: Optional[datetime.date] = Field(default=None)
    customer: uuid.UUID
    folder: Optional[uuid.UUID] = Field(default=None)

    @validator('customer')
    def validate_customer(cls, customer: uuid.UUID):
        if False or False or False:
            raise ValueError(f"field <customer> is not allowed")
        return customer
    @validator('folder')
    def validate_folder(cls, folder: Optional[uuid.UUID] = Field(default=None)):
        if False or False or False:
            raise ValueError(f"field <folder> is not allowed")
        return folder

class ReadFile_Asset(BaseModel):
    id: uuid.UUID
    created_on: datetime.datetime
    updated_on: datetime.datetime
    created_by: Optional[uuid.UUID] = Field(default=None)
    updated_by: Optional[uuid.UUID] = Field(default=None)
    file_name: str
    asset: uuid.UUID
    file_size: Optional[int] = Field(default=None)
    favorite: Optional[bool] = Field(default=False)
    deleted: Optional[bool] = Field(default=False)
    extension: Optional[str] = Field(default=None)
    open_time: Optional[datetime.date] = Field(default=None)
    customer: Optional[uuid.UUID] = Field(default=None)
    customer__details: Optional[object] = Field(default={})
    folder: Optional[uuid.UUID] = Field(default=None)
    folder__details: Optional[object] = Field(default={})


    class Config:
        orm_mode = True


class UpdateFile_Asset(BaseModel):
    file_name: Optional[str] = Field(default=None)
    asset: Optional[uuid.UUID] = Field(default=None)
    file_size: Optional[int] = Field(default=None)
    favorite: Optional[bool] = Field(default=False)
    deleted: Optional[bool] = Field(default=False)
    extension: Optional[str] = Field(default=None)
    open_time: Optional[datetime.date] = Field(default=None)
    customer: Optional[uuid.UUID] = Field(default=None)
    folder: Optional[uuid.UUID] = Field(default=None)


    class Config:
        orm_mode = True


class ReadFile_Assets(BaseModel):
    data: list[Optional[ReadFile_Asset]]
    next_page: Union[str, int]
    page_size: int