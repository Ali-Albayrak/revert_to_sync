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
    content = "content"
    design = "design"


class Content_CommentModel(BaseModel):
    __tablename__ = 'content_comments'
    __table_args__ = {'schema': os.environ.get('DEFAULT_SCHEMA', 'public')}


    comment = Column(Text, nullable=True, default=None)

    type = Column(Enum(TypeEnum), nullable=True, default=None)


    strategy_content = Column(UUID(as_uuid=True), ForeignKey(os.environ.get('DEFAULT_SCHEMA', 'public') + ".strategy_contents.id"))
    strategy_content__details = relationship("Strategy_ContentModel", back_populates='content_comments', lazy='subquery')

    @classmethod
    async def objects(cls, session):
        obj = await Manager.async_init(cls, session)
        return obj



