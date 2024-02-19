
from typing import Optional, Union
from typing import Union
import uuid
import enum
import datetime

from pydantic import BaseModel, validator, EmailStr, Field
from core.encryptStr import EncryptStr


# select enums
class InformationResourceEnum(str, enum.Enum):
    social_media = "social_media"
    search_engines = "search_engines"
    family_and_friends = "family_and_friends"
    books = "books"
# select enums
class AgeEnum(str, enum.Enum):
    under_18 = "under_18"
    _18_24 = "_18_24"
    _25_34 = "_25_34"
    _35_44 = "_35_44"
    _45_54 = "_45_54"
    _55_64 = "_55_64"
    _65_and_older = "_65_and_older"
# select enums
class EducationStatusEnum(str, enum.Enum):
    less_than_high_school = "less_than_high_school"
    high_school = "high_school"
    associate = "associate"
    bachelor = "bachelor"
    master = "master"
    professional = "professional"
    doctorate = "doctorate"
# select enums
class CommunicationPreferenceEnum(str, enum.Enum):
    phone = "phone"
    email = "email"
    text_messaging = "text_messaging"
    social_media = "social_media"
    face_to_face = "face_to_face"
# select enums
class SocialNetworkEnum(str, enum.Enum):
    website = "website"
    facebook = "facebook"
    instagram = "instagram"
    twitter = "twitter"
    tiktok = "tiktok"
    google = "google"
    snapchat = "snapchat"
    youtube = "youtube"


class CreateStrategy_Persona(BaseModel):
    id: Optional[uuid.UUID]
    residence_location: str
    income: str
    industry: str
    job_title: str
    job_measurement: Optional[str] = Field(default=None)
    information_resource: list[InformationResourceEnum]
    age: AgeEnum
    education_status: EducationStatusEnum
    report_to: Optional[str] = Field(default=None)
    job_responsibilities: Optional[str] = Field(default=None)
    goals: str
    challenges: str
    communication_preference: list[CommunicationPreferenceEnum]
    social_network: list[SocialNetworkEnum]
    strategy: uuid.UUID

    @validator('information_resource')
    def validate_information_resource(cls, information_resource: list[InformationResourceEnum]):
        if False or False or False:
            raise ValueError(f"field <information_resource> is not allowed")
        return information_resource
    @validator('age')
    def validate_age(cls, age: AgeEnum):
        if False or False or False:
            raise ValueError(f"field <age> is not allowed")
        return age
    @validator('education_status')
    def validate_education_status(cls, education_status: EducationStatusEnum):
        if False or False or False:
            raise ValueError(f"field <education_status> is not allowed")
        return education_status
    @validator('communication_preference')
    def validate_communication_preference(cls, communication_preference: list[CommunicationPreferenceEnum]):
        if False or False or False:
            raise ValueError(f"field <communication_preference> is not allowed")
        return communication_preference
    @validator('social_network')
    def validate_social_network(cls, social_network: list[SocialNetworkEnum]):
        if False or False or False:
            raise ValueError(f"field <social_network> is not allowed")
        return social_network
    @validator('strategy')
    def validate_strategy(cls, strategy: uuid.UUID):
        if False or False or False:
            raise ValueError(f"field <strategy> is not allowed")
        return strategy

class ReadStrategy_Persona(BaseModel):
    id: uuid.UUID
    created_on: datetime.datetime
    updated_on: datetime.datetime
    created_by: Optional[uuid.UUID] = Field(default=None)
    updated_by: Optional[uuid.UUID] = Field(default=None)
    residence_location: str
    income: str
    industry: str
    job_title: str
    job_measurement: Optional[str] = Field(default=None)
    information_resource: list[InformationResourceEnum]
    age: AgeEnum
    education_status: EducationStatusEnum
    report_to: Optional[str] = Field(default=None)
    job_responsibilities: Optional[str] = Field(default=None)
    goals: str
    challenges: str
    communication_preference: list[CommunicationPreferenceEnum]
    social_network: list[SocialNetworkEnum]
    strategy: Optional[uuid.UUID] = Field(default=None)
    strategy__details: Optional[object] = Field(default={})


    @validator('information_resource')
    def validate_information_resource(cls, information_resource: list[InformationResourceEnum]):
        return information_resource

    @validator('age')
    def validate_age(cls, age: AgeEnum):
        return age

    @validator('education_status')
    def validate_education_status(cls, education_status: EducationStatusEnum):
        return education_status

    @validator('communication_preference')
    def validate_communication_preference(cls, communication_preference: list[CommunicationPreferenceEnum]):
        return communication_preference

    @validator('social_network')
    def validate_social_network(cls, social_network: list[SocialNetworkEnum]):
        return social_network

    class Config:
        orm_mode = True


class UpdateStrategy_Persona(BaseModel):
    residence_location: Optional[str] = Field(default=None)
    income: Optional[str] = Field(default=None)
    industry: Optional[str] = Field(default=None)
    job_title: Optional[str] = Field(default=None)
    job_measurement: Optional[str] = Field(default=None)
    information_resource: Optional[list[InformationResourceEnum]]
    age: Optional[AgeEnum]
    education_status: Optional[EducationStatusEnum]
    report_to: Optional[str] = Field(default=None)
    job_responsibilities: Optional[str] = Field(default=None)
    goals: Optional[str] = Field(default=None)
    challenges: Optional[str] = Field(default=None)
    communication_preference: Optional[list[CommunicationPreferenceEnum]]
    social_network: Optional[list[SocialNetworkEnum]]
    strategy: Optional[uuid.UUID] = Field(default=None)


    @validator('information_resource')
    def validate_information_resource(cls, information_resource: list[InformationResourceEnum]):
        if False or '__' in information_resource or information_resource in ['id']:
            raise ValueError(f"field <information_resource> is not allowed")
        return information_resource

    @validator('age')
    def validate_age(cls, age: AgeEnum):
        if False or '__' in age or age in ['id']:
            raise ValueError(f"field <age> is not allowed")
        return age

    @validator('education_status')
    def validate_education_status(cls, education_status: EducationStatusEnum):
        if False or '__' in education_status or education_status in ['id']:
            raise ValueError(f"field <education_status> is not allowed")
        return education_status

    @validator('communication_preference')
    def validate_communication_preference(cls, communication_preference: list[CommunicationPreferenceEnum]):
        if False or '__' in communication_preference or communication_preference in ['id']:
            raise ValueError(f"field <communication_preference> is not allowed")
        return communication_preference

    @validator('social_network')
    def validate_social_network(cls, social_network: list[SocialNetworkEnum]):
        if False or '__' in social_network or social_network in ['id']:
            raise ValueError(f"field <social_network> is not allowed")
        return social_network

    class Config:
        orm_mode = True


class ReadStrategy_Personas(BaseModel):
    data: list[Optional[ReadStrategy_Persona]]
    next_page: Union[str, int]
    page_size: int