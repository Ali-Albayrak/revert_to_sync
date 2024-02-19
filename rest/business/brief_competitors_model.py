import os
import importlib
from core.logger import log




import enum
from sqlalchemy import DATETIME, String, ForeignKey
from sqlalchemy import String, ForeignKey, Column, Text, ARRAY
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


class Brief_CompetitorModel(BaseModel):
    __tablename__ = 'brief_competitors'
    __table_args__ = {'schema': os.environ.get('DEFAULT_SCHEMA', 'public')}


    platform = Column(ARRAY(Text), nullable=True, default=None)

    link = Column(Text, nullable=True, default=None)


    brief = Column(UUID(as_uuid=True), ForeignKey(os.environ.get('DEFAULT_SCHEMA', 'public') + ".briefs.id"))
    brief__details = relationship("BriefModel", back_populates='brief_competitors', lazy='subquery')

    @classmethod
    async def objects(cls, session):
        obj = await Manager.async_init(cls, session)
        return obj



