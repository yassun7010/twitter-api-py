from twitter_api.types.extra_permissive_model import ExtraPermissiveModel


class TestHasExtraFields:
    def test_get_extra_fields(self):
        class A(ExtraPermissiveModel):
            a: int
            b: str

        assert A.model_validate({"a": 1, "b": "b"}).model_extra == {}
        assert A.model_validate({"a": 1, "b": "b", "c": 2}).model_extra != {}

    def test_get_extra_fields_deep(self):
        class A(ExtraPermissiveModel):
            c: int
            d: str

        class B(ExtraPermissiveModel):
            a: A
            b: str

        assert (
            B.model_validate(
                {
                    "a": {"c": 1, "d": "d"},
                    "b": "b",
                }
            ).model_extra
            == {}
        )

        assert (
            B.model_validate(
                {
                    "a": {"c": 1, "d": "d"},
                    "b": "b",
                    "e": 2,
                }
            ).model_extra
            != {}
        )

        assert (
            B.model_validate(
                {
                    "a": {"c": 1, "d": "d", "e": 2},
                    "b": "b",
                }
            ).model_extra
            != {}
        )
