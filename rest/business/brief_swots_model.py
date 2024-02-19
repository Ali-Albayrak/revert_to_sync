import os
import importlib
from core.logger import log




import enum
from sqlalchemy import DATETIME, String, ForeignKey
from sqlalchemy import String, ForeignKey, Column, Text
from sqlalchemy.orm import relationship
from core.base_model import BaseModel
from core.manager import Manager
from fastapi import HTTPException
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import select



# select enums


class Brief_SwotModel(BaseModel):
    __tablename__ = 'brief_swots'
    __table_args__ = {'schema': os.environ.get('DEFAULT_SCHEMA', 'public')}


    strength_keywords = Column(Text, nullable=True, default=None)

    strength_description = Column(Text, nullable=True, default=None)

    weakness_keywords = Column(Text, nullable=True, default=None)

    weakness_description = Column(Text, nullable=True, default=None)

    opportunities_keywords = Column(Text, nullable=True, default=None)

    opportunities_description = Column(Text, nullable=True, default=None)

    threats_keywords = Column(Text, nullable=True, default=None)

    threats_description = Column(Text, nullable=True, default=None)

    usps = Column(Text, nullable=True, default=None)

    challenges = Column(Text, nullable=True, default=None)

    your_reputation = Column(Text, nullable=True, default=None)

    occasions_of_best_sale = Column(Text, nullable=True, default=None)


    brief = Column(UUID(as_uuid=True), ForeignKey(os.environ.get('DEFAULT_SCHEMA', 'public') + ".briefs.id"))
    brief__details = relationship("BriefModel", back_populates='brief_swots', lazy='subquery')

    @classmethod
    async def objects(cls, session):
        obj = await Manager.async_init(cls, session)
        return obj



