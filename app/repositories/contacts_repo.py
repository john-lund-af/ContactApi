from app.database.json_db import JsonDB


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
