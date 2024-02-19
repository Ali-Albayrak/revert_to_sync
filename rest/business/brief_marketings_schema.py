
from typing import Optional, Union
from typing import Union
import uuid
import enum
import datetime

from pydantic import BaseModel, validator, EmailStr, Field
from core.encryptStr import EncryptStr


# select enums
class MonthlyBudgetEnum(str, enum.Enum):
    _100_300 = "_100_300"
    _300_600 = "_300_600"
    _600_1000 = "_600_1000"
    _1000_2000 = "_1000_2000"
    other = "other"
# select enums
class DurationEnum(str, enum.Enum):
    _1_3 = "_1_3"
    _3_6 = "_3_6"
    _6_9 = "_6_9"
    _9_12 = "_9_12"
    more_than_a_year = "more_than_a_year"
# select enums
class FocusOnEnum(str, enum.Enum):
    website = "website"
    facebook = "facebook"
    instagram = "instagram"
    twitter = "twitter"
    tiktok = "tiktok"
    google = "google"
    youtube = "youtube"
# select enums
class SalesChannelEnum(str, enum.Enum):
    yemeksepeti = "yemeksepeti"
    hepsiburada = "hepsiburada"
    trendyol = "trendyol"
    getir = "getir"
    amazon = "amazon"


class CreateBrief_Marketing(BaseModel):
    id: Optional[uuid.UUID]
    current_online_activities: Optional[str] = Field(default=None)
    marketing_angels: Optional[str] = Field(default=None)
    previous_activities: Optional[str] = Field(default=None)
    previous_issues: Optional[str] = Field(default=None)
    monthly_budget: Optional[MonthlyBudgetEnum]
    duration: Optional[DurationEnum]
    focus_on: Optional[list[FocusOnEnum]]
    sales_channel: Optional[list[SalesChannelEnum]]
    brief: uuid.UUID

    @validator('monthly_budget')
    def validate_monthly_budget(cls, monthly_budget: Optional[MonthlyBudgetEnum]):
        if False or False or False:
            raise ValueError(f"field <monthly_budget> is not allowed")
        return monthly_budget
    @validator('duration')
    def validate_duration(cls, duration: Optional[DurationEnum]):
        if False or False or False:
            raise ValueError(f"field <duration> is not allowed")
        return duration
    @validator('focus_on')
    def validate_focus_on(cls, focus_on: Optional[list[FocusOnEnum]]):
        if False or False or False:
            raise ValueError(f"field <focus_on> is not allowed")
        return focus_on
    @validator('sales_channel')
    def validate_sales_channel(cls, sales_channel: Optional[list[SalesChannelEnum]]):
        if False or False or False:
            raise ValueError(f"field <sales_channel> is not allowed")
        return sales_channel
    @validator('brief')
    def validate_brief(cls, brief: uuid.UUID):
        if False or False or False:
            raise ValueError(f"field <brief> is not allowed")
        return brief

class ReadBrief_Marketing(BaseModel):
    id: uuid.UUID
    created_on: datetime.datetime
    updated_on: datetime.datetime
    created_by: Optional[uuid.UUID] = Field(default=None)
    updated_by: Optional[uuid.UUID] = Field(default=None)
    current_online_activities: Optional[str] = Field(default=None)
    marketing_angels: Optional[str] = Field(default=None)
    previous_activities: Optional[str] = Field(default=None)
    previous_issues: Optional[str] = Field(default=None)
    monthly_budget: Optional[MonthlyBudgetEnum]
    duration: Optional[DurationEnum]
    focus_on: Optional[list[FocusOnEnum]]
    sales_channel: Optional[list[SalesChannelEnum]]
    brief: Optional[uuid.UUID] = Field(default=None)
    brief__details: Optional[object] = Field(default={})


    @validator('monthly_budget')
    def validate_monthly_budget(cls, monthly_budget: Optional[MonthlyBudgetEnum]):
        return monthly_budget

    @validator('duration')
    def validate_duration(cls, duration: Optional[DurationEnum]):
        return duration

    @validator('focus_on')
    def validate_focus_on(cls, focus_on: Optional[list[FocusOnEnum]]):
        return focus_on

    @validator('sales_channel')
    def validate_sales_channel(cls, sales_channel: Optional[list[SalesChannelEnum]]):
        return sales_channel

    class Config:
        orm_mode = True


class UpdateBrief_Marketing(BaseModel):
    current_online_activities: Optional[str] = Field(default=None)
    marketing_angels: Optional[str] = Field(default=None)
    previous_activities: Optional[str] = Field(default=None)
    previous_issues: Optional[str] = Field(default=None)
    monthly_budget: Optional[MonthlyBudgetEnum]
    duration: Optional[DurationEnum]
    focus_on: Optional[list[FocusOnEnum]]
    sales_channel: Optional[list[SalesChannelEnum]]
    brief: Optional[uuid.UUID] = Field(default=None)


    @validator('monthly_budget')
    def validate_monthly_budget(cls, monthly_budget: Optional[MonthlyBudgetEnum]):
        if False or '__' in monthly_budget or monthly_budget in ['id']:
            raise ValueError(f"field <monthly_budget> is not allowed")
        return monthly_budget

    @validator('duration')
    def validate_duration(cls, duration: Optional[DurationEnum]):
        if False or '__' in duration or duration in ['id']:
            raise ValueError(f"field <duration> is not allowed")
        return duration

    @validator('focus_on')
    def validate_focus_on(cls, focus_on: Optional[list[FocusOnEnum]]):
        if False or '__' in focus_on or focus_on in ['id']:
            raise ValueError(f"field <focus_on> is not allowed")
        return focus_on

    @validator('sales_channel')
    def validate_sales_channel(cls, sales_channel: Optional[list[SalesChannelEnum]]):
        if False or '__' in sales_channel or sales_channel in ['id']:
            raise ValueError(f"field <sales_channel> is not allowed")
        return sales_channel

    class Config:
        orm_mode = True


class ReadBrief_Marketings(BaseModel):
    data: list[Optional[ReadBrief_Marketing]]
    next_page: Union[str, int]
    page_size: int