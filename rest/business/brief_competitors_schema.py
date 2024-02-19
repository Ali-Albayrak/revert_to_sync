
from typing import Optional, Union
from typing import Union
import uuid
import enum
import datetime

from pydantic import BaseModel, validator, EmailStr, Field
from core.encryptStr import EncryptStr


# select enums
class PlatformEnum(str, enum.Enum):
    website = "website"
    facebook = "facebook"
    instagram = "instagram"
    twitter = "twitter"
    tiktok = "tiktok"
    google = "google"
    youtube = "youtube"


class CreateBrief_Competitor(BaseModel):
    id: Optional[uuid.UUID]
    platform: Optional[list[PlatformEnum]]
    link: Optional[str] = Field(default=None)
    brief: uuid.UUID

    @validator('platform')
    def validate_platform(cls, platform: Optional[list[PlatformEnum]]):
        if False or False or False:
            raise ValueError(f"field <platform> is not allowed")
        return platform
    @validator('brief')
    def validate_brief(cls, brief: uuid.UUID):
        if False or False or False:
            raise ValueError(f"field <brief> is not allowed")
        return brief

class ReadBrief_Competitor(BaseModel):
    id: uuid.UUID
    created_on: datetime.datetime
    updated_on: datetime.datetime
    created_by: Optional[uuid.UUID] = Field(default=None)
    updated_by: Optional[uuid.UUID] = Field(default=None)
    platform: Optional[list[PlatformEnum]]
    link: Optional[str] = Field(default=None)
    brief: Optional[uuid.UUID] = Field(default=None)
    brief__details: Optional[object] = Field(default={})


    @validator('platform')
    def validate_platform(cls, platform: Optional[list[PlatformEnum]]):
        return platform

    class Config:
        orm_mode = True


class UpdateBrief_Competitor(BaseModel):
    platform: Optional[list[PlatformEnum]]
    link: Optional[str] = Field(default=None)
    brief: Optional[uuid.UUID] = Field(default=None)


    @validator('platform')
    def validate_platform(cls, platform: Optional[list[PlatformEnum]]):
        if False or '__' in platform or platform in ['id']:
            raise ValueError(f"field <platform> is not allowed")
        return platform

    class Config:
        orm_mode = True


class ReadBrief_Competitors(BaseModel):
    data: list[Optional[ReadBrief_Competitor]]
    next_page: Union[str, int]
    page_size: int