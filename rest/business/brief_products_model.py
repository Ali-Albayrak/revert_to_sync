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
class TypeEnum(str, enum.Enum):
    best_sale = "best_sale"
    top_sale = "top_sale"
    offer = "offer"


class Brief_ProductModel(BaseModel):
    __tablename__ = 'brief_products'
    __table_args__ = {'schema': os.environ.get('DEFAULT_SCHEMA', 'public')}


    product_image = Column(UUID(as_uuid=True), ForeignKey("public.files.id"))

    product_name = Column(Text, nullable=True, default=None)

    price = Column(Integer, nullable=True, default=None)

    type = Column(Enum(TypeEnum), nullable=True, default=None)

    discount = Column(Integer, nullable=True, default=None)


    brief = Column(UUID(as_uuid=True), ForeignKey(os.environ.get('DEFAULT_SCHEMA', 'public') + ".briefs.id"))
    brief__details = relationship("BriefModel", back_populates='brief_products', lazy='subquery')

    @classmethod
    async def objects(cls, session):
        obj = await Manager.async_init(cls, session)
        return obj



