import json
from pathlib import Path


class JsonDataLoader:
    def load(self, filename: str) -> dict:
        with open(get_json_data_filepath(filename)) as file:
            return json.load(file)


def get_json_data_filepath(filename: str) -> Path:
    """
    自動テスト用データのファイルパスを返す。

    自動テスト用のデータを作成したいときに使う。
    """
    return Path(__file__).parent / filename
