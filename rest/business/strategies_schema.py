
from typing import Optional, Union
from typing import Union
import uuid
import enum
import datetime

from pydantic import BaseModel, validator, EmailStr, Field
from core.encryptStr import EncryptStr


# select enums
class AdsBudgetEnum(str, enum.Enum):
    _100_300 = "_100_300"
    _300_600 = "_300_600"
    _600_1000 = "_600_1000"
    _1000_2000 = "_1000_2000"
    other = "other"


class CreateStrategy(BaseModel):
    id: Optional[uuid.UUID]
    customer: Optional[uuid.UUID] = Field(default=None)
    name: Optional[str] = Field(default=None)
    ads_budget: Optional[AdsBudgetEnum]
    custom_budget: Optional[str] = Field(default=None)
    budget_distribution: Optional[dict] = Field(default={})

    @validator('customer')
    def validate_customer(cls, customer: Optional[uuid.UUID] = Field(default=None)):
        if False or False or False:
            raise ValueError(f"field <customer> is not allowed")
        return customer
    @validator('ads_budget')
    def validate_ads_budget(cls, ads_budget: Optional[AdsBudgetEnum]):
        if False or False or False:
            raise ValueError(f"field <ads_budget> is not allowed")
        return ads_budget

class ReadStrategy(BaseModel):
    id: uuid.UUID
    created_on: datetime.datetime
    updated_on: datetime.datetime
    created_by: Optional[uuid.UUID] = Field(default=None)
    updated_by: Optional[uuid.UUID] = Field(default=None)
    customer: Optional[uuid.UUID] = Field(default=None)
    customer__details: Optional[object] = Field(default={})
    name: Optional[str] = Field(default=None)
    strategy_plans: Optional[list[object]] = Field(default=[{}])
    strategy_personas: Optional[list[object]] = Field(default=[{}])
    strategy_audiences: Optional[list[object]] = Field(default=[{}])
    strategy_objectives: Optional[list[object]] = Field(default=[{}])
    ads_budget: Optional[AdsBudgetEnum]
    custom_budget: Optional[str] = Field(default=None)
    budget_distribution: Optional[dict] = Field(default={})


    @validator('ads_budget')
    def validate_ads_budget(cls, ads_budget: Optional[AdsBudgetEnum]):
        return ads_budget

    class Config:
        orm_mode = True


class UpdateStrategy(BaseModel):
    customer: Optional[uuid.UUID] = Field(default=None)
    name: Optional[str] = Field(default=None)
    ads_budget: Optional[AdsBudgetEnum]
    custom_budget: Optional[str] = Field(default=None)
    budget_distribution: Optional[dict] = Field(default={})


    @validator('ads_budget')
    def validate_ads_budget(cls, ads_budget: Optional[AdsBudgetEnum]):
        if False or '__' in ads_budget or ads_budget in ['id']:
            raise ValueError(f"field <ads_budget> is not allowed")
        return ads_budget

    class Config:
        orm_mode = True


class ReadStrategies(BaseModel):
    data: list[Optional[ReadStrategy]]
    next_page: Union[str, int]
    page_size: int