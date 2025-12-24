"""Defines the type of data we expect in our patient endpoints for profiles"""
from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: str = "patient"
    
class UserCreate(UserBase):
    password: str # Plain text from client, will be hashed before DB save

class UserRead(UserBase):
    id: UUID
    is_active: bool

    # Allows Pydantic to read data from SQLAlchemy objects
    model_config = ConfigDict(from_attributes=True)



