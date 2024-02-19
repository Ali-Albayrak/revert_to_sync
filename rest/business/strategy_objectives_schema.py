
from typing import Optional, Union
from typing import Union
import uuid
import enum
import datetime

from pydantic import BaseModel, validator, EmailStr, Field
from core.encryptStr import EncryptStr


# select enums
class ObjectivesEnum(str, enum.Enum):
    branding = "branding"
    brand_awareness = "brand_awareness"
    sales = "sales"
    engagement = "engagement"
# select enums
class PercentageEnum(str, enum.Enum):
    _10 = "_10"
    _20 = "_20"
    _30 = "_30"
    _40 = "_40"
    _50 = "_50"
    _60 = "_60"
    _70 = "_70"
    _80 = "_80"
    _90 = "_90"
    _100 = "_100"


class CreateStrategy_Objective(BaseModel):
    id: Optional[uuid.UUID]
    objectives: Optional[ObjectivesEnum]
    percentage: Optional[PercentageEnum]
    kpi_goals: Optional[dict] = Field(default={})
    strategy: uuid.UUID

    @validator('objectives')
    def validate_objectives(cls, objectives: Optional[ObjectivesEnum]):
        if False or False or False:
            raise ValueError(f"field <objectives> is not allowed")
        return objectives
    @validator('percentage')
    def validate_percentage(cls, percentage: Optional[PercentageEnum]):
        if False or False or False:
            raise ValueError(f"field <percentage> is not allowed")
        return percentage
    @validator('strategy')
    def validate_strategy(cls, strategy: uuid.UUID):
        if False or False or False:
            raise ValueError(f"field <strategy> is not allowed")
        return strategy

class ReadStrategy_Objective(BaseModel):
    id: uuid.UUID
    created_on: datetime.datetime
    updated_on: datetime.datetime
    created_by: Optional[uuid.UUID] = Field(default=None)
    updated_by: Optional[uuid.UUID] = Field(default=None)
    objectives: Optional[ObjectivesEnum]
    percentage: Optional[PercentageEnum]
    kpi_goals: Optional[dict] = Field(default={})
    strategy: Optional[uuid.UUID] = Field(default=None)
    strategy__details: Optional[object] = Field(default={})


    @validator('objectives')
    def validate_objectives(cls, objectives: Optional[ObjectivesEnum]):
        return objectives

    @validator('percentage')
    def validate_percentage(cls, percentage: Optional[PercentageEnum]):
        return percentage

    class Config:
        orm_mode = True


class UpdateStrategy_Objective(BaseModel):
    objectives: Optional[ObjectivesEnum]
    percentage: Optional[PercentageEnum]
    kpi_goals: Optional[dict] = Field(default={})
    strategy: Optional[uuid.UUID] = Field(default=None)


    @validator('objectives')
    def validate_objectives(cls, objectives: Optional[ObjectivesEnum]):
        if False or '__' in objectives or objectives in ['id']:
            raise ValueError(f"field <objectives> is not allowed")
        return objectives

    @validator('percentage')
    def validate_percentage(cls, percentage: Optional[PercentageEnum]):
        if False or '__' in percentage or percentage in ['id']:
            raise ValueError(f"field <percentage> is not allowed")
        return percentage

    class Config:
        orm_mode = True


class ReadStrategy_Objectives(BaseModel):
    data: list[Optional[ReadStrategy_Objective]]
    next_page: Union[str, int]
    page_size: int