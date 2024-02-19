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
class AdsBudgetEnum(str, enum.Enum):
    _100_300 = "_100_300"
    _300_600 = "_300_600"
    _600_1000 = "_600_1000"
    _1000_2000 = "_1000_2000"
    other = "other"


class StrategyModel(BaseModel):
    __tablename__ = 'strategies'
    __table_args__ = {'schema': os.environ.get('DEFAULT_SCHEMA', 'public')}



    customer = Column(UUID(as_uuid=True), ForeignKey(os.environ.get('DEFAULT_SCHEMA', 'public') + ".customers.id"))
    customer__details = relationship("CustomerModel", back_populates='strategies', lazy='subquery')

    name = Column(Text, nullable=True, default=None)

    strategy_plans = relationship('Strategy_PlanModel', back_populates='strategy__details', lazy='subquery')

    strategy_personas = relationship('Strategy_PersonaModel', back_populates='strategy__details', lazy='subquery')

    strategy_audiences = relationship('Strategy_AudienceModel', back_populates='strategy__details', lazy='subquery')

    strategy_objectives = relationship('Strategy_ObjectiveModel', back_populates='strategy__details', lazy='subquery')

    ads_budget = Column(Enum(AdsBudgetEnum), nullable=True, default=None)

    custom_budget = Column(Text, nullable=True, default=None)

    budget_distribution = Column(JSON, nullable=True, default=None)

    @classmethod
    async def objects(cls, session):
        obj = await Manager.async_init(cls, session)
        return obj



