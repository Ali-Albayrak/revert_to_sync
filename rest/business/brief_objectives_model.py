import os
import importlib
from core.logger import log




import enum
from sqlalchemy import DATETIME, String, ForeignKey
from sqlalchemy import String, ForeignKey, Column, Enum, JSON, Text
from sqlalchemy.orm import relationship
from core.base_model import BaseModel
from core.manager import Manager
from fastapi import HTTPException
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import select



# select enums
class ObjectivesEnum(str, enum.Enum):
    branding = "branding"
    brand_awareness = "brand_awareness"
    sales = "sales"
    engagement = "engagement"


class Brief_ObjectiveModel(BaseModel):
    __tablename__ = 'brief_objectives'
    __table_args__ = {'schema': os.environ.get('DEFAULT_SCHEMA', 'public')}


    name = Column(Text, nullable=True, default=None)

    objectives = Column(Enum(ObjectivesEnum), nullable=True, default=None)

    kpi_goals = Column(JSON, nullable=True, default=None)


    brief = Column(UUID(as_uuid=True), ForeignKey(os.environ.get('DEFAULT_SCHEMA', 'public') + ".briefs.id"))
    brief__details = relationship("BriefModel", back_populates='brief_objectives', lazy='subquery')

    @classmethod
    async def objects(cls, session):
        obj = await Manager.async_init(cls, session)
        return obj



