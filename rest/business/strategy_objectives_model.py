import os
import importlib
from core.logger import log




import enum
from sqlalchemy import DATETIME, String, ForeignKey
from sqlalchemy import String, ForeignKey, Column, JSON, Enum
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
class PercentageEnum(str, enum.Enum):
    _10 = "_10"
    _20 = "_20"
    _30 = "_30"
    _40 = "_40"
    _50 = "_50"
    _60 = "_60"
    _70 = "_70"
    _80 = "_80"
    _90 = "_90"
    _100 = "_100"


class Strategy_ObjectiveModel(BaseModel):
    __tablename__ = 'strategy_objectives'
    __table_args__ = {'schema': os.environ.get('DEFAULT_SCHEMA', 'public')}


    objectives = Column(Enum(ObjectivesEnum), nullable=True, default=None)

    percentage = Column(Enum(PercentageEnum), nullable=True, default=None)

    kpi_goals = Column(JSON, nullable=True, default=None)


    strategy = Column(UUID(as_uuid=True), ForeignKey(os.environ.get('DEFAULT_SCHEMA', 'public') + ".strategies.id"))
    strategy__details = relationship("StrategyModel", back_populates='strategy_objectives', lazy='subquery')

    @classmethod
    async def objects(cls, session):
        obj = await Manager.async_init(cls, session)
        return obj



