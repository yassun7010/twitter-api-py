from twitter_api.types.extra_permissive_model import (
    ExtraPermissiveModel,
    get_extra_fields,
)


class TestHasExtraFields:
    def test_get_extra_fields(self):
        class A(ExtraPermissiveModel):
            a: int
            b: str

        assert get_extra_fields(A.parse_obj({"a": 1, "b": "b"})) == {}
        assert get_extra_fields(A.parse_obj({"a": 1, "b": "b", "c": 2})) != {}

    def test_get_extra_fields_deep(self):
        class A(ExtraPermissiveModel):
            c: int
            d: str

        class B(ExtraPermissiveModel):
            a: A
            b: str

        assert (
            get_extra_fields(
                B.parse_obj(
                    {
                        "a": {"c": 1, "d": "d"},
                        "b": "b",
                    }
                )
            )
            == {}
        )

        assert (
            get_extra_fields(
                B.parse_obj(
                    {
                        "a": {"c": 1, "d": "d"},
                        "b": "b",
                        "e": 2,
                    }
                )
            )
            != {}
        )

        assert (
            get_extra_fields(
                B.parse_obj(
                    {
                        "a": {"c": 1, "d": "d", "e": 2},
                        "b": "b",
                    }
                )
            )
            != {}
        )
