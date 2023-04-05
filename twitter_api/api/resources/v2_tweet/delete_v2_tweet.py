from twitter_api.api.resources.api_resources import ApiResources
from twitter_api.api.types.v2_tweet.tweet_id import TweetId
from twitter_api.rate_limit.rate_limit_decorator import rate_limit
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel

ENDPOINT = Endpoint("DELETE", "https://api.twitter.com/2/tweets/:id")


class V2DeleteTweetResponseBodyData(ExtraPermissiveModel):
    deleted: bool


class V2DeleteTweetResponseBody(ExtraPermissiveModel):
    data: V2DeleteTweetResponseBodyData


class V2DeleteTweetResources(ApiResources):
    @rate_limit(ENDPOINT, "user", requests=50, mins=15)
    def delete(
        self,
        id: TweetId,
    ) -> V2DeleteTweetResponseBody:
        # flake8: noqa E501
        """
        ツイートを削除する。

        refer: https://developer.twitter.com/en/docs/twitter-api/tweets/manage-tweets/api-reference/delete-tweets-id
        """
        return self.request_client.delete(
            endpoint=ENDPOINT,
            response_type=V2DeleteTweetResponseBody,
            url=ENDPOINT.url.replace(":id", id),
        )
