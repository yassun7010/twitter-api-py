import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.contexts.spawn_real_client import spawn_real_client
from twitter_api.error import UnsupportedAuthenticationError


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestSpawnRealClient:
    def test_spawn_real_client_is_success_when_permit(
        self,
        request: pytest.FixtureRequest,
    ):
        with spawn_real_client(
            "oauth2_app_real_client",
            request,
            permit=True,
        ) as _:
            pass

    def test_spawn_real_client_is_failed_when_permit(
        self,
        request: pytest.FixtureRequest,
    ):
        with pytest.raises(ValueError):
            with spawn_real_client(
                "oauth2_app_real_client",
                request,
                permit=True,
            ) as _:
                raise ValueError()

    def test_spawn_real_client_is_success_when_non_permit(
        self,
        request: pytest.FixtureRequest,
    ):
        with pytest.raises(UnsupportedAuthenticationError):
            with spawn_real_client(
                "oauth2_app_real_client", request, permit=False
            ) as _:
                pass

    def test_spawn_real_client_is_failed_when_non_permit(
        self,
        request: pytest.FixtureRequest,
    ):
        with pytest.raises(ValueError):
            with spawn_real_client(
                "oauth2_app_real_client", request, permit=False
            ) as _:
                raise ValueError()
