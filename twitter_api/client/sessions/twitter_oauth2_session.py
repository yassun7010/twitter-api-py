from abc import ABCMeta, abstractmethod

from twitter_api.api.types.v2_oauth2.oauth2_access_token import OAuth2AcccessToken
from twitter_api.types.oauth import CallbackUrl


class TwitterOAuth2Session(metaclass=ABCMeta):
    @abstractmethod
    def generate_authorization_url(self):
        from twitter_api.api.types.v2_oauth2.oauth2_authorization import (
            OAuth2Authorization,
        )

        return OAuth2Authorization(
            authorization_url="dummy",
            state="dummy",
            code_verifier="dummy",
            _session=self,
        )

    @abstractmethod
    def fetch_token(
        self,
        authorization_response_url: CallbackUrl,
        state: str,
        code_verifier: str,
    ) -> OAuth2AcccessToken:
        ...
