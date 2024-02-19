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
class MonthlyBudgetEnum(str, enum.Enum):
    _100_300 = "_100_300"
    _300_600 = "_300_600"
    _600_1000 = "_600_1000"
    _1000_2000 = "_1000_2000"
    other = "other"
class DurationEnum(str, enum.Enum):
    _1_3 = "_1_3"
    _3_6 = "_3_6"
    _6_9 = "_6_9"
    _9_12 = "_9_12"
    more_than_a_year = "more_than_a_year"
class FocusOnEnum(str, enum.Enum):
    website = "website"
    facebook = "facebook"
    instagram = "instagram"
    twitter = "twitter"
    tiktok = "tiktok"
    google = "google"
    youtube = "youtube"
class SalesChannelEnum(str, enum.Enum):
    yemeksepeti = "yemeksepeti"
    hepsiburada = "hepsiburada"
    trendyol = "trendyol"
    getir = "getir"
    amazon = "amazon"


class Brief_MarketingModel(BaseModel):
    __tablename__ = 'brief_marketings'
    __table_args__ = {'schema': os.environ.get('DEFAULT_SCHEMA', 'public')}


    current_online_activities = Column(Text, nullable=True, default=None)

    marketing_angels = Column(Text, nullable=True, default=None)

    previous_activities = Column(Text, nullable=True, default=None)

    previous_issues = Column(Text, nullable=True, default=None)

    monthly_budget = Column(Enum(MonthlyBudgetEnum), nullable=True, default=None)

    duration = Column(Enum(DurationEnum), nullable=True, default=None)

    focus_on = Column(ARRAY(Text), nullable=True, default=None)

    sales_channel = Column(ARRAY(Text), nullable=True, default=None)


    brief = Column(UUID(as_uuid=True), ForeignKey(os.environ.get('DEFAULT_SCHEMA', 'public') + ".briefs.id"))
    brief__details = relationship("BriefModel", back_populates='brief_marketings', lazy='subquery')

    @classmethod
    async def objects(cls, session):
        obj = await Manager.async_init(cls, session)
        return obj



