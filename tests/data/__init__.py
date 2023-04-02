import json
from pathlib import Path


class JsonDataLoader:
    def load(self, filename: str) -> dict:
        with open(Path(__file__).parent / filename) as file:
            return json.load(file)
