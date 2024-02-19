import os
import importlib
from core.logger import log

from actions import attach_customer_to_new_user, create_brief_strategy_id, delete_user_after_customer


import enum
from sqlalchemy import DATETIME, String, ForeignKey
from sqlalchemy import String, ForeignKey, Column, Enum, JSON, Integer, Text
from sqlalchemy.orm import relationship
from core.base_model import BaseModel
from core.manager import Manager
from fastapi import HTTPException
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import select

class CustomManager(Manager):
    async def pre_save(self, **kwargs) -> dict:
        try:
            jwt = kwargs.get("jwt", {})
            new_data = kwargs.get("new_data", {})
            old_data = kwargs.get("old_data", {})
            well_known_urls = kwargs.get("well_known_urls", {})
            new_data = attach_customer_to_new_user.handler(jwt=jwt, new_data=new_data, old_data=old_data, well_known_urls=well_known_urls, method="create")
            return new_data
        except Exception as err:
            log.warn("at least one step in pre_create trigger has been skipped")
            log.debug(err)
            log.error("Error while executing pre_create trigger, check the debug above!")
            return new_data

    async def post_save(self, **kwargs) -> dict:
        try:
            jwt = kwargs.get("jwt", {})
            new_data = kwargs.get("new_data", {})
            old_data = kwargs.get("old_data", {})
            well_known_urls = kwargs.get("well_known_urls", {})
            new_data = create_brief_strategy_id.handler(jwt=jwt, new_data=new_data, old_data=old_data, well_known_urls=well_known_urls, method="create")
            return new_data
        except Exception as err:
            log.warn("at least one step in post_create trigger has been skipped")
            log.debug(err)
            log.error("Error while executing post_create trigger, check the debug above!")
            return new_data




    async def post_delete(self, **kwargs) -> bool:
        try:
            jwt = kwargs.get("jwt", {})
            new_data = kwargs.get("new_data", {})
            old_data = kwargs.get("old_data", {})
            well_known_urls = kwargs.get("well_known_urls", {})
            new_data = delete_user_after_customer.handler(jwt=jwt, new_data=new_data, old_data=old_data, well_known_urls=well_known_urls, method="delete")
            return new_data
        except Exception as err:
            log.warn("at least one step in post_delete trigger has been skipped")
            log.debug(err)
            log.error("Error while executing post_delete trigger, check the debug above!")
            return new_data


# select enums
class AccountTypeEnum(str, enum.Enum):
    individual = "individual"
    multi = "multi"
class StageEnum(str, enum.Enum):
    analysis = "analysis"
    strategy = "strategy"
class IndicationEnum(str, enum.Enum):
    approved = "approved"
    draft = "draft"


class CustomerModel(BaseModel):
    __tablename__ = 'customers'
    __table_args__ = {'schema': os.environ.get('DEFAULT_SCHEMA', 'public')}


    email = Column(Text, nullable=True, default=None)

    username = Column(Text, nullable=True, default=None)

    first_name = Column(Text, nullable=True, default=None)

    last_name = Column(Text, nullable=True, default=None)

    full_name = Column(Text, nullable=True, default=None)

    phone = Column(Text, nullable=True, default=None)

    profile_picture = Column(UUID(as_uuid=True), ForeignKey("public.files.id"))

    addresses = Column(JSON, nullable=True, default=None)

    account_manager = Column(Text, nullable=True, default=None)

    industry = Column(Text, nullable=True, default=None)

    sub_industry = Column(Text, nullable=True, default=None)

    brand_name = Column(Text, nullable=True, default=None)

    business_number = Column(Text, nullable=True, default=None)

    personal_number = Column(Text, nullable=True, default=None)

    account_type = Column(Enum(AccountTypeEnum), nullable=True, default=None)

    completion_percentage = Column(Integer, nullable=True, default=None)

    stage = Column(Enum(StageEnum), nullable=True, default=None)

    indication = Column(Enum(IndicationEnum), nullable=True, default=None)

    briefs = relationship('BriefModel', back_populates='customer__details')

    strategies = relationship('StrategyModel', back_populates='customer__details')

    appointments = relationship('AppointmentModel', back_populates='customer__details')

    file_assets = relationship('File_AssetModel', back_populates='customer__details')

    folders = relationship('FolderModel', back_populates='customer__details')

    designs = relationship('DesignModel', back_populates='customer__details')


    user = Column(UUID(as_uuid=True), ForeignKey("public.users.id"))


    @classmethod
    async def objects(cls, session):
        obj = await CustomManager.async_init(cls, session)
        return obj




    @classmethod
    async def validate_unique_brand_name(cls, db, brand_name, id=None):
        query = db.query(cls).filter_by(brand_name=brand_name)
        if id is not None:
            query = query.filter(cls.id != id)
        existing_record = query.first()
        if existing_record:
            raise HTTPException(status_code=422, detail={
                "field_name": "brand_name",
                "message": f"brand_name should be unique"
            })
    @classmethod
    async def validate_unique_business_number(cls, db, business_number, id=None):
        # query = select(cls).where(cls.business_number==business_number)
        query = db.query(cls).filter_by(business_number=business_number)
        if id is not None:
            query = query.filter(cls.id != id)
        existing_record = query.first()
        # if id is not None:
        #     query = query.where(cls.id != id)
        # result = await db.execute(query)
        # existing_record = result.scalars().first()
        if existing_record:
            raise HTTPException(status_code=422, detail={
                "field_name": "business_number",
                "message": f"business_number should be unique"
            })