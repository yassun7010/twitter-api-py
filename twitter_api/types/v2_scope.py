from typing import Callable, Literal

Scope = Literal[
    "block.read",
    "block.write",
    "bookmark.read",
    "bookmark.write",
    "dm.read",
    "dm.write",
    "follows.read",
    "follows.write",
    "like.read",
    "like.write",
    "list.read",
    "list.write",
    "mute.read",
    "mute.write",
    "offline.access",
    "space.read",
    "tweet.moderate.write",
    "tweet.read",
    "tweet.write",
    "users.read",
]
"""
OAuth2.0 で用いるスコープ。

Refer: https://developer.twitter.com/en/docs/authentication/oauth-2-0/authorization-code
"""

ALL_SCOPES: list[Scope] = [
    "block.read",
    "block.write",
    "bookmark.read",
    "bookmark.write",
    "dm.read",
    "dm.write",
    "follows.read",
    "follows.write",
    "like.read",
    "like.write",
    "list.read",
    "list.write",
    "mute.read",
    "mute.write",
    "offline.access",
    "space.read",
    "tweet.moderate.write",
    "tweet.read",
    "tweet.write",
    "users.read",
]


def oauth2_scopes(
    *scopes: Scope,
) -> Callable:
    """
    OAuth2 を用いた操作に必要なスコープを表す。

    Twitter の API ドキュメントを補完するメモとして用意されており、処理は何も行われない。
    """

    def _oauth2_scopes(func):
        def _wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return _wrapper

    return _oauth2_scopes
