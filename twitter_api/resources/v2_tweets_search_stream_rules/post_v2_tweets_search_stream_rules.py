from datetime import datetime
from typing import NotRequired, Optional, TypedDict, Union

from pydantic import Field

from twitter_api.rate_limit.rate_limit import rate_limit
from twitter_api.resources.api_resources import ApiResources
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.http import downcast_dict
from twitter_api.types.v2_rule.rule import Rule
from twitter_api.types.v2_rule.rule_id import RuleId
from twitter_api.types.v2_rule.rule_tag import RuleTag

ENDPOINT = Endpoint("POST", "https://api.twitter.com/2/tweets/search/stream/rules")

PostV2TweetsSearchStreamRulesQueryParameters = TypedDict(
    "PostV2TweetsSearchStreamRulesQueryParameters",
    {
        "dry_run": NotRequired[Optional[bool]],
    },
)


class AddData(TypedDict):
    value: str
    tag: NotRequired[Optional[RuleTag]]


class DeleteDataByIds(TypedDict):
    ids: list[RuleId]


class DeleteDataByValues(TypedDict):
    values: list[str]


DeleteData = Union[DeleteDataByIds, DeleteDataByValues]


class PostV2TweetsSearchStreamRulesRequestBody(TypedDict):
    add: NotRequired[list[AddData]]
    delete: NotRequired[Optional[DeleteData]]


class PostV2TweetsSearchStreamRulesResponseBodyMetaSummary(ExtraPermissiveModel):
    created: Optional[int] = None
    not_created: Optional[int] = None
    deleted: Optional[int] = None
    not_deleted: Optional[int] = None
    invalid: Optional[int] = None
    valid: Optional[int] = None


class PostV2TweetsSearchStreamRulesResponseBodyMeta(ExtraPermissiveModel):
    sent: datetime
    summary: PostV2TweetsSearchStreamRulesResponseBodyMetaSummary


class PostV2TweetsSearchStreamRulesResponseBody(ExtraPermissiveModel):
    data: list[Rule] = Field(default_factory=list)
    meta: PostV2TweetsSearchStreamRulesResponseBodyMeta
    errors: Optional[list[dict]] = None


class PostV2TweetsSearchStreamRulesResources(ApiResources):
    @rate_limit(ENDPOINT, "app", requests=450, mins=15)
    def post(
        self,
        request_body: PostV2TweetsSearchStreamRulesRequestBody,
        query: Optional[PostV2TweetsSearchStreamRulesQueryParameters] = None,
    ) -> PostV2TweetsSearchStreamRulesResponseBody:
        """
        ツイートの一覧を検索するフィルターを作成する。

        refer: https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/api-reference/post-tweets-search-stream-rules
        """
        return self.request_client.post(
            endpoint=ENDPOINT,
            response_body_type=PostV2TweetsSearchStreamRulesResponseBody,
            query=downcast_dict(query),
            body=downcast_dict(request_body),
        )


class AsyncPostV2TweetsSearchStreamRulesResources(
    PostV2TweetsSearchStreamRulesResources
):
    async def post(
        self,
        request_body: PostV2TweetsSearchStreamRulesRequestBody,
        query: Optional[PostV2TweetsSearchStreamRulesQueryParameters] = None,
    ) -> PostV2TweetsSearchStreamRulesResponseBody:
        return super().post(request_body, query)
