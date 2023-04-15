from twitter_api.types.extra_permissive_model import ExtraPermissiveModel


class PollOption(ExtraPermissiveModel):
    position: int
    label: str
    votes: int
