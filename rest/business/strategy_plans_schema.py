
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
# select enums
class PostFormatEnum(str, enum.Enum):
    video = "video"
    real = "real"
    story = "story"
    post = "post"
    design = "design"
    carousel = "carousel"
# select enums
class ContentTypeEnum(str, enum.Enum):
    awareness = "awareness"
    branding = "branding"
    sales = "sales"
    engagement = "engagement"
    informative = "informative"


class CreateStrategy_Plan(BaseModel):
    id: Optional[uuid.UUID]
    platform: PlatformEnum
    post_format: PostFormatEnum
    content_type: ContentTypeEnum
    publish_day: Optional[str] = Field(default=None)
    publish_time: Optional[str] = Field(default=None)
    num_of_posts: Optional[int] = Field(default=None)
    content_requested: Optional[bool] = Field(default=False)
    ad_requested: Optional[bool] = Field(default=False)
    strategy: uuid.UUID

    @validator('platform')
    def validate_platform(cls, platform: PlatformEnum):
        if False or False or False:
            raise ValueError(f"field <platform> is not allowed")
        return platform
    @validator('post_format')
    def validate_post_format(cls, post_format: PostFormatEnum):
        if False or False or False:
            raise ValueError(f"field <post_format> is not allowed")
        return post_format
    @validator('content_type')
    def validate_content_type(cls, content_type: ContentTypeEnum):
        if False or False or False:
            raise ValueError(f"field <content_type> is not allowed")
        return content_type
    @validator('strategy')
    def validate_strategy(cls, strategy: uuid.UUID):
        if False or False or False:
            raise ValueError(f"field <strategy> is not allowed")
        return strategy

class ReadStrategy_Plan(BaseModel):
    id: uuid.UUID
    created_on: datetime.datetime
    updated_on: datetime.datetime
    created_by: Optional[uuid.UUID] = Field(default=None)
    updated_by: Optional[uuid.UUID] = Field(default=None)
    platform: PlatformEnum
    post_format: PostFormatEnum
    content_type: ContentTypeEnum
    publish_day: Optional[str] = Field(default=None)
    publish_time: Optional[str] = Field(default=None)
    num_of_posts: Optional[int] = Field(default=None)
    content_requested: Optional[bool] = Field(default=False)
    ad_requested: Optional[bool] = Field(default=False)
    strategy: Optional[uuid.UUID] = Field(default=None)
    strategy__details: Optional[object] = Field(default={})
    strategy_contents: Optional[list[object]] = Field(default=[{}])
    ads: Optional[list[object]] = Field(default=[{}])


    @validator('platform')
    def validate_platform(cls, platform: PlatformEnum):
        return platform

    @validator('post_format')
    def validate_post_format(cls, post_format: PostFormatEnum):
        return post_format

    @validator('content_type')
    def validate_content_type(cls, content_type: ContentTypeEnum):
        return content_type

    class Config:
        orm_mode = True


class UpdateStrategy_Plan(BaseModel):
    platform: Optional[PlatformEnum]
    post_format: Optional[PostFormatEnum]
    content_type: Optional[ContentTypeEnum]
    publish_day: Optional[str] = Field(default=None)
    publish_time: Optional[str] = Field(default=None)
    num_of_posts: Optional[int] = Field(default=None)
    content_requested: Optional[bool] = Field(default=False)
    ad_requested: Optional[bool] = Field(default=False)
    strategy: Optional[uuid.UUID] = Field(default=None)


    @validator('platform')
    def validate_platform(cls, platform: PlatformEnum):
        if False or '__' in platform or platform in ['id']:
            raise ValueError(f"field <platform> is not allowed")
        return platform

    @validator('post_format')
    def validate_post_format(cls, post_format: PostFormatEnum):
        if False or '__' in post_format or post_format in ['id']:
            raise ValueError(f"field <post_format> is not allowed")
        return post_format

    @validator('content_type')
    def validate_content_type(cls, content_type: ContentTypeEnum):
        if False or '__' in content_type or content_type in ['id']:
            raise ValueError(f"field <content_type> is not allowed")
        return content_type

    class Config:
        orm_mode = True


class ReadStrategy_Plans(BaseModel):
    data: list[Optional[ReadStrategy_Plan]]
    next_page: Union[str, int]
    page_size: int