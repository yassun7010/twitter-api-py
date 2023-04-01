class TestTwitterApiRealClient:
    def test_real_client(self, real_client):
        # インターフェースの未実装がないかをテストする。
        # TestTwitterApiMockClient はテストで必ずテストされるので、テスト不要。
        assert True
