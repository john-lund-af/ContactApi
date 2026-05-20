from datetime import datetime
from app.database.json_db import JsonDB
from uuid import uuid4, UUID

from app.models.contact_models import ContactCreate, Contact, ContactUpdate


class ContactNotFoundError(Exception):
    pass


class ContactRepository:

    def __init__(self, db: JsonDB):
        self.db = db

    def get_all(self) -> list[dict]:
        data = self.db.load()
        return data["contacts"]


    def get_contact(self, contact_id: UUID) -> dict:
        data = self.db.load()

        for contact in data["contacts"]:
            if UUID(contact["id"]) == contact_id:
                return contact
        else:
            raise ContactNotFoundError(f"Contact with id {contact_id} not found")


    def create_contact(self, contact_data: ContactCreate) -> Contact:
        data = self.db.load()
        now = datetime.now()

        new_contact = Contact(id=uuid4(), created_at=now, updated_at=now, **contact_data.model_dump())

        data["contacts"].append(new_contact.model_dump(mode="json"))
        self.db.save(data)

        return new_contact


    def remove_contact(self, contact_id: UUID) -> dict | None:
        data = self.db.load()

        contact = next((contact for contact in data["contacts"] if UUID(contact["id"]) == contact_id), None)

        if contact is None:
            raise ContactNotFoundError(f"Contact with id {contact_id} not found")

        data["contacts"].remove(contact)
        self.db.save(data)
        return contact


    def update_contact(self, contact_id: UUID, new_contact_data: ContactUpdate) -> Contact:
        data = self.db.load()

        for index, contact in enumerate(data["contacts"]):
            if contact_id == UUID(contact["id"]):
                now = datetime.now()

                updated_contact = Contact(id=contact_id,
                                          created_at=contact["created_at"],
                                          updated_at=now,
                                          **new_contact_data.model_dump())

                data["contacts"][index] = updated_contact.model_dump(mode="json")
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
        query_str = query_str.lower().strip()

        if not query_str:
            return []

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

