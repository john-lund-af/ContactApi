import json
from pathlib import Path

class JsonDB:

    def __init__(self, file_path: str = "/app/db/contacts.json"):
        base_dir = Path(__file__).resolve().parent.parent
        self.file_path = base_dir / "db" / "contacts.json"

    def load(self) -> dict:
        with open(self.file_path) as file:
            return json.load(file)

    def save(self, data: dict) -> None:
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

