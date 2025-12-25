"""Defines the type of data we expect in our patient endpoints for profiles"""

from datetime import datetime
from typing import Optional
from uuid import UUID
import enum

from pydantic import BaseModel, ConfigDict, EmailStr
from fastapi_users import schemas


# ----------------- Users Schemas -----------------
class UserRole(str, enum.Enum):
    PATIENT = "patient"
    PROVIDER = "provider"
    ADMIN = "admin"


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.PATIENT


class UserCreate(schemas.BaseUserCreate):
    full_name: str
    role: UserRole = UserRole.PATIENT
    # email and password fields are inherited


class UserRead(schemas.BaseUser[UUID]):
    full_name: str
    role: UserRole

    # model_config is inherited from BaseUser, no need to redefine
    # id, email, is_active, is_superuser, is_verified are also inherited
    

# Note: Inherit from fastapi_users.schemas.BaseUserUpdate (Optional but recommended)
class UserUpdate(schemas.BaseUserUpdate):
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    

# ------------ Providers & Availability Schemas ------------
class ProviderBase(BaseModel):
    specialty: str
    bio: str
    clinic_address: Optional[str] = None


class ProviderCreate(ProviderBase):
    user_id: UUID


class ProviderRead(ProviderBase):
    id: UUID
    user_id: UUID
    model_config = ConfigDict(from_attributes=True)


class Availability(BaseModel):
    id: UUID
    provider_id: UUID
    start_time: datetime
    end_time: datetime
    is_booked: bool
    model_config = ConfigDict(from_attributes=True)


# ----------------- Appointment Schemas -----------------
class AppointmentBase(BaseModel):
    provider_id: UUID
    slot_id: UUID


class AppointmentCreate(AppointmentBase):
    pass  # patient_id is taken from the JWT token, not the request body


class AppointmentRead(AppointmentBase):
    id: UUID
    patient_id: UUID
    status: str
    created_at: datetime
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
