from datetime import datetime
from typing import Optional

from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.v2_poll.poll_id import PollId
from twitter_api.types.v2_poll.poll_option import PollOption


class Poll(ExtraPermissiveModel):
    """
    投票情報。

    refer: https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/poll
    """

    id: PollId
    options: list[PollOption]
    duration_minutes: Optional[datetime] = None
    end_datetime: Optional[datetime] = None
    voting_status: Optional[str] = None
