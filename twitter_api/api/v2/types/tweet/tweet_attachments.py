from typing import Optional

from twitter_api.types.extra_permissive_model import ExtraPermissiveModel

from ..media.media_key import MediaKey
from ..poll.poll_id import PollId


class TweetAttachments(ExtraPermissiveModel):
    poll_ids: Optional[list[PollId]]
    media_keys: Optional[list[MediaKey]]
