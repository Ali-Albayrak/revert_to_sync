import os
import importlib
from core.logger import log




import enum
from sqlalchemy import DATETIME, String, ForeignKey
from sqlalchemy import String, ForeignKey, Column, Enum, Integer, BOOLEAN, Text
from sqlalchemy.orm import relationship
from core.base_model import BaseModel
from core.manager import Manager
from fastapi import HTTPException
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import select



# select enums
class PlatformEnum(str, enum.Enum):
    website = "website"
    facebook = "facebook"
    instagram = "instagram"
    twitter = "twitter"
    tiktok = "tiktok"
    google = "google"
    youtube = "youtube"
class PostFormatEnum(str, enum.Enum):
    video = "video"
    real = "real"
    story = "story"
    post = "post"
    design = "design"
    carousel = "carousel"
class ContentTypeEnum(str, enum.Enum):
    awareness = "awareness"
    branding = "branding"
    sales = "sales"
    engagement = "engagement"
    informative = "informative"


class Strategy_PlanModel(BaseModel):
    __tablename__ = 'strategy_plans'
    __table_args__ = {'schema': os.environ.get('DEFAULT_SCHEMA', 'public')}


    platform = Column(Enum(PlatformEnum), nullable=False, default=None)

    post_format = Column(Enum(PostFormatEnum), nullable=False, default=None)

    content_type = Column(Enum(ContentTypeEnum), nullable=False, default=None)

    publish_day = Column(Text, nullable=True, default=None)

    publish_time = Column(Text, nullable=True, default=None)

    num_of_posts = Column(Integer, nullable=True, default=None)

    content_requested = Column(BOOLEAN, nullable=True, default=False)

    ad_requested = Column(BOOLEAN, nullable=True, default=False)


    strategy = Column(UUID(as_uuid=True), ForeignKey(os.environ.get('DEFAULT_SCHEMA', 'public') + ".strategies.id"))
    strategy__details = relationship("StrategyModel", back_populates='strategy_plans', lazy='subquery')

    strategy_contents = relationship('Strategy_ContentModel', back_populates='strategy_plan__details', lazy='subquery')

    ads = relationship('AdModel', back_populates='strategy_plan__details', lazy='subquery')

    @classmethod
    async def objects(cls, session):
        obj = await Manager.async_init(cls, session)
        return obj



