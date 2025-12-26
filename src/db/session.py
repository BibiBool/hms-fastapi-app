"""Session management and engine"""

import os
import datetime
import uuid
from collections.abc import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, relationship

# Change the string if you change database
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the environment")

class Base(DeclarativeBase):
    pass


# classes: users, providers, availability, appointments
class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    full_name = Column(String(50), nullable=False)
    role = Column(
        Enum("patient", "provider", "admin", name="user_roles"),
        nullable=False,
        default="patient",
    )


class Provider(Base):
    __tablename__ = "providers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    specialty = Column(String(50), nullable=False)
    bio = Column(Text, nullable=False)
    clinic_address = Column(Text, default=True)


class Availability(Base):
    __tablename__ = "availabilities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider_id = Column(
        UUID(as_uuid=True), ForeignKey("providers.id"), nullable=False
    )
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    is_booked = Column(Boolean, default=False)


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    provider_id = Column(
        UUID(as_uuid=True), ForeignKey("providers.id"), nullable=False
    )
    slot_id = Column(
        UUID(as_uuid=True),
        ForeignKey("availabilities.id"),
        unique=True,
        nullable=False,
    )
    status = Column(
        Enum("scheduled", "completed", "canceled", name="appointment_status"),
        default="scheduled",
    )
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
    )

    # Soft delete column
    deleted_at = Column(DateTime(timezone=True), nullable=True)


# Engine and Session Setup
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
