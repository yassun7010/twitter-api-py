import sys

from twitter_api.api.types.v2_oauth2.twitter_oauth2_access_token_client import (
    TwitterOAuth2AccessTokenClient,
)
from twitter_api.api.types.v2_scope import SCOPES
from twitter_api.client import TwitterApiClient
from twitter_api.error import TwitterApiError

YOUR_CALLBACK_URL = "https://127.0.0.1:3000/"

try:
    # Backend: 認証用の URL を作成します。
    backend = (
        TwitterApiClient.from_oauth2_user_flow_env(
            callback_url=YOUR_CALLBACK_URL,
            scope=SCOPES,
        )
        .request("https://twitter.com/i/oauth2/authorize")
        .generate_authorization_url()
    )

    # ユーザに認証ページへの URL を返却します。
    user = backend

    # Frontend: ユーザは承認ボタンを押した後、リダイレクトした CallbackURL をバックエンドに返します。
    user = user.open_request_url().input_response_url()

    # Backend: アクセストークンを取得し、 Twitter API のクライアントを作成します。
    access_token = (
        TwitterOAuth2AccessTokenClient.from_authorization_response_url_env(
            callback_url=YOUR_CALLBACK_URL,
            authorization_response_url=user.authorization_response_url,
            code_verifier=backend.code_verifier,
            state=backend.state,
        )
        .request("https://api.twitter.com/2/oauth2/token")
        .post()
        .access_token
    )

    print(f"\nGet Access Token: {access_token}\n")

    client = TwitterApiClient.from_oauth2_bearer_token(access_token)

    # Twitter API を呼ぶことができるようになりました。
    tweet = (
        client.chain()
        .request("https://api.twitter.com/2/tweets/:id")
        .get("1460323737035677698")
        .data
    )

    print(tweet)


except TwitterApiError as error:
    print(error, file=sys.stderr)
