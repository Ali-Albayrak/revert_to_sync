
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


class CreateBrief_Objective(BaseModel):
    id: Optional[uuid.UUID]
    name: Optional[str] = Field(default=None)
    objectives: Optional[ObjectivesEnum]
    kpi_goals: Optional[dict] = Field(default={})
    brief: uuid.UUID

    @validator('objectives')
    def validate_objectives(cls, objectives: Optional[ObjectivesEnum]):
        if False or False or False:
            raise ValueError(f"field <objectives> is not allowed")
        return objectives
    @validator('brief')
    def validate_brief(cls, brief: uuid.UUID):
        if False or False or False:
            raise ValueError(f"field <brief> is not allowed")
        return brief

class ReadBrief_Objective(BaseModel):
    id: uuid.UUID
    created_on: datetime.datetime
    updated_on: datetime.datetime
    created_by: Optional[uuid.UUID] = Field(default=None)
    updated_by: Optional[uuid.UUID] = Field(default=None)
    name: Optional[str] = Field(default=None)
    objectives: Optional[ObjectivesEnum]
    kpi_goals: Optional[dict] = Field(default={})
    brief: Optional[uuid.UUID] = Field(default=None)
    brief__details: Optional[object] = Field(default={})


    @validator('objectives')
    def validate_objectives(cls, objectives: Optional[ObjectivesEnum]):
        return objectives

    class Config:
        orm_mode = True


class UpdateBrief_Objective(BaseModel):
    name: Optional[str] = Field(default=None)
    objectives: Optional[ObjectivesEnum]
    kpi_goals: Optional[dict] = Field(default={})
    brief: Optional[uuid.UUID] = Field(default=None)


    @validator('objectives')
    def validate_objectives(cls, objectives: Optional[ObjectivesEnum]):
        if False or '__' in objectives or objectives in ['id']:
            raise ValueError(f"field <objectives> is not allowed")
        return objectives

    class Config:
        orm_mode = True


class ReadBrief_Objectives(BaseModel):
    data: list[Optional[ReadBrief_Objective]]
    next_page: Union[str, int]
    page_size: int