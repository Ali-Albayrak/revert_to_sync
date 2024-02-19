
from typing import Optional, Union, List
from typing import Union
import uuid
import enum
import datetime

from pydantic import BaseModel, validator, EmailStr, Field
from core.encryptStr import EncryptStr


# select enums
class GenderEnum(str, enum.Enum):
    male = "male"
    female = "female"
    both = "both"
# select enums
class AgeGroupEnum(str, enum.Enum):
    under_18 = "under_18"
    _18_24 = "_18_24"
    _25_34 = "_25_34"
    _35_44 = "_35_44"
    _45_54 = "_45_54"
    _55_64 = "_55_64"
    _65_and_older = "_65_and_older"
# select enums
class TheClassEnum(str, enum.Enum):
    a = "a"
    b = "b"
    c = "c"


class CreateBrief_Audience(BaseModel):
    id: Optional[uuid.UUID]
    interests: Optional[str] = Field(default=None)
    journey: Optional[str] = Field(default=None)
    keywords: Optional[str] = Field(default=None)
    geo_audience: Optional[List[str]]
    gender: Optional[GenderEnum]
    age_group: Optional[list[AgeGroupEnum]]
    the_class: Optional[list[TheClassEnum]]
    sales_channel: Optional[str] = Field(default=None)
    brief: uuid.UUID

    @validator('geo_audience')
    def validate_geo_audience(cls, geo_audience: Optional[List[str]]):
        if False or False or False:
            raise ValueError(f"field <geo_audience> is not allowed")
        return geo_audience
    @validator('gender')
    def validate_gender(cls, gender: Optional[GenderEnum]):
        if False or False or False:
            raise ValueError(f"field <gender> is not allowed")
        return gender
    @validator('age_group')
    def validate_age_group(cls, age_group: Optional[list[AgeGroupEnum]]):
        if False or False or False:
            raise ValueError(f"field <age_group> is not allowed")
        return age_group
    @validator('the_class')
    def validate_the_class(cls, the_class: Optional[list[TheClassEnum]]):
        if False or False or False:
            raise ValueError(f"field <the_class> is not allowed")
        return the_class
    @validator('brief')
    def validate_brief(cls, brief: uuid.UUID):
        if False or False or False:
            raise ValueError(f"field <brief> is not allowed")
        return brief

class ReadBrief_Audience(BaseModel):
    id: uuid.UUID
    created_on: datetime.datetime
    updated_on: datetime.datetime
    created_by: Optional[uuid.UUID] = Field(default=None)
    updated_by: Optional[uuid.UUID] = Field(default=None)
    interests: Optional[str] = Field(default=None)
    journey: Optional[str] = Field(default=None)
    keywords: Optional[str] = Field(default=None)
    geo_audience: Optional[List[str]]
    gender: Optional[GenderEnum]
    age_group: Optional[list[AgeGroupEnum]]
    the_class: Optional[list[TheClassEnum]]
    sales_channel: Optional[str] = Field(default=None)
    brief: Optional[uuid.UUID] = Field(default=None)
    brief__details: Optional[object] = Field(default={})


    @validator('geo_audience')
    def validate_geo_audience(cls, geo_audience: Optional[List[str]]):
        return geo_audience

    @validator('gender')
    def validate_gender(cls, gender: Optional[GenderEnum]):
        return gender

    @validator('age_group')
    def validate_age_group(cls, age_group: Optional[list[AgeGroupEnum]]):
        return age_group

    @validator('the_class')
    def validate_the_class(cls, the_class: Optional[list[TheClassEnum]]):
        return the_class

    class Config:
        orm_mode = True


class UpdateBrief_Audience(BaseModel):
    interests: Optional[str] = Field(default=None)
    journey: Optional[str] = Field(default=None)
    keywords: Optional[str] = Field(default=None)
    geo_audience: Optional[List[str]]
    gender: Optional[GenderEnum]
    age_group: Optional[list[AgeGroupEnum]]
    the_class: Optional[list[TheClassEnum]]
    sales_channel: Optional[str] = Field(default=None)
    brief: Optional[uuid.UUID] = Field(default=None)


    @validator('geo_audience')
    def validate_geo_audience(cls, geo_audience: Optional[List[str]]):
        if False or '__' in geo_audience or geo_audience in ['id']:
            raise ValueError(f"field <geo_audience> is not allowed")
        return geo_audience

    @validator('gender')
    def validate_gender(cls, gender: Optional[GenderEnum]):
        if False or '__' in gender or gender in ['id']:
            raise ValueError(f"field <gender> is not allowed")
        return gender

    @validator('age_group')
    def validate_age_group(cls, age_group: Optional[list[AgeGroupEnum]]):
        if False or '__' in age_group or age_group in ['id']:
            raise ValueError(f"field <age_group> is not allowed")
        return age_group

    @validator('the_class')
    def validate_the_class(cls, the_class: Optional[list[TheClassEnum]]):
        if False or '__' in the_class or the_class in ['id']:
            raise ValueError(f"field <the_class> is not allowed")
        return the_class

    class Config:
        orm_mode = True


class ReadBrief_Audiences(BaseModel):
    data: list[Optional[ReadBrief_Audience]]
    next_page: Union[str, int]
    page_size: int