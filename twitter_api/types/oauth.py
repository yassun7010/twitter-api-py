"""
Twitter の OAuth 認証に必要な情報をまとめた型。

型を作るほどなのか難しい所であるが、同じことを指す用語がたくさん存在するため、
あえて型を作ることで説明文を用意している。

refer: https://developer.twitter.com/en/docs/authentication/oauth-1-0a/obtaining-user-access-tokens
"""

from typing import Annotated, Literal, TypeAlias, TypeVar

T = TypeVar("T", bound=str)

OAuthVersion = Literal["1.0a", "2.0"]

Env = Annotated[T, ...]
"""
環境変数名。
"""


ApiKey: TypeAlias = str
"""
アプリの認証に必要なキー。

同じことを指す用語として下記が存在する。

- App Key
- API Key
- Consumer API Key
- Consumer Key
- Customer Key
- oauth_consumer_key
"""

ApiSecret: TypeAlias = str
"""
アプリの認証に必要な秘密キー。

同じことを指す用語として下記が存在する。

- App Key Secret
- API Secret Key
- Consumer Secret
- Consumer Key
- Customer Key
- oauth_consumer_secret
"""

AccessToken: TypeAlias = str
"""
アクセスの認証に必要なキー。

同じことを指す用語として下記が存在する。

- Access token
- Token
- resulting
- oauth_token
"""

AccessSecret: TypeAlias = str
"""
アクセスの認証に必要な秘密キー。

同じことを指す用語として下記が存在する。

- Access secret
- Access token secret
- Token Secret
- resulting oauth_token_secret
"""

OAuthToken: TypeAlias = str
"""
OAuth 認証をするときに、一時的に発行されるトークン。

同じことを指す用語として下記が存在する。
- Request Token
- oauth_token
"""

OAuthTokenSecret: TypeAlias = str
"""
OAuth 認証をするときに、一時的に発行されるトークンの秘密キー。

同じことを指す用語として下記が存在する。
- Request Token Secret
- oauth_token_secret
"""

OauthVerifier: TypeAlias = str
"""
OAuth 認証をするときに、一時的に発行されるトークンを検証するキー。
"""


ClientId: TypeAlias = str
"""
OAuth2.0 で認証をするときに必要なID。
"""

ClientSecret: TypeAlias = str
"""
OAuth2.0 で認証をするときに必要な秘密キー。
"""

CallbackUrl: TypeAlias = str
"""
OAuth でユーザ認証をするときに必要なコールバック URL。
"""
