import base64
from typing import Literal, TypedDict

from twitter_api.api.resources.api_resources import ApiResources
from twitter_api.api.types.v2_scope import Scope
from twitter_api.types.comma_separatable import CommaSeparatable, comma_separated_str
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.http import Url
from twitter_api.types.oauth import AccessToken, ClientId

ENDPOINT: Endpoint = Endpoint("POST", "https://twitter.com/i/oauth2/authorize")


class GetOauth2AuthorizeQueryParameters(TypedDict):
    response_type: Literal["code"]
    client_id: ClientId
    redirect_uri: Url
    scope: CommaSeparatable[Scope]
    state: str
    code_challenge: str
    code_challenge_method: Literal["S256", "plain"]


def _make_query(query: GetOauth2AuthorizeQueryParameters) -> dict:
    return {
        "response_type": comma_separated_str(query["response_type"]),
        "client_id": query["client_id"],
        "redirect_uri": query["redirect_uri"],
        "scope": query["scope"],
        "state": query["state"],
        "code_challenge": query["code_challenge"],
        "code_challenge_method": query["code_challenge_method"],
    }


class GetOauth2AuthorizeResponseBody(ExtraPermissiveModel):
    token_type: Literal["bearer"]
    expires_in: int
    access_token: AccessToken
    scope: list[Scope]
    expores_at: int


class GetOauth2AuthorizeResources(ApiResources):
    def get(
        self,
        query: GetOauth2AuthorizeQueryParameters,
    ) -> GetOauth2AuthorizeResponseBody:
        # flake8: noqa E501
        """
        OAuth 2.0 のアプリ用のアクセストークンのセットを生成するために使用する。

        refer: https://developer.twitter.com/en/docs/authentication/api-reference/token
        """

        return self.request_client.post(
            endpoint=ENDPOINT,
            response_type=GetOauth2AuthorizeResponseBody,
            auth=False,
            headers={
                "Authorization": f"Basic ",
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            },
            query=_make_query(query),
        )
