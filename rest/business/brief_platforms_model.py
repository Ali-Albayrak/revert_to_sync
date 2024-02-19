import os
import importlib
from core.logger import log




import enum
from sqlalchemy import DATETIME, String, ForeignKey
from sqlalchemy import String, ForeignKey, Column, Enum, BOOLEAN, Text
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


class Brief_PlatformModel(BaseModel):
    __tablename__ = 'brief_platforms'
    __table_args__ = {'schema': os.environ.get('DEFAULT_SCHEMA', 'public')}


    platform = Column(Enum(PlatformEnum), nullable=True, default=None)

    page_link = Column(Text, nullable=True, default=None)

    business_link = Column(Text, nullable=True, default=None)

    paired = Column(BOOLEAN, nullable=True, default=False)

    deep_analytics = relationship('Deep_AnalysisModel', back_populates='brief_platform__details', lazy='subquery')


    brief = Column(UUID(as_uuid=True), ForeignKey(os.environ.get('DEFAULT_SCHEMA', 'public') + ".briefs.id"))
    brief__details = relationship("BriefModel", back_populates='brief_platforms', lazy='subquery')

    @classmethod
    async def objects(cls, session):
        obj = await Manager.async_init(cls, session)
        return obj



