from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class ContactInfo(BaseModel):
    type: str = Field(..., min_length=1, examples=["private", "work"])
    phone: Optional[str] = None
    email: Optional[EmailStr] = None


class Address(BaseModel):
    type: str = Field(..., min_length=1, examples=["home", "work"])
    street: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None


class ContactCreate(BaseModel):
    first_name: str = Field(..., min_length=2)
    last_name: str = Field(..., min_length=2)
    notes: Optional[str] = None
    favorite: bool = False
    contact_infos: list[ContactInfo] = []
    addresses: list[Address] = []


class ContactUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=2)
    last_name: Optional[str] = Field(None, min_length=2)
    notes: Optional[str] = None
    favorite: Optional[bool] = None
    contact_infos: Optional[list[ContactInfo]] = None
    addresses: Optional[list[Address]] = None


class Contact(ContactCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime


class ContactDatabase(BaseModel):
    contacts: list[Contact] = []