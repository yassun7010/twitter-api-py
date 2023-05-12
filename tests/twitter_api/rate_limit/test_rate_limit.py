from contextlib import asynccontextmanager, contextmanager
from datetime import datetime
from typing import AsyncGenerator, Generator, Optional

import pytest

from twitter_api.client.request.request_async_mock_client import RequestAsyncMockClient
from twitter_api.client.request.request_mock_client import RequestMockClient
from twitter_api.rate_limit.continue_rate_limit_handling import (
    ContinueRateLimitHandling,
)
from twitter_api.rate_limit.manager import DEFAULT_RATE_LIMIT_MANAGER
from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager
from twitter_api.rate_limit.rate_limit import rate_limit
from twitter_api.rate_limit.rate_limit_info import RateLimitInfo
from twitter_api.resources.api_resources import ApiResources
from twitter_api.types.endpoint import Endpoint

TEST_ENDPOINT = Endpoint("GET", "https://example.com")


def api_resource_sync(rate_limit_manager: RateLimitManager):
    return ApiResources(
        RequestMockClient(
            oauth_version="2.0",
            rate_limit_target="app",
            rate_limit_manager=rate_limit_manager,
        )
    )


def api_resource_async(rate_limit_manager: RateLimitManager):
    return ApiResources(
        RequestAsyncMockClient(
            oauth_version="2.0",
            rate_limit_target="app",
            rate_limit_manager=rate_limit_manager,
        )
    )


class IgnoreValueErrorRateLimitManager(RateLimitManager):
    def check_limit_over(
        self, rate_limit_info: RateLimitInfo, now: Optional[datetime] = None
    ) -> Optional[float]:
        return None

    @contextmanager
    def handle_rate_limit_sync(
        self, rate_limit_info: RateLimitInfo
    ) -> Generator[None, None, None]:
        try:
            yield
            return
        except ValueError:
            raise ContinueRateLimitHandling()

    @asynccontextmanager
    async def handle_rate_limit_async(
        self, rate_limit_info: RateLimitInfo
    ) -> AsyncGenerator[None, None]:
        try:
            yield
            return
        except ValueError:
            raise ContinueRateLimitHandling()


class TestRateLimit:
    def test_rate_limit(self):
        @rate_limit(TEST_ENDPOINT, "app", requests=500, mins=15)
        def handle(self: ApiResources):
            return 1

        assert handle(api_resource_sync(DEFAULT_RATE_LIMIT_MANAGER)) == 1

    def test_rate_limit_when_error(self):
        @rate_limit(TEST_ENDPOINT, "app", requests=500, mins=15)
        def handle(self: ApiResources):
            raise ValueError()

        with pytest.raises(ValueError):
            handle(api_resource_sync(DEFAULT_RATE_LIMIT_MANAGER))

    def test_rate_limit_when_error_handle(self):
        @rate_limit(TEST_ENDPOINT, "app", requests=500, mins=15)
        def handle(self: ApiResources):
            raise ValueError()

        class IgnoreValueErrorRateLimitManager(RateLimitManager):
            def check_limit_over(
                self, rate_limit_info: RateLimitInfo, now: Optional[datetime] = None
            ) -> Optional[float]:
                return None

            @contextmanager
            def handle_rate_limit_sync(
                self, rate_limit_info: RateLimitInfo
            ) -> Generator[None, None, None]:
                try:
                    yield
                except ValueError:
                    pass

            @asynccontextmanager
            async def handle_rate_limit_async(
                self, rate_limit_info: RateLimitInfo
            ) -> AsyncGenerator[None, None]:
                try:
                    yield
                except ValueError:
                    pass

        assert handle(api_resource_sync(IgnoreValueErrorRateLimitManager())) is None

    def test_rate_limit_when_sometimes_error_handle_sync(self):
        result_iter = iter([ValueError(), ValueError(), 1])

        @rate_limit(TEST_ENDPOINT, "app", requests=500, mins=15)
        def handle(self: ApiResources):
            result = next(result_iter)
            if isinstance(result, ValueError):
                raise result
            else:
                return result

        assert handle(api_resource_sync(IgnoreValueErrorRateLimitManager())) == 1

    @pytest.mark.asyncio
    async def test_rate_limit_when_sometimes_error_handle_async(self):
        result_iter = iter([ValueError(), ValueError(), 1])

        @rate_limit(TEST_ENDPOINT, "app", requests=500, mins=15)
        async def handle(self: ApiResources):
            result = next(result_iter)
            if isinstance(result, ValueError):
                raise result
            else:
                return result

        assert await handle(api_resource_async(IgnoreValueErrorRateLimitManager())) == 1
