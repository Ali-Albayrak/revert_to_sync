
from typing import Optional, Union, List
from typing import Union
import uuid
import enum
import datetime

from pydantic import BaseModel, validator, EmailStr, Field
from core.encryptStr import EncryptStr


# select enums
class FacebookAudienceAgeEnum(str, enum.Enum):
    _14_20 = "_14_20"
    _20_30 = "_20_30"
    _40_50 = "_40_50"
# select enums
class FacebookAudienceGenderEnum(str, enum.Enum):
    male = "male"
    female = "female"
# select enums
class PlatformTypeEnum(str, enum.Enum):
    website = "website"
    facebook = "facebook"
    instagram = "instagram"
    twitter = "twitter"
    tiktok = "tiktok"
    google = "google"
    youtube = "youtube"


class CreateDeep_Analysis(BaseModel):
    id: Optional[uuid.UUID]
    website_visits: Optional[str] = Field(default=None)
    website_performance: Optional[str] = Field(default=None)
    website_technical_issues: Optional[str] = Field(default=None)
    website_traffic_sources: Optional[str] = Field(default=None)
    facebook_engagement_rate: Optional[str] = Field(default=None)
    facebook_followers: Optional[str] = Field(default=None)
    facebook_likes: Optional[str] = Field(default=None)
    facebook_comments: Optional[str] = Field(default=None)
    facebook_share: Optional[str] = Field(default=None)
    facebook_monthly_posts: Optional[str] = Field(default=None)
    facebook_type_of_content: Optional[List[str]]
    facebook_interests: Optional[str] = Field(default=None)
    facebook_achieved_platfrms_in_future: Optional[List[str]]
    facebook_achieved_platfrms_in_past: Optional[List[str]]
    facebook_tranding_hashtags: Optional[List[str]]
    facebook_successful_key_words: Optional[List[str]]
    facebook_tone_of_voice: Optional[List[str]]
    facebook_audience_age: Optional[FacebookAudienceAgeEnum]
    facebook_audience_gender: Optional[FacebookAudienceGenderEnum]
    facebook_best_performing_post: Optional[str] = Field(default=None)
    facebook_ads_revenue: Optional[str] = Field(default=None)
    instagram_followes: Optional[str] = Field(default=None)
    twitter_followes: Optional[str] = Field(default=None)
    tiktok_followes: Optional[str] = Field(default=None)
    google_seo: Optional[str] = Field(default=None)
    youtube_followes: Optional[str] = Field(default=None)
    platform_type: PlatformTypeEnum
    brief_platform: uuid.UUID

    @validator('facebook_type_of_content')
    def validate_facebook_type_of_content(cls, facebook_type_of_content: Optional[List[str]]):
        if False or False or False:
            raise ValueError(f"field <facebook_type_of_content> is not allowed")
        return facebook_type_of_content
    @validator('facebook_achieved_platfrms_in_future')
    def validate_facebook_achieved_platfrms_in_future(cls, facebook_achieved_platfrms_in_future: Optional[List[str]]):
        if False or False or False:
            raise ValueError(f"field <facebook_achieved_platfrms_in_future> is not allowed")
        return facebook_achieved_platfrms_in_future
    @validator('facebook_achieved_platfrms_in_past')
    def validate_facebook_achieved_platfrms_in_past(cls, facebook_achieved_platfrms_in_past: Optional[List[str]]):
        if False or False or False:
            raise ValueError(f"field <facebook_achieved_platfrms_in_past> is not allowed")
        return facebook_achieved_platfrms_in_past
    @validator('facebook_tranding_hashtags')
    def validate_facebook_tranding_hashtags(cls, facebook_tranding_hashtags: Optional[List[str]]):
        if False or False or False:
            raise ValueError(f"field <facebook_tranding_hashtags> is not allowed")
        return facebook_tranding_hashtags
    @validator('facebook_successful_key_words')
    def validate_facebook_successful_key_words(cls, facebook_successful_key_words: Optional[List[str]]):
        if False or False or False:
            raise ValueError(f"field <facebook_successful_key_words> is not allowed")
        return facebook_successful_key_words
    @validator('facebook_tone_of_voice')
    def validate_facebook_tone_of_voice(cls, facebook_tone_of_voice: Optional[List[str]]):
        if False or False or False:
            raise ValueError(f"field <facebook_tone_of_voice> is not allowed")
        return facebook_tone_of_voice
    @validator('facebook_audience_age')
    def validate_facebook_audience_age(cls, facebook_audience_age: Optional[FacebookAudienceAgeEnum]):
        if False or False or False:
            raise ValueError(f"field <facebook_audience_age> is not allowed")
        return facebook_audience_age
    @validator('facebook_audience_gender')
    def validate_facebook_audience_gender(cls, facebook_audience_gender: Optional[FacebookAudienceGenderEnum]):
        if False or False or False:
            raise ValueError(f"field <facebook_audience_gender> is not allowed")
        return facebook_audience_gender
    @validator('platform_type')
    def validate_platform_type(cls, platform_type: PlatformTypeEnum):
        if False or False or False:
            raise ValueError(f"field <platform_type> is not allowed")
        return platform_type
    @validator('brief_platform')
    def validate_brief_platform(cls, brief_platform: uuid.UUID):
        if False or False or False:
            raise ValueError(f"field <brief_platform> is not allowed")
        return brief_platform

