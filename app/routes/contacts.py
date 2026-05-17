from fastapi import APIRouter, HTTPException
from app.database.json_db import JsonDB
from app.repositories import contacts_repo
from app.repositories.contacts_repo import ContactRepository, ContactNotFoundError

router = APIRouter()
contact_repo = ContactRepository(JsonDB())


@router.get("/")
def get_contacts():
    try:
        return contact_repo.get_all()
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch contacts")


@router.get("/{contact_id}")
def get_contact(contact_id):
    try:
        return contact_repo.get_contact(contact_id)
    except ContactNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.post("/")
def create_contact(contact: dict):
    return contact_repo.create_contact(contact)


@router.delete("/{contact_id}")
def delete_contact(contact_id: str):
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

