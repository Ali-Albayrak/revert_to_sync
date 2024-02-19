import os
import importlib
from core.logger import log




import enum
from sqlalchemy import DATETIME, String, ForeignKey
from sqlalchemy import ARRAY, String, ForeignKey, Column, Enum, Text
from sqlalchemy.orm import relationship
from core.base_model import BaseModel
from core.manager import Manager
from fastapi import HTTPException
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import select



# select enums
class InformationResourceEnum(str, enum.Enum):
    social_media = "social_media"
    search_engines = "search_engines"
    family_and_friends = "family_and_friends"
    books = "books"
class AgeEnum(str, enum.Enum):
    under_18 = "under_18"
    _18_24 = "_18_24"
    _25_34 = "_25_34"
    _35_44 = "_35_44"
    _45_54 = "_45_54"
    _55_64 = "_55_64"
    _65_and_older = "_65_and_older"
class EducationStatusEnum(str, enum.Enum):
    less_than_high_school = "less_than_high_school"
    high_school = "high_school"
    associate = "associate"
    bachelor = "bachelor"
    master = "master"
    professional = "professional"
    doctorate = "doctorate"
class CommunicationPreferenceEnum(str, enum.Enum):
    phone = "phone"
    email = "email"
    text_messaging = "text_messaging"
    social_media = "social_media"
    face_to_face = "face_to_face"
class SocialNetworkEnum(str, enum.Enum):
    website = "website"
    facebook = "facebook"
    instagram = "instagram"
    twitter = "twitter"
    tiktok = "tiktok"
    google = "google"
    snapchat = "snapchat"
    youtube = "youtube"


class Strategy_PersonaModel(BaseModel):
    __tablename__ = 'strategy_personas'
    __table_args__ = {'schema': os.environ.get('DEFAULT_SCHEMA', 'public')}


    residence_location = Column(Text, nullable=False, default=None)

    income = Column(Text, nullable=False, default=None)

    industry = Column(Text, nullable=False, default=None)

    job_title = Column(Text, nullable=False, default=None)

    job_measurement = Column(Text, nullable=True, default=None)

    information_resource = Column(ARRAY(Text), nullable=False, default=None)

    age = Column(Enum(AgeEnum), nullable=False, default=None)

    education_status = Column(Enum(EducationStatusEnum), nullable=False, default=None)

    report_to = Column(Text, nullable=True, default=None)

    job_responsibilities = Column(Text, nullable=True, default=None)

    goals = Column(Text, nullable=False, default=None)

    challenges = Column(Text, nullable=False, default=None)

    communication_preference = Column(ARRAY(Text), nullable=False, default=None)

    social_network = Column(ARRAY(Text), nullable=False, default=None)


    strategy = Column(UUID(as_uuid=True), ForeignKey(os.environ.get('DEFAULT_SCHEMA', 'public') + ".strategies.id"))
    strategy__details = relationship("StrategyModel", back_populates='strategy_personas', lazy='subquery')

    @classmethod
    async def objects(cls, session):
        obj = await Manager.async_init(cls, session)
        return obj



