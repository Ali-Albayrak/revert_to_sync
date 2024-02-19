import os
import importlib
from core.logger import log




import enum
from sqlalchemy import DATETIME, String, ForeignKey
from sqlalchemy import String, ForeignKey, Enum, Column, Text
from sqlalchemy.orm import relationship
from core.base_model import BaseModel
from core.manager import Manager
from fastapi import HTTPException
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import select



# select enums
class TypeEnum(str, enum.Enum):
    local = "local"
    vistaCreate = "vistaCreate"


class DesignModel(BaseModel):
    __tablename__ = 'designs'
    __table_args__ = {'schema': os.environ.get('DEFAULT_SCHEMA', 'public')}


    design_link = Column(Text, nullable=True, default=None)

    text_on_design = Column(Text, nullable=True, default=None)

    content_name = Column(Text, nullable=True, default=None)

    type = Column(Enum(TypeEnum), nullable=True, default=None)

    included_offer = Column(Text, nullable=True, default=None)

    notes = Column(Text, nullable=True, default=None)


    customer = Column(UUID(as_uuid=True), ForeignKey(os.environ.get('DEFAULT_SCHEMA', 'public') + ".customers.id"))
    customer__details = relationship("CustomerModel", back_populates='designs', lazy='subquery')


    strategy_content = Column(UUID(as_uuid=True), ForeignKey(os.environ.get('DEFAULT_SCHEMA', 'public') + ".strategy_contents.id"))
    strategy_content__details = relationship("Strategy_ContentModel", back_populates='designs', lazy='subquery')

    @classmethod
    async def objects(cls, session):
        obj = await Manager.async_init(cls, session)
        return obj



