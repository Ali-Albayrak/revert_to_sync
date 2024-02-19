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


class AppointmentModel(BaseModel):
    __tablename__ = 'appointments'
    __table_args__ = {'schema': os.environ.get('DEFAULT_SCHEMA', 'public')}



    customer = Column(UUID(as_uuid=True), ForeignKey(os.environ.get('DEFAULT_SCHEMA', 'public') + ".customers.id"))
    customer__details = relationship("CustomerModel", back_populates='appointments', lazy='subquery')

    approval_status = Column(Text, nullable=True, default=None)

    account_manager = Column(Text, nullable=True, default=None)

    meeting_schedule = Column(Text, nullable=True, default=None)

    brief_last_update = Column(DATE, nullable=True, default=None)

    @classmethod
    async def objects(cls, session):
        obj = await Manager.async_init(cls, session)
        return obj



