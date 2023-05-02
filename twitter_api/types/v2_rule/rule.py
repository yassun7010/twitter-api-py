from typing import Optional

from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.v2_rule.rule_id import RuleId
from twitter_api.types.v2_rule.rule_tag import RuleTag


class Rule(ExtraPermissiveModel):
    id: RuleId
    value: str
    tag: Optional[RuleTag] = None
