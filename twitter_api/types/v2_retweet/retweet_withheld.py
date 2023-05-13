from typing import Optional

from typing_extensions import Literal

from twitter_api.types.extra_permissive_model import ExtraPermissiveModel


class RetweetWithheld(ExtraPermissiveModel):
    """
    refer: https://help.twitter.com/en/rules-and-policies/tweet-withheld-by-country
    """

    country_codes: Optional[list[str]] = None
    scope: Optional[Literal["tweet", "user"]]
