from twitter_api.api.resources.oauth_authenticate import OauthAuthenticateUrl
from twitter_api.api.resources.oauth_authorize import OauthAuthorizeUrl

OAuth1RequestUrl = OauthAuthenticateUrl | OauthAuthorizeUrl
