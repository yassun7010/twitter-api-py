import pytest

from twitter_api.client.twitter_api_client import TwitterApiClient


class TestTwitterApiClient:
    def test_client(self, client):
        # インターフェースの未実装がないかをテストする。
        # TestTwitterApiMockClient はテストで必ずテストされるので、テスト不要。
        assert True

    def test_client_constructor(self):
        """
        TwitterApiClient でのコンストラクタによる生成を禁止する。

        TwitterApiClient.from_* 系統の表現によるインスタンス化しか許可しない。
        """
        with pytest.raises(TypeError):
            TwitterApiClient()  # type: ignore
