from datetime import datetime
from typing import Optional

from twitter_api.types.extra_permissive_model import ExtraPermissiveModel


class TweetEditControls(ExtraPermissiveModel):
    edits_remaining: Optional[int] = None
    is_edit_eligible: Optional[bool] = None
    editable_until: Optional[datetime] = None
