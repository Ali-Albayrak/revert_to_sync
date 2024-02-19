import os
import importlib
from core.logger import log




import enum
from sqlalchemy import DATETIME, String, ForeignKey
from sqlalchemy import String, ForeignKey, Column, DATE, Text
from sqlalchemy.orm import relationship
from core.base_model import BaseModel
from core.manager import Manager
from fastapi import HTTPException
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import select



# select enums


class AdModel(BaseModel):
    __tablename__ = 'ads'
    __table_args__ = {'schema': os.environ.get('DEFAULT_SCHEMA', 'public')}


    name = Column(Text, nullable=True, default=None)

    about = Column(Text, nullable=True, default=None)

    start_date = Column(DATE, nullable=True, default=None)

    end_date = Column(DATE, nullable=True, default=None)


    strategy_plan = Column(UUID(as_uuid=True), ForeignKey(os.environ.get('DEFAULT_SCHEMA', 'public') + ".strategy_plans.id"))
    strategy_plan__details = relationship("Strategy_PlanModel", back_populates='ads', lazy='subquery')

    @classmethod
    async def objects(cls, session):
        obj = await Manager.async_init(cls, session)
        return obj



