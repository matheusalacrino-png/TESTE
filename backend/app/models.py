import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class UserRole(str, enum.Enum):
    owner = 'owner'
    manager = 'manager'


class RequestStatus(str, enum.Enum):
    pending = 'pending'
    internal = 'internal'
    google = 'google'


class Company(Base):
    __tablename__ = 'companies'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(180), nullable=False)
    whatsapp_number: Mapped[str] = mapped_column(String(30), nullable=False)
    google_review_url: Mapped[str] = mapped_column(String(500), nullable=True)
    google_place_id: Mapped[str] = mapped_column(String(120), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    users = relationship('User', back_populates='company')
    requests = relationship('ReviewRequest', back_populates='company')


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.owner)
    company_id: Mapped[int] = mapped_column(ForeignKey('companies.id'), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    company = relationship('Company', back_populates='users')


class ReviewRequest(Base):
    __tablename__ = 'review_requests'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey('companies.id'), index=True)
    customer_name: Mapped[str] = mapped_column(String(120), nullable=False)
    customer_whatsapp: Mapped[str] = mapped_column(String(30), nullable=False)
    service_name: Mapped[str] = mapped_column(String(160), nullable=False)
    status: Mapped[RequestStatus] = mapped_column(Enum(RequestStatus), default=RequestStatus.pending)
    stars: Mapped[int | None] = mapped_column(Integer, nullable=True)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    company = relationship('Company', back_populates='requests')
