from twitter_api.rate_limit.rate_limit import rate_limit
from twitter_api.resources.api_resources import ApiResources
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.v2_scope import oauth2_scopes
from twitter_api.types.v2_tweet.tweet_id import TweetId

ENDPOINT = Endpoint("DELETE", "https://api.twitter.com/2/tweets/:id")


class DeleteV2TweetResponseBodyData(ExtraPermissiveModel):
    deleted: bool


class DeleteV2TweetResponseBody(ExtraPermissiveModel):
    data: DeleteV2TweetResponseBodyData


class DeleteV2TweetResources(ApiResources):
    @oauth2_scopes(
        "tweet.read",
        "tweet.write",
        "users.read",
    )
    @rate_limit(ENDPOINT, "user", requests=50, mins=15)
    def delete(
        self,
        id: TweetId,
    ) -> DeleteV2TweetResponseBody:
        """
        ツイートを削除する。

        refer: https://developer.twitter.com/en/docs/twitter-api/tweets/manage-tweets/api-reference/delete-tweets-id
        """
        return self.request_client.delete(
            endpoint=ENDPOINT,
            response_body_type=DeleteV2TweetResponseBody,
            url=ENDPOINT.url.replace(":id", id),
        )


class AsyncDeleteV2TweetResources(DeleteV2TweetResources):
    async def delete(
        self,
        id: TweetId,
    ) -> DeleteV2TweetResponseBody:
        return super().delete(id)
