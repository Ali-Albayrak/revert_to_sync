
from typing import Optional, Union
from typing import Union
import uuid
import enum
import datetime

from pydantic import BaseModel, validator, EmailStr, Field
from core.encryptStr import EncryptStr




class CreateAd(BaseModel):
    id: Optional[uuid.UUID]
    name: Optional[str] = Field(default=None)
    about: Optional[str] = Field(default=None)
    start_date: Optional[datetime.date] = Field(default=None)
    end_date: Optional[datetime.date] = Field(default=None)
    strategy_plan: Optional[uuid.UUID] = Field(default=None)

    @validator('strategy_plan')
    def validate_strategy_plan(cls, strategy_plan: Optional[uuid.UUID] = Field(default=None)):
        if False or False or False:
            raise ValueError(f"field <strategy_plan> is not allowed")
        return strategy_plan

class ReadAd(BaseModel):
    id: uuid.UUID
    created_on: datetime.datetime
    updated_on: datetime.datetime
    created_by: Optional[uuid.UUID] = Field(default=None)
    updated_by: Optional[uuid.UUID] = Field(default=None)
    name: Optional[str] = Field(default=None)
    about: Optional[str] = Field(default=None)
    start_date: Optional[datetime.date] = Field(default=None)
    end_date: Optional[datetime.date] = Field(default=None)
    strategy_plan: Optional[uuid.UUID] = Field(default=None)
    strategy_plan__details: Optional[object] = Field(default={})


    class Config:
        orm_mode = True


class UpdateAd(BaseModel):
    name: Optional[str] = Field(default=None)
    about: Optional[str] = Field(default=None)
    start_date: Optional[datetime.date] = Field(default=None)
    end_date: Optional[datetime.date] = Field(default=None)
    strategy_plan: Optional[uuid.UUID] = Field(default=None)


    class Config:
        orm_mode = True


class ReadAds(BaseModel):
    data: list[Optional[ReadAd]]
    next_page: Union[str, int]
    page_size: int