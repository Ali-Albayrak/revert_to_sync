import os
import importlib
from core.logger import log




import enum
from sqlalchemy import DATETIME, String, ForeignKey
from sqlalchemy import BOOLEAN, String, ForeignKey, Column, Text
from sqlalchemy.orm import relationship
from core.base_model import BaseModel
from core.manager import Manager
from fastapi import HTTPException
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import select



# select enums


class FolderModel(BaseModel):
    __tablename__ = 'folders'
    __table_args__ = {'schema': os.environ.get('DEFAULT_SCHEMA', 'public')}


    folder_name = Column(Text, nullable=False, default=None)

    favorite = Column(BOOLEAN, nullable=True, default=False)

    deleted = Column(BOOLEAN, nullable=True, default=False)


    customer = Column(UUID(as_uuid=True), ForeignKey(os.environ.get('DEFAULT_SCHEMA', 'public') + ".customers.id"))
    customer__details = relationship("CustomerModel", back_populates='folders', lazy='subquery')

    file_assets = relationship('File_AssetModel', back_populates='folder__details', lazy='subquery')

    @classmethod
    async def objects(cls, session):
        obj = await Manager.async_init(cls, session)
        return obj



