from typing import Literal

Scope = Literal[
    "block.read",
    "block.write",
    "bookmark.read",
    "bookmark.write",
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

SCOPES: list[Scope] = [
    "block.read",
    "block.write",
    "bookmark.read",
    "bookmark.write",
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
