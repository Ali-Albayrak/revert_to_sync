
from typing import Optional, Union
from typing import Union
import uuid
import enum
import datetime

from pydantic import BaseModel, validator, EmailStr, Field
from core.encryptStr import EncryptStr


# select enums
class AccountTypeEnum(str, enum.Enum):
    individual = "individual"
    multi = "multi"
# select enums
class StageEnum(str, enum.Enum):
    analysis = "analysis"
    strategy = "strategy"
# select enums
class IndicationEnum(str, enum.Enum):
    approved = "approved"
    draft = "draft"


class CreateCustomer(BaseModel):
    id: Optional[uuid.UUID]
    email: Optional[str] = Field(default=None)
    username: Optional[str] = Field(default=None)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    full_name: Optional[str] = Field(default=None)
    phone: Optional[str] = Field(default=None)
    profile_picture: Optional[uuid.UUID] = Field(default=None)
    addresses: Optional[dict] = Field(default={})
    account_manager: Optional[str] = Field(default=None)
    industry: Optional[str] = Field(default=None)
    sub_industry: Optional[str] = Field(default=None)
    brand_name: Optional[str] = Field(default=None)
    business_number: Optional[str] = Field(default=None)
    personal_number: Optional[str] = Field(default=None)
    account_type: Optional[AccountTypeEnum]
    completion_percentage: Optional[int] = Field(default=None)
    stage: Optional[StageEnum]
    indication: Optional[IndicationEnum]
    user: Optional[uuid.UUID] = Field(default=None)

    @validator('account_type')
    def validate_account_type(cls, account_type: Optional[AccountTypeEnum]):
        if False or False or False:
            raise ValueError(f"field <account_type> is not allowed")
        return account_type
    @validator('stage')
    def validate_stage(cls, stage: Optional[StageEnum]):
        if False or False or False:
            raise ValueError(f"field <stage> is not allowed")
        return stage
    @validator('indication')
    def validate_indication(cls, indication: Optional[IndicationEnum]):
        if False or False or False:
            raise ValueError(f"field <indication> is not allowed")
        return indication
    @validator('user')
    def validate_user(cls, user: Optional[uuid.UUID] = Field(default=None)):
        if False or False or False:
            raise ValueError(f"field <user> is not allowed")
        return user

class ReadCustomer(BaseModel):
    id: uuid.UUID
    created_on: datetime.datetime
    updated_on: datetime.datetime
    created_by: Optional[uuid.UUID] = Field(default=None)
    updated_by: Optional[uuid.UUID] = Field(default=None)
    email: Optional[str] = Field(default=None)
    username: Optional[str] = Field(default=None)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    full_name: Optional[str] = Field(default=None)
    phone: Optional[str] = Field(default=None)
    profile_picture: Optional[uuid.UUID] = Field(default=None)
    addresses: Optional[dict] = Field(default={})
    account_manager: Optional[str] = Field(default=None)
    industry: Optional[str] = Field(default=None)
    sub_industry: Optional[str] = Field(default=None)
    brand_name: Optional[str] = Field(default=None)
    business_number: Optional[str] = Field(default=None)
    personal_number: Optional[str] = Field(default=None)
    account_type: Optional[AccountTypeEnum]
    completion_percentage: Optional[int] = Field(default=None)
    stage: Optional[StageEnum]
    indication: Optional[IndicationEnum]
    briefs: Optional[list[object]] = Field(default=[{}])
    strategies: Optional[list[object]] = Field(default=[{}])
    appointments: Optional[list[object]] = Field(default=[{}])
    file_assets: Optional[list[object]] = Field(default=[{}])
    folders: Optional[list[object]] = Field(default=[{}])
    designs: Optional[list[object]] = Field(default=[{}])
    user: Optional[uuid.UUID] = Field(default=None)


    @validator('account_type')
    def validate_account_type(cls, account_type: Optional[AccountTypeEnum]):
        return account_type

    @validator('stage')
    def validate_stage(cls, stage: Optional[StageEnum]):
        return stage

    @validator('indication')
    def validate_indication(cls, indication: Optional[IndicationEnum]):
        return indication

    class Config:
        orm_mode = True


class UpdateCustomer(BaseModel):
    email: Optional[str] = Field(default=None)
    username: Optional[str] = Field(default=None)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    full_name: Optional[str] = Field(default=None)
    phone: Optional[str] = Field(default=None)
    profile_picture: Optional[uuid.UUID] = Field(default=None)
    addresses: Optional[dict] = Field(default={})
    account_manager: Optional[str] = Field(default=None)
    industry: Optional[str] = Field(default=None)
    sub_industry: Optional[str] = Field(default=None)
    brand_name: Optional[str] = Field(default=None)
    business_number: Optional[str] = Field(default=None)
    personal_number: Optional[str] = Field(default=None)
    account_type: Optional[AccountTypeEnum]
    completion_percentage: Optional[int] = Field(default=None)
    stage: Optional[StageEnum]
    indication: Optional[IndicationEnum]
    user: Optional[uuid.UUID] = Field(default=None)


    @validator('account_type')
    def validate_account_type(cls, account_type: Optional[AccountTypeEnum]):
        if False or '__' in account_type or account_type in ['id']:
            raise ValueError(f"field <account_type> is not allowed")
        return account_type

    @validator('stage')
    def validate_stage(cls, stage: Optional[StageEnum]):
        if False or '__' in stage or stage in ['id']:
            raise ValueError(f"field <stage> is not allowed")
        return stage

    @validator('indication')
    def validate_indication(cls, indication: Optional[IndicationEnum]):
        if False or '__' in indication or indication in ['id']:
            raise ValueError(f"field <indication> is not allowed")
        return indication

    class Config:
        orm_mode = True


class ReadCustomers(BaseModel):
    data: list[Optional[ReadCustomer]]
    next_page: Union[str, int]
    page_size: int