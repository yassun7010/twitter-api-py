from contextlib import contextmanager

from twitter_api.error import (
    OAuth2UserAccessTokenExpired,
    TwitterApiErrorCode,
    TwitterApiResponseFailed,
)


@contextmanager
def check_oauth2_user_access_token():
    """
    OAuth 2.0 のユーザ認証が失効することで自動テストが失敗することがある。

    ユーザ認証が失効することによってエラーが発生していることが分かるようにエラーを上書きする。
    """

    try:
        yield
    except TwitterApiResponseFailed as error:
        if error.status_code == TwitterApiErrorCode.Forbidden:
            raise OAuth2UserAccessTokenExpired()
        else:
            raise error
