from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, HttpUrl

from app.models import RequestStatus, UserRole


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    company_name: str
    whatsapp_number: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class CompanyOut(BaseModel):
    id: int
    name: str
    whatsapp_number: str
    google_review_url: str | None = None
    google_place_id: str | None = None

    model_config = {'from_attributes': True}


class CompanyUpdate(BaseModel):
    name: str | None = None
    whatsapp_number: str | None = None
    google_review_url: HttpUrl | None = None
    google_place_id: str | None = None


class ReviewRequestCreate(BaseModel):
    customer_name: str
    customer_whatsapp: str
    service_name: str


class ReviewResponseIn(BaseModel):
    stars: int = Field(ge=1, le=5)
    comment: str | None = None


class ReviewRequestOut(BaseModel):
    id: int
    customer_name: str
    customer_whatsapp: str
    service_name: str
    status: RequestStatus
    stars: int | None = None
    comment: str | None = None
    created_at: datetime

    model_config = {'from_attributes': True}


class DashboardMetrics(BaseModel):
    total_requests: int
    rated: int
    average: float
    positive_rate: float
    critical_count: int
    pending: int


class WhatsAppTemplatePayload(BaseModel):
    to: str
    customer_name: str
    company_name: str


class GoogleReviewLinkOut(BaseModel):
    place_id: str | None = None
    review_url: str | None = None


class MeOut(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
    company_id: int

    model_config = {'from_attributes': True}
