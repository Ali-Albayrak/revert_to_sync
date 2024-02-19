
from typing import Optional, Union
from typing import Union
import uuid
import enum
import datetime

from pydantic import BaseModel, validator, EmailStr, Field
from core.encryptStr import EncryptStr


# select enums
class RequestStatusEnum(str, enum.Enum):
    pending = "pending"
    success = "success"
    faill = "faill"


class CreateStrategy_Content(BaseModel):
    id: Optional[uuid.UUID]
    language: Optional[str] = Field(default=None)
    voice_tone: Optional[str] = Field(default=None)
    call_to_action: Optional[str] = Field(default=None)
    company_bg: Optional[str] = Field(default=None)
    product_details: Optional[str] = Field(default=None)
    promotion_details: Optional[str] = Field(default=None)
    reference_link: Optional[str] = Field(default=None)
    request_status: Optional[RequestStatusEnum]
    content_name: Optional[str] = Field(default=None)
    generated_content: Optional[str] = Field(default=None)
    generated_hashtags: Optional[str] = Field(default=None)
    puplishing_date: Optional[datetime.date] = Field(default=None)
    approved: Optional[bool] = Field(default=False)
    strategy_plan: uuid.UUID

    @validator('request_status')
    def validate_request_status(cls, request_status: Optional[RequestStatusEnum]):
        if False or False or False:
            raise ValueError(f"field <request_status> is not allowed")
        return request_status
    @validator('strategy_plan')
    def validate_strategy_plan(cls, strategy_plan: uuid.UUID):
        if False or False or False:
            raise ValueError(f"field <strategy_plan> is not allowed")
        return strategy_plan

class ReadStrategy_Content(BaseModel):
    id: uuid.UUID
    created_on: datetime.datetime
    updated_on: datetime.datetime
    created_by: Optional[uuid.UUID] = Field(default=None)
    updated_by: Optional[uuid.UUID] = Field(default=None)
    language: Optional[str] = Field(default=None)
    voice_tone: Optional[str] = Field(default=None)
    call_to_action: Optional[str] = Field(default=None)
    company_bg: Optional[str] = Field(default=None)
    product_details: Optional[str] = Field(default=None)
    promotion_details: Optional[str] = Field(default=None)
    reference_link: Optional[str] = Field(default=None)
    request_status: Optional[RequestStatusEnum]
    content_name: Optional[str] = Field(default=None)
    generated_content: Optional[str] = Field(default=None)
    generated_hashtags: Optional[str] = Field(default=None)
    puplishing_date: Optional[datetime.date] = Field(default=None)
    approved: Optional[bool] = Field(default=False)
    strategy_plan: Optional[uuid.UUID] = Field(default=None)
    strategy_plan__details: Optional[object] = Field(default={})
    designs: Optional[list[object]] = Field(default=[{}])
    content_comments: Optional[list[object]] = Field(default=[{}])


    @validator('request_status')
    def validate_request_status(cls, request_status: Optional[RequestStatusEnum]):
        return request_status

    class Config:
        orm_mode = True


class UpdateStrategy_Content(BaseModel):
    language: Optional[str] = Field(default=None)
    voice_tone: Optional[str] = Field(default=None)
    call_to_action: Optional[str] = Field(default=None)
    company_bg: Optional[str] = Field(default=None)
    product_details: Optional[str] = Field(default=None)
    promotion_details: Optional[str] = Field(default=None)
    reference_link: Optional[str] = Field(default=None)
    request_status: Optional[RequestStatusEnum]
    content_name: Optional[str] = Field(default=None)
    generated_content: Optional[str] = Field(default=None)
    generated_hashtags: Optional[str] = Field(default=None)
    puplishing_date: Optional[datetime.date] = Field(default=None)
    approved: Optional[bool] = Field(default=False)
    strategy_plan: Optional[uuid.UUID] = Field(default=None)


    @validator('request_status')
    def validate_request_status(cls, request_status: Optional[RequestStatusEnum]):
        if False or '__' in request_status or request_status in ['id']:
            raise ValueError(f"field <request_status> is not allowed")
        return request_status

    class Config:
        orm_mode = True


class ReadStrategy_Contents(BaseModel):
    data: list[Optional[ReadStrategy_Content]]
    next_page: Union[str, int]
    page_size: int