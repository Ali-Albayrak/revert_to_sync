import os
import importlib
from core.logger import log




import enum
from sqlalchemy import DATETIME, String, ForeignKey
from sqlalchemy import ARRAY, String, ForeignKey, Column, Enum, Text
from sqlalchemy.orm import relationship
from core.base_model import BaseModel
from core.manager import Manager
from fastapi import HTTPException
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import select



# select enums
class FacebookAudienceAgeEnum(str, enum.Enum):
    _14_20 = "_14_20"
    _20_30 = "_20_30"
    _40_50 = "_40_50"
class FacebookAudienceGenderEnum(str, enum.Enum):
    male = "male"
    female = "female"
class PlatformTypeEnum(str, enum.Enum):
    website = "website"
    facebook = "facebook"
    instagram = "instagram"
    twitter = "twitter"
    tiktok = "tiktok"
    google = "google"
    youtube = "youtube"


class Deep_AnalysisModel(BaseModel):
    __tablename__ = 'deep_analytics'
    __table_args__ = {'schema': os.environ.get('DEFAULT_SCHEMA', 'public')}


    website_visits = Column(Text, nullable=True, default=None)

    website_performance = Column(Text, nullable=True, default=None)

    website_technical_issues = Column(Text, nullable=True, default=None)

    website_traffic_sources = Column(Text, nullable=True, default=None)

    facebook_engagement_rate = Column(Text, nullable=True, default=None)

    facebook_followers = Column(Text, nullable=True, default=None)

    facebook_likes = Column(Text, nullable=True, default=None)

    facebook_comments = Column(Text, nullable=True, default=None)

    facebook_share = Column(Text, nullable=True, default=None)

    facebook_monthly_posts = Column(Text, nullable=True, default=None)

    facebook_type_of_content = Column(ARRAY(Text), nullable=True, default=None)

    facebook_interests = Column(Text, nullable=True, default=None)

    facebook_achieved_platfrms_in_future = Column(ARRAY(Text), nullable=True, default=None)

    facebook_achieved_platfrms_in_past = Column(ARRAY(Text), nullable=True, default=None)

    facebook_tranding_hashtags = Column(ARRAY(Text), nullable=True, default=None)

    facebook_successful_key_words = Column(ARRAY(Text), nullable=True, default=None)

    facebook_tone_of_voice = Column(ARRAY(Text), nullable=True, default=None)

    facebook_audience_age = Column(Enum(FacebookAudienceAgeEnum), nullable=True, default=None)

    facebook_audience_gender = Column(Enum(FacebookAudienceGenderEnum), nullable=True, default=None)

    facebook_best_performing_post = Column(Text, nullable=True, default=None)

    facebook_ads_revenue = Column(Text, nullable=True, default=None)

    instagram_followes = Column(Text, nullable=True, default=None)

    twitter_followes = Column(Text, nullable=True, default=None)

    tiktok_followes = Column(Text, nullable=True, default=None)

    google_seo = Column(Text, nullable=True, default=None)

    youtube_followes = Column(Text, nullable=True, default=None)

    platform_type = Column(Enum(PlatformTypeEnum), nullable=False, default=None)


    brief_platform = Column(UUID(as_uuid=True), ForeignKey(os.environ.get('DEFAULT_SCHEMA', 'public') + ".brief_platforms.id"))
    brief_platform__details = relationship("Brief_PlatformModel", back_populates='deep_analytics', lazy='subquery')

    @classmethod
    async def objects(cls, session):
        obj = await Manager.async_init(cls, session)
        return obj



