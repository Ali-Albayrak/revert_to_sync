import os
import importlib
from core.logger import log




import enum
from sqlalchemy import DATETIME, String, ForeignKey
from sqlalchemy import Enum, String, ForeignKey, Column, Text
from sqlalchemy.orm import relationship
from core.base_model import BaseModel
from core.manager import Manager
from fastapi import HTTPException
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import select



# select enums
class StatusEnum(str, enum.Enum):
    pending = "pending"
    todo = "todo"
    completed = "completed"


class BriefModel(BaseModel):
    __tablename__ = 'briefs'
    __table_args__ = {'schema': os.environ.get('DEFAULT_SCHEMA', 'public')}



    customer = Column(UUID(as_uuid=True), ForeignKey(os.environ.get('DEFAULT_SCHEMA', 'public') + ".customers.id"))
    customer__details = relationship("CustomerModel", back_populates='briefs', lazy='subquery')

    brief_platforms = relationship('Brief_PlatformModel', back_populates='brief__details', lazy='subquery')

    brief_competitors = relationship('Brief_CompetitorModel', back_populates='brief__details', lazy='subquery')

    brief_products = relationship('Brief_ProductModel', back_populates='brief__details', lazy='subquery')

    brief_audiences = relationship('Brief_AudienceModel', back_populates='brief__details', lazy='subquery')

    brief_personas = relationship('Brief_PersonaModel', back_populates='brief__details', lazy='subquery')

    brief_swots = relationship('Brief_SwotModel', back_populates='brief__details', lazy='subquery')

    brief_marketings = relationship('Brief_MarketingModel', back_populates='brief__details', lazy='subquery')

    brief_objectives = relationship('Brief_ObjectiveModel', back_populates='brief__details', lazy='subquery')

    brief_businesses = relationship('Brief_BusinessModel', back_populates='brief__details', lazy='subquery')

    brief_extras = relationship('Brief_ExtraModel', back_populates='brief__details', lazy='subquery')

    extra_details = Column(Text, nullable=True, default=None)

    status = Column(Enum(StatusEnum), nullable=True, default=None)

    @classmethod
    async def objects(cls, session):
        obj = await Manager.async_init(cls, session)
        return obj



