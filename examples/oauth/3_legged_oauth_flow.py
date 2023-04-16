import os
import sys
from textwrap import dedent

from twitter_api.api.types.oauth1.twitter_oauth1_access_token_client import (
    TwitterOAuth1AccessTokenClient,
)
from twitter_api.client import TwitterApiClient
from twitter_api.error import TwitterApiError

YOUR_CALLBACK_URL = os.environ["CALLBACK_URL"]


try:
    # Backend: 認証用の URL を作成します。
    backend = (
        TwitterApiClient.from_oauth1_user_flow_env()
        .request("https://api.twitter.com/oauth/request_token")
        .post()
        .request("https://api.twitter.com/oauth/authorize")
        .generate_authorization_url()
    )

    # ユーザに認証ページへの URL を返却します。
    user = backend

    # Frontend: ユーザは承認ボタンを押した後、リダイレクトした CallbackURL をバックエンドに返します。
    user = user.print_request_url().input_response_url()

    token = (
        TwitterOAuth1AccessTokenClient.from_authorization_response_url_env(
            callback_url=YOUR_CALLBACK_URL,
            authorization_response_url=user.authorization_response_url,
        )
        .request("https://api.twitter.com/oauth/access_token")
        .post()
    )

    print(
        dedent(
            f"""
            Get Access Token: {token.oauth_token}
            Get Access Secret: {token.oauth_token_secret}
            """
        )
    )

    client = token.generate_client()

    tweets = (
        client.chain()
        .request("https://api.twitter.com/2/tweets")
        .get(
            {"ids": ["1460323737035677698"]},
        )
        .data
    )

except TwitterApiError as error:
    print(error, file=sys.stderr)
