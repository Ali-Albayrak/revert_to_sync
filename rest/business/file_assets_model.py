import os
import importlib
from core.logger import log




import enum
from sqlalchemy import DATETIME, String, ForeignKey
from sqlalchemy import String, ForeignKey, Column, DATE, Integer, BOOLEAN, Text
from sqlalchemy.orm import relationship
from core.base_model import BaseModel
from core.manager import Manager
from fastapi import HTTPException
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import select



# select enums


class File_AssetModel(BaseModel):
    __tablename__ = 'file_assets'
    __table_args__ = {'schema': os.environ.get('DEFAULT_SCHEMA', 'public')}


    file_name = Column(Text, nullable=False, default=None)

    asset = Column(UUID(as_uuid=True), ForeignKey("public.files.id"))

    file_size = Column(Integer, nullable=True, default=None)

    favorite = Column(BOOLEAN, nullable=True, default=False)

    deleted = Column(BOOLEAN, nullable=True, default=False)

    extension = Column(Text, nullable=True, default=None)

    open_time = Column(DATE, nullable=True, default=None)


    customer = Column(UUID(as_uuid=True), ForeignKey(os.environ.get('DEFAULT_SCHEMA', 'public') + ".customers.id"))
    customer__details = relationship("CustomerModel", back_populates='file_assets', lazy='subquery')


    folder = Column(UUID(as_uuid=True), ForeignKey(os.environ.get('DEFAULT_SCHEMA', 'public') + ".folders.id"))
    folder__details = relationship("FolderModel", back_populates='file_assets', lazy='subquery')

    @classmethod
    async def objects(cls, session):
        obj = await Manager.async_init(cls, session)
        return obj



