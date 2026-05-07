from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/")
def get_contacts():
    pass

@router.get("/{contact_id}")
def get_contact(contact_id):
    pass
