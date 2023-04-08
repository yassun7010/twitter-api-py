from typing_extensions import Literal

from .get_oauth2_authorize import GetOauth2AuthorizeResources

Oauth2AuthorizeUrl = Literal["https://twitter.com/i/oauth2/authorize"]


class Oauth2AuthorizeResources(GetOauth2AuthorizeResources):
    pass
