import os
import importlib
from core.logger import log




import enum
from sqlalchemy import DATETIME, String, ForeignKey
from sqlalchemy import String, ForeignKey, Column, Enum, Integer, Text
from sqlalchemy.orm import relationship
from core.base_model import BaseModel
from core.manager import Manager
from fastapi import HTTPException
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import select



# select enums
class AccordingToEnum(str, enum.Enum):
    weekly = "weekly"
    monthly = "monthly"
    yearly = "yearly"


class Brief_BusinessModel(BaseModel):
    __tablename__ = 'brief_businesses'
    __table_args__ = {'schema': os.environ.get('DEFAULT_SCHEMA', 'public')}


    key = Column(Text, nullable=True, default=None)

    value = Column(Integer, nullable=True, default=None)

    according_to = Column(Enum(AccordingToEnum), nullable=True, default=None)


    brief = Column(UUID(as_uuid=True), ForeignKey(os.environ.get('DEFAULT_SCHEMA', 'public') + ".briefs.id"))
    brief__details = relationship("BriefModel", back_populates='brief_businesses', lazy='subquery')

    @classmethod
    async def objects(cls, session):
        obj = await Manager.async_init(cls, session)
        return obj



