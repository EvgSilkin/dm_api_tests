from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict


class UserRole(str, Enum):
    GUEST = "Guest"
    PLAYER = "Player"
    ADMINISTRATOR = "Administrator"
    NANNY_MODERATOR = "NannyModerator"
    REGULAR_MODERATOR = "RegularModerator"
    SENIOR_MODERATOR = "SeniorModerator"


class Paging(BaseModel):
    posts_per_page: int = Field(..., alias='postsPerPage')
    comments_per_page: int = Field(..., alias='commentsPerPage')
    topics_per_page: int = Field(..., alias='topicsPerPage')
    messages_per_page: int = Field(..., alias='messagesPerPage')
    entities_per_page: int = Field(..., alias='entitiesPerPage')


class Settings(BaseModel):
    color_schema: str = Field(..., alias='colorSchema')
    paging: Paging


class Rating(BaseModel):
    enabled: bool
    quality: int
    quantity: int


class Resource(BaseModel):
    info: str
    settings: Settings
    login: str
    roles: List[UserRole]
    rating: Rating
    online: datetime
    registration: datetime


class UserDetailsEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")
    resource: Optional[Resource] = None
    metadata: Optional[str] = None