class ReadDeep_Analysis(BaseModel):
    id: uuid.UUID
    created_on: datetime.datetime
    updated_on: datetime.datetime
    created_by: Optional[uuid.UUID] = Field(default=None)
    updated_by: Optional[uuid.UUID] = Field(default=None)
    website_visits: Optional[str] = Field(default=None)
    website_performance: Optional[str] = Field(default=None)
    website_technical_issues: Optional[str] = Field(default=None)
    website_traffic_sources: Optional[str] = Field(default=None)
    facebook_engagement_rate: Optional[str] = Field(default=None)
    facebook_followers: Optional[str] = Field(default=None)
    facebook_likes: Optional[str] = Field(default=None)
    facebook_comments: Optional[str] = Field(default=None)
    facebook_share: Optional[str] = Field(default=None)
    facebook_monthly_posts: Optional[str] = Field(default=None)
    facebook_type_of_content: Optional[List[str]]
    facebook_interests: Optional[str] = Field(default=None)
    facebook_achieved_platfrms_in_future: Optional[List[str]]
    facebook_achieved_platfrms_in_past: Optional[List[str]]
    facebook_tranding_hashtags: Optional[List[str]]
    facebook_successful_key_words: Optional[List[str]]
    facebook_tone_of_voice: Optional[List[str]]
    facebook_audience_age: Optional[FacebookAudienceAgeEnum]
    facebook_audience_gender: Optional[FacebookAudienceGenderEnum]
    facebook_best_performing_post: Optional[str] = Field(default=None)
    facebook_ads_revenue: Optional[str] = Field(default=None)
    instagram_followes: Optional[str] = Field(default=None)
    twitter_followes: Optional[str] = Field(default=None)
    tiktok_followes: Optional[str] = Field(default=None)
    google_seo: Optional[str] = Field(default=None)
    youtube_followes: Optional[str] = Field(default=None)
    platform_type: PlatformTypeEnum
    brief_platform: Optional[uuid.UUID] = Field(default=None)
    brief_platform__details: Optional[object] = Field(default={})


    @validator('facebook_type_of_content')
    def validate_facebook_type_of_content(cls, facebook_type_of_content: Optional[List[str]]):
        return facebook_type_of_content

    @validator('facebook_achieved_platfrms_in_future')
    def validate_facebook_achieved_platfrms_in_future(cls, facebook_achieved_platfrms_in_future: Optional[List[str]]):
        return facebook_achieved_platfrms_in_future

    @validator('facebook_achieved_platfrms_in_past')
    def validate_facebook_achieved_platfrms_in_past(cls, facebook_achieved_platfrms_in_past: Optional[List[str]]):
        return facebook_achieved_platfrms_in_past

    @validator('facebook_tranding_hashtags')
    def validate_facebook_tranding_hashtags(cls, facebook_tranding_hashtags: Optional[List[str]]):
        return facebook_tranding_hashtags

    @validator('facebook_successful_key_words')
    def validate_facebook_successful_key_words(cls, facebook_successful_key_words: Optional[List[str]]):
        return facebook_successful_key_words

    @validator('facebook_tone_of_voice')
    def validate_facebook_tone_of_voice(cls, facebook_tone_of_voice: Optional[List[str]]):
        return facebook_tone_of_voice

    @validator('facebook_audience_age')
    def validate_facebook_audience_age(cls, facebook_audience_age: Optional[FacebookAudienceAgeEnum]):
        return facebook_audience_age

    @validator('facebook_audience_gender')
    def validate_facebook_audience_gender(cls, facebook_audience_gender: Optional[FacebookAudienceGenderEnum]):
        return facebook_audience_gender

    @validator('platform_type')
    def validate_platform_type(cls, platform_type: PlatformTypeEnum):
        return platform_type

    class Config:
        orm_mode = True


