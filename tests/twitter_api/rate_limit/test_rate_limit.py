from contextlib import contextmanager
from datetime import datetime
from typing import Generator, Optional

import pytest

from twitter_api.client.request.request_async_mock_client import RequestAsyncMockClient
from twitter_api.client.request.request_mock_client import RequestMockClient
from twitter_api.rate_limit.manager import DEFAULT_RATE_LIMIT_MANAGER
from twitter_api.rate_limit.manager.rate_limit_manager import (
    RateLimitManager,
    RetryRateLimitHandling,
)
from twitter_api.rate_limit.rate_limit import rate_limit
from twitter_api.rate_limit.rate_limit_info import RateLimitInfo
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


def async_api_resource(rate_limit_manager: RateLimitManager):
    return ApiResources(
        RequestAsyncMockClient(
            oauth_version="2.0",
            rate_limit_target="app",
            rate_limit_manager=rate_limit_manager,
        )
    )


class IgnoreWhenErrorRateLimitManager(RateLimitManager):
    def check_limit_over(
        self, rate_limit_info: RateLimitInfo, now: Optional[datetime] = None
    ) -> Optional[float]:
        return None

    @contextmanager
    def handle(self, rate_limit_info: RateLimitInfo) -> Generator[None, None, None]:
        try:
            yield
        except Exception:
            pass


class RetryWhenErrorRateLimitManager(RateLimitManager):
    def check_limit_over(
        self, rate_limit_info: RateLimitInfo, now: Optional[datetime] = None
    ) -> Optional[float]:
        return None

    @contextmanager
    def handle(self, rate_limit_info: RateLimitInfo) -> Generator[None, None, None]:
        try:
            yield
        except Exception:
            raise RetryRateLimitHandling()


class TestRateLimit:
    def test_rate_limit(self):
        @rate_limit(TEST_ENDPOINT, "app", requests=500, mins=15)
        def handler(self: ApiResources):
            return 1

        assert handler(api_resource(DEFAULT_RATE_LIMIT_MANAGER)) == 1

    @pytest.mark.asyncio
    async def test_rate_limit_async(self):
        @rate_limit(TEST_ENDPOINT, "app", requests=500, mins=15)
        async def handler(self: ApiResources):
            return 1

        assert await handler(async_api_resource(DEFAULT_RATE_LIMIT_MANAGER)) == 1

    def test_rate_limit_raise_error(self):
        @rate_limit(TEST_ENDPOINT, "app", requests=500, mins=15)
        def handler(self: ApiResources):
            raise ValueError()

        with pytest.raises(ValueError):
            handler(api_resource(DEFAULT_RATE_LIMIT_MANAGER))

    @pytest.mark.asyncio
    async def test_rate_limit_raise_error_async(self):
        @rate_limit(TEST_ENDPOINT, "app", requests=500, mins=15)
        async def handler(self: ApiResources):
            raise ValueError()

        with pytest.raises(ValueError):
            await handler(async_api_resource(DEFAULT_RATE_LIMIT_MANAGER))

    def test_rate_limit_when_error_handler(self):
        @rate_limit(TEST_ENDPOINT, "app", requests=500, mins=15)
        def handler(self: ApiResources):
            raise ValueError()

        assert handler(api_resource(IgnoreWhenErrorRateLimitManager())) is None

    @pytest.mark.asyncio
    async def test_rate_limit_when_error_ahandler(self):
        @rate_limit(TEST_ENDPOINT, "app", requests=500, mins=15)
        async def handler(self: ApiResources):
            raise ValueError()

        assert (
            await handler(async_api_resource(IgnoreWhenErrorRateLimitManager())) is None
        )

    def test_rate_limit_when_sometimes_error_handler(self):
        result_iter = iter([ValueError(), ValueError(), 1])

        @rate_limit(TEST_ENDPOINT, "app", requests=500, mins=15)
        def handler(self: ApiResources):
            result = next(result_iter)
            if isinstance(result, ValueError):
                raise result
            else:
                return result

        assert handler(api_resource(RetryWhenErrorRateLimitManager())) == 1

    @pytest.mark.asyncio
    async def test_rate_limit_when_sometimes_error_ahandler(self):
        result_iter = iter([ValueError(), ValueError(), 1])

        @rate_limit(TEST_ENDPOINT, "app", requests=500, mins=15)
        async def handler(self: ApiResources):
            result = next(result_iter)
            if isinstance(result, ValueError):
                raise result
            else:
                return result

        assert await handler(async_api_resource(RetryWhenErrorRateLimitManager())) == 1
