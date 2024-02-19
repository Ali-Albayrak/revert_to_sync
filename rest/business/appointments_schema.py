
from typing import Optional, Union
from typing import Union
import uuid
import enum
import datetime

from pydantic import BaseModel, validator, EmailStr, Field
from core.encryptStr import EncryptStr




class CreateAppointment(BaseModel):
    id: Optional[uuid.UUID]
    customer: Optional[uuid.UUID] = Field(default=None)
    approval_status: Optional[str] = Field(default=None)
    account_manager: Optional[str] = Field(default=None)
    meeting_schedule: Optional[str] = Field(default=None)
    brief_last_update: Optional[datetime.date] = Field(default=None)

    @validator('customer')
    def validate_customer(cls, customer: Optional[uuid.UUID] = Field(default=None)):
        if False or False or False:
            raise ValueError(f"field <customer> is not allowed")
        return customer

class ReadAppointment(BaseModel):
    id: uuid.UUID
    created_on: datetime.datetime
    updated_on: datetime.datetime
    created_by: Optional[uuid.UUID] = Field(default=None)
    updated_by: Optional[uuid.UUID] = Field(default=None)
    customer: Optional[uuid.UUID] = Field(default=None)
    customer__details: Optional[object] = Field(default={})
    approval_status: Optional[str] = Field(default=None)
    account_manager: Optional[str] = Field(default=None)
    meeting_schedule: Optional[str] = Field(default=None)
    brief_last_update: Optional[datetime.date] = Field(default=None)


    class Config:
        orm_mode = True


class UpdateAppointment(BaseModel):
    customer: Optional[uuid.UUID] = Field(default=None)
    approval_status: Optional[str] = Field(default=None)
    account_manager: Optional[str] = Field(default=None)
    meeting_schedule: Optional[str] = Field(default=None)
    brief_last_update: Optional[datetime.date] = Field(default=None)


    class Config:
        orm_mode = True


class ReadAppointments(BaseModel):
    data: list[Optional[ReadAppointment]]
    next_page: Union[str, int]
    page_size: int