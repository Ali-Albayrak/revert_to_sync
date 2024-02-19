import os
import importlib
from core.logger import log

from actions import content_ready


import enum
from sqlalchemy import DATETIME, String, ForeignKey
from sqlalchemy import String, ForeignKey, Column, DATE, Enum, BOOLEAN, Text
from sqlalchemy.orm import relationship
from core.base_model import BaseModel
from core.manager import Manager
from fastapi import HTTPException
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import select

class CustomManager(Manager):



    async def post_update(self, **kwargs) -> dict:
        try:
            jwt = kwargs.get("jwt", {})
            new_data = kwargs.get("new_data", {})
            old_data = kwargs.get("old_data", {})
            well_known_urls = kwargs.get("well_known_urls", {})
            new_data = await content_ready.handler(jwt=jwt, new_data=new_data, old_data=old_data, well_known_urls=well_known_urls, method="update")
            return new_data
        except Exception as err:
            log.warn("at least one step in post_update trigger has been skipped")
            log.debug(err)
            log.error("Error while executing post_update trigger, check the debug above!")
            return new_data




# select enums
class RequestStatusEnum(str, enum.Enum):
    pending = "pending"
    success = "success"
    faill = "faill"


class Strategy_ContentModel(BaseModel):
    __tablename__ = 'strategy_contents'
    __table_args__ = {'schema': os.environ.get('DEFAULT_SCHEMA', 'public')}


    language = Column(Text, nullable=True, default=None)

    voice_tone = Column(Text, nullable=True, default=None)

    call_to_action = Column(Text, nullable=True, default=None)

    company_bg = Column(Text, nullable=True, default=None)

    product_details = Column(Text, nullable=True, default=None)

    promotion_details = Column(Text, nullable=True, default=None)

    reference_link = Column(Text, nullable=True, default=None)

    request_status = Column(Enum(RequestStatusEnum), nullable=True, default=None)

    content_name = Column(Text, nullable=True, default=None)

    generated_content = Column(Text, nullable=True, default=None)

    generated_hashtags = Column(Text, nullable=True, default=None)

    puplishing_date = Column(DATE, nullable=True, default=None)

    approved = Column(BOOLEAN, nullable=True, default=False)


    strategy_plan = Column(UUID(as_uuid=True), ForeignKey(os.environ.get('DEFAULT_SCHEMA', 'public') + ".strategy_plans.id"))
    strategy_plan__details = relationship("Strategy_PlanModel", back_populates='strategy_contents', lazy='subquery')

    designs = relationship('DesignModel', back_populates='strategy_content__details', lazy='subquery')

    content_comments = relationship('Content_CommentModel', back_populates='strategy_content__details', lazy='subquery')

    @classmethod
    async def objects(cls, session):
        obj = await CustomManager.async_init(cls, session)
        return obj



