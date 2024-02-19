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
class GenderEnum(str, enum.Enum):
    male = "male"
    female = "female"
    both = "both"
class AgeGroupEnum(str, enum.Enum):
    under_18 = "under_18"
    _18_24 = "_18_24"
    _25_34 = "_25_34"
    _35_44 = "_35_44"
    _45_54 = "_45_54"
    _55_64 = "_55_64"
    _65_and_older = "_65_and_older"
class TheClassEnum(str, enum.Enum):
    a = "a"
    b = "b"
    c = "c"


class Brief_AudienceModel(BaseModel):
    __tablename__ = 'brief_audiences'
    __table_args__ = {'schema': os.environ.get('DEFAULT_SCHEMA', 'public')}


    interests = Column(Text, nullable=True, default=None)

    journey = Column(Text, nullable=True, default=None)

    keywords = Column(Text, nullable=True, default=None)

    geo_audience = Column(ARRAY(Text), nullable=True, default=None)

    gender = Column(Enum(GenderEnum), nullable=True, default=None)

    age_group = Column(ARRAY(Text), nullable=True, default=None)

    the_class = Column(ARRAY(Text), nullable=True, default=None)

    sales_channel = Column(Text, nullable=True, default=None)


    brief = Column(UUID(as_uuid=True), ForeignKey(os.environ.get('DEFAULT_SCHEMA', 'public') + ".briefs.id"))
    brief__details = relationship("BriefModel", back_populates='brief_audiences', lazy='subquery')

    @classmethod
    async def objects(cls, session):
        obj = await Manager.async_init(cls, session)
        return obj



