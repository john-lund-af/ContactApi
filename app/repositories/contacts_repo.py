from app.database.json_db import JsonDB
from uuid import uuid4

class ContactNotFoundError(Exception):
    pass


class ContactRepository:

    def __init__(self, db: JsonDB):
        self.db = db

    def get_all(self) -> list[dict]:
        data = self.db.load()
        return data["contacts"]


    def get_contact(self, contact_id: str) -> dict:
        data = self.db.load()

        for contact in data["contacts"]:
            if contact["id"] == contact_id:
                return contact
        else:
            raise ContactNotFoundError(f"Contact with id {contact_id} not found")


    def create_contact(self, contact_data: dict) -> dict:
        data = self.db.load()

        new_id = str(uuid4())
        new_contact = {
            "id": new_id,
            **contact_data
        }

        data["contacts"].append(new_contact)
        self.db.save(data)

        return new_contact


    def remove_contact(self, contact_id: str):
        data = self.db.load()

        contact = next((contact for contact in data["contacts"] if contact["id"] == contact_id), None)

        if contact is None:
            raise ContactNotFoundError(f"Contact with id {contact_id} not found")

        data["contacts"].remove(contact)
        self.db.save(data)
        return contact


    def update_contact(self, contact_id: str, new_contact_data: dict):
        data = self.db.load()

        for index, contact in enumerate(data["contacts"]):
            if contact_id == contact["id"]:
                updated_contact = {
                    "id": contact_id,
                    **new_contact_data
                }
                data["contacts"][index] = updated_contact
                self.db.save(data)
                return updated_contact

        raise ContactNotFoundError(f"Contact with id {contact_id} not found")

