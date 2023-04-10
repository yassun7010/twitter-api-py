from pathlib import Path


def json_test_data(filename: str) -> Path:
    """
    自動テスト用データの絶対ファイルパスを返す。
    """

    return Path(__file__).parent / filename
