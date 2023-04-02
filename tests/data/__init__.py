import json
from pathlib import Path


class JsonDataLoader:
    def load(self, filename: str) -> dict:
        with open(get_json_data_filepath(filename)) as file:
            return json.load(file)


def get_json_data_filepath(filename: str) -> Path:
    return Path(__file__).parent / filename
