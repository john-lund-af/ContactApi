from uuid import UUID
from fastapi import APIRouter, HTTPException, Query
from app.database.json_db import JsonDB
from app.models.contact_models import Contact, ContactCreate
from app.repositories import contacts_repo
from app.repositories.contacts_repo import ContactRepository, ContactNotFoundError

router = APIRouter()
contact_repo = ContactRepository(JsonDB())


@router.get("/", response_model=list[Contact])
def get_contacts():
    try:
        return contact_repo.get_all()
    except Exception as exc:
        print(exc)
        raise HTTPException(status_code=500, detail="Failed to fetch contacts")


@router.get("/search", response_model=list[Contact])
def search_contacts(query: str = Query(..., min_lenght=1)):
    try:
        return contact_repo.search_contacts(query)
    except Exception as exc:
        print(exc)
        raise HTTPException(status_code=500, detail="Internal error fetching contacts")


@router.get("/{contact_id}", response_model=Contact)
def get_contact(contact_id: UUID):
    try:
        return contact_repo.get_contact(contact_id)
    except ContactNotFoundError as cnfexc:
        raise HTTPException(status_code=404, detail=str(cnfexc))
    except Exception as exc:
        print(exc)
        raise HTTPException(status_code=500, detail="Internal error fetching contact")


@router.post("/", response_model=Contact)
def create_contact(contact: ContactCreate):
    try:
        return contact_repo.create_contact(contact)
    except Exception as exc:
        print(exc)
        raise HTTPException(status_code=500, detail="Internal error creating contact")


@router.delete("/{contact_id}", response_model=Contact)
def delete_contact(contact_id: UUID):
    try:
        return contact_repo.remove_contact(contact_id)
    except ContactNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.put("/{contact_id}")
def update_contact(contact_id, updated_contact: dict):
    try:
        return contact_repo.update_contact(contact_id, updated_contact)
    except ContactNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

