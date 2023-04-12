from contextlib import contextmanager

import pytest

from tests.contexts.check_oauth2_user_access_token import check_oauth2_user_access_token
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient
from twitter_api.error import (
    TwitterApiErrorCode,
    TwitterApiResponseFailed,
    UnsupportedAuthenticationError,
)


@contextmanager
def spawn_real_client(
    client_fixture_name: str,
    request: pytest.FixtureRequest,
    permit: bool,
):
    """
    実際のクライアントを Fixture から作成する。
    """
    with check_oauth2_user_access_token():
        real_client: TwitterApiRealClient = request.getfixturevalue(client_fixture_name)

        try:
            yield real_client

        except TwitterApiResponseFailed as error:
            # API が許可していないと考えている認証方法で認証エラーが出た場合のみ、例外を無視する。
            if not permit and error.status_code == TwitterApiErrorCode.Forbidden.value:
                pass
            else:
                raise error
        except Exception as error:
            # 認証以外のエラーはそのまま投げる。
            raise error
        else:
            # 認証が許可されていないはずなのに API を呼べたら例外を投げる。
            if not permit:
                raise UnsupportedAuthenticationError()