class UpdateDeep_Analysis(BaseModel):
    website_visits: Optional[str] = Field(default=None)
    website_performance: Optional[str] = Field(default=None)
    website_technical_issues: Optional[str] = Field(default=None)
    website_traffic_sources: Optional[str] = Field(default=None)
    facebook_engagement_rate: Optional[str] = Field(default=None)
    facebook_followers: Optional[str] = Field(default=None)
    facebook_likes: Optional[str] = Field(default=None)
    facebook_comments: Optional[str] = Field(default=None)
    facebook_share: Optional[str] = Field(default=None)
    facebook_monthly_posts: Optional[str] = Field(default=None)
    facebook_type_of_content: Optional[List[str]]
    facebook_interests: Optional[str] = Field(default=None)
    facebook_achieved_platfrms_in_future: Optional[List[str]]
    facebook_achieved_platfrms_in_past: Optional[List[str]]
    facebook_tranding_hashtags: Optional[List[str]]
    facebook_successful_key_words: Optional[List[str]]
    facebook_tone_of_voice: Optional[List[str]]
    facebook_audience_age: Optional[FacebookAudienceAgeEnum]
    facebook_audience_gender: Optional[FacebookAudienceGenderEnum]
    facebook_best_performing_post: Optional[str] = Field(default=None)
    facebook_ads_revenue: Optional[str] = Field(default=None)
    instagram_followes: Optional[str] = Field(default=None)
    twitter_followes: Optional[str] = Field(default=None)
    tiktok_followes: Optional[str] = Field(default=None)
    google_seo: Optional[str] = Field(default=None)
    youtube_followes: Optional[str] = Field(default=None)
    platform_type: Optional[PlatformTypeEnum]
    brief_platform: Optional[uuid.UUID] = Field(default=None)


    @validator('facebook_type_of_content')
    def validate_facebook_type_of_content(cls, facebook_type_of_content: Optional[List[str]]):
        if False or '__' in facebook_type_of_content or facebook_type_of_content in ['id']:
            raise ValueError(f"field <facebook_type_of_content> is not allowed")
        return facebook_type_of_content

    @validator('facebook_achieved_platfrms_in_future')
    def validate_facebook_achieved_platfrms_in_future(cls, facebook_achieved_platfrms_in_future: Optional[List[str]]):
        if False or '__' in facebook_achieved_platfrms_in_future or facebook_achieved_platfrms_in_future in ['id']:
            raise ValueError(f"field <facebook_achieved_platfrms_in_future> is not allowed")
        return facebook_achieved_platfrms_in_future

    @validator('facebook_achieved_platfrms_in_past')
    def validate_facebook_achieved_platfrms_in_past(cls, facebook_achieved_platfrms_in_past: Optional[List[str]]):
        if False or '__' in facebook_achieved_platfrms_in_past or facebook_achieved_platfrms_in_past in ['id']:
            raise ValueError(f"field <facebook_achieved_platfrms_in_past> is not allowed")
        return facebook_achieved_platfrms_in_past

    @validator('facebook_tranding_hashtags')
    def validate_facebook_tranding_hashtags(cls, facebook_tranding_hashtags: Optional[List[str]]):
        if False or '__' in facebook_tranding_hashtags or facebook_tranding_hashtags in ['id']:
            raise ValueError(f"field <facebook_tranding_hashtags> is not allowed")
        return facebook_tranding_hashtags

    @validator('facebook_successful_key_words')
    def validate_facebook_successful_key_words(cls, facebook_successful_key_words: Optional[List[str]]):
        if False or '__' in facebook_successful_key_words or facebook_successful_key_words in ['id']:
            raise ValueError(f"field <facebook_successful_key_words> is not allowed")
        return facebook_successful_key_words

    @validator('facebook_tone_of_voice')
    def validate_facebook_tone_of_voice(cls, facebook_tone_of_voice: Optional[List[str]]):
        if False or '__' in facebook_tone_of_voice or facebook_tone_of_voice in ['id']:
            raise ValueError(f"field <facebook_tone_of_voice> is not allowed")
        return facebook_tone_of_voice

    @validator('facebook_audience_age')
    def validate_facebook_audience_age(cls, facebook_audience_age: Optional[FacebookAudienceAgeEnum]):
        if False or '__' in facebook_audience_age or facebook_audience_age in ['id']:
            raise ValueError(f"field <facebook_audience_age> is not allowed")
        return facebook_audience_age

    @validator('facebook_audience_gender')
    def validate_facebook_audience_gender(cls, facebook_audience_gender: Optional[FacebookAudienceGenderEnum]):
        if False or '__' in facebook_audience_gender or facebook_audience_gender in ['id']:
            raise ValueError(f"field <facebook_audience_gender> is not allowed")
        return facebook_audience_gender

    @validator('platform_type')
    def validate_platform_type(cls, platform_type: PlatformTypeEnum):
        if False or '__' in platform_type or platform_type in ['id']:
            raise ValueError(f"field <platform_type> is not allowed")
        return platform_type

    class Config:
        orm_mode = True


class ReadDeep_Analytics(BaseModel):
    data: list[Optional[ReadDeep_Analysis]]
    next_page: Union[str, int]
    page_size: int