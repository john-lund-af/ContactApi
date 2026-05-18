from datetime import datetime
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
        now:str = datetime.now().isoformat()

        new_contact = {
            "id": new_id,
            "created_at": now,
            "updated_at": now,
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
                now: str = datetime.now().isoformat()

                updated_contact = {
                    "id": contact_id,
                    "created_at": contact["created_at"],
                    "updated_at": now,
                    **new_contact_data
                }
                data["contacts"][index] = updated_contact
                self.db.save(data)
                return updated_contact

        raise ContactNotFoundError(f"Contact with id {contact_id} not found")


    def search_contacts(self, query_str: str) -> list[dict]:
        """
        Retrieves contacts that contain the query string in any of the string properties of the contact
        :param query_str: A string with the content to search for
        :return: A list with contacts that had the content of the searched string
        """
        data = self.db.load()
        result = []

        def contains_query(value) -> bool:
            if isinstance(value, str):
                return query_str in value.lower()

            if isinstance(value, dict):
                for item in value.values():
                    if contains_query(item):
                        return True

            if isinstance(value, list):
                for item in value:
                    if contains_query(item):
                        return True

            return False

        for contact in data["contacts"]:
            if contains_query(contact):
                result.append(contact)

        return result

