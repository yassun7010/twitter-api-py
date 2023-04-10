from pathlib import Path


def json_test_data(filename: str) -> Path:
    """
    自動テスト用データのファイルパスを返す。

    自動テスト用のデータを作成したいときに使う。
    """

    return Path(__file__).parent / filename
