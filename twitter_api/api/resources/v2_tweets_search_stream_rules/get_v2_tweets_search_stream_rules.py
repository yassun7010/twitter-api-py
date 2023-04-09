from datetime import datetime
from typing import NotRequired, Optional, TypedDict

from pydantic import Field

from twitter_api.api.resources.api_resources import ApiResources
from twitter_api.api.types.v2_rule.rule import Rule
from twitter_api.api.types.v2_rule.rule_id import RuleId
from twitter_api.api.types.v2_scope import oauth2_scopes
from twitter_api.rate_limit.rate_limit_decorator import rate_limit
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.http import downcast_dict

ENDPOINT = Endpoint("GET", "https://api.twitter.com/2/tweets/search/stream/rules")

GetV2TweetsSearchStreamRulesQueryParameters = TypedDict(
    "GetV2TweetsSearchStreamRulesQueryParameters",
    {
        "ids": NotRequired[Optional[list[RuleId]]],
    },
)


class GetV2TweetsSearchStreamRulesResponseBodyMeta(ExtraPermissiveModel):
    sent: datetime


class GetV2TweetsSearchStreamRulesResponseBody(ExtraPermissiveModel):
    data: list[Rule] = Field(default_factory=list)
    meta: GetV2TweetsSearchStreamRulesResponseBodyMeta


class GetV2TweetsSearchStreamRulesResources(ApiResources):
    @rate_limit(ENDPOINT, "app", requests=450, mins=15)
    def get(
        self,
        query: Optional[GetV2TweetsSearchStreamRulesQueryParameters] = None,
    ) -> GetV2TweetsSearchStreamRulesResponseBody:
        # flake8: noqa E501
        """
        ツイートの一覧を検索するフィルターの一覧を取得する。

        refer: https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/api-reference/get-tweets-search-stream-rules
        """
        return self.request_client.post(
            endpoint=ENDPOINT,
            response_type=GetV2TweetsSearchStreamRulesResponseBody,
            query=downcast_dict(query),
        )