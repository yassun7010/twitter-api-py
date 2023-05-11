from twitter_api.client.request.request_mock_client import RequestMockClient
from twitter_api.rate_limit.manager import DEFAULT_RATE_LIMIT_MANAGER
from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager
from twitter_api.rate_limit.rate_limit import rate_limit
from twitter_api.resources.api_resources import ApiResources
from twitter_api.types.endpoint import Endpoint

TEST_ENDPOINT = Endpoint("GET", "https://example.com")


def api_resource(rate_limit_manager: RateLimitManager):
    return ApiResources(
        RequestMockClient(
            oauth_version="2.0",
            rate_limit_target="app",
            rate_limit_manager=rate_limit_manager,
        )
    )


class TestRateLimit:
    def test_rate_limit(self):
        @rate_limit(
            TEST_ENDPOINT,
            "app",
            requests=500,
            mins=15,
        )
        def handle(self: ApiResources):
            return 1

        assert handle(api_resource(DEFAULT_RATE_LIMIT_MANAGER)) == 1
