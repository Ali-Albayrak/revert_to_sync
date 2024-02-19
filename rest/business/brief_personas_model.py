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


class Brief_PersonaModel(BaseModel):
    __tablename__ = 'brief_personas'
    __table_args__ = {'schema': os.environ.get('DEFAULT_SCHEMA', 'public')}


    voice_tone = Column(Text, nullable=True, default=None)

    buyers_role = Column(Text, nullable=True, default=None)

    best_time = Column(Text, nullable=True, default=None)

    demographical = Column(Text, nullable=True, default=None)


    brief = Column(UUID(as_uuid=True), ForeignKey(os.environ.get('DEFAULT_SCHEMA', 'public') + ".briefs.id"))
    brief__details = relationship("BriefModel", back_populates='brief_personas', lazy='subquery')

    @classmethod
    async def objects(cls, session):
        obj = await Manager.async_init(cls, session)
        return obj



