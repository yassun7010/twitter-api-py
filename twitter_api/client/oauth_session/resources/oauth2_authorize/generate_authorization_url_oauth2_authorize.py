from twitter_api.client.oauth_session.resources.session_resources import (
    OAuth2SessionResources,
)


class GenerateAuthorizationUrlOAuth2AuthorizeSessionResources(OAuth2SessionResources):
    def generate_authorization_url(self):
        return self._session.generate_authorization_url()
