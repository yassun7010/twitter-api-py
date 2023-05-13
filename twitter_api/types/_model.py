from typing import TYPE_CHECKING, AbstractSet, Any, Callable, Mapping, Optional, Union

from pydantic import BaseModel

if TYPE_CHECKING:
    IntStr = Union[int, str]
    AbstractSetIntStr = AbstractSet[IntStr]
    MappingIntStrAny = Mapping[IntStr, Any]


class Model(BaseModel):
    def dict(
        self,
        *,
        include: Optional[Union["AbstractSetIntStr", "MappingIntStrAny"]] = None,
        exclude: Optional[Union["AbstractSetIntStr", "MappingIntStrAny"]] = None,
        by_alias: bool = False,
        skip_defaults: Optional[bool] = None,
        exclude_unset: bool = True,
        exclude_defaults: bool = False,
        exclude_none: bool = True,
    ) -> dict:
        """
        pydantic のデフォルトとは異なり、exclude_unset と exclude_none を
        デフォルトで有効にしている。
        """

        return super().dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )

    def json(
        self,
        *,
        include: Optional[Union["AbstractSetIntStr", "MappingIntStrAny"]] = None,
        exclude: Optional[Union["AbstractSetIntStr", "MappingIntStrAny"]] = None,
        by_alias: bool = False,
        skip_defaults: Optional[bool] = None,
        exclude_unset: bool = True,
        exclude_defaults: bool = False,
        exclude_none: bool = True,
        encoder: Optional[Callable[[Any], Any]] = None,
        models_as_dict: bool = True,
        ensure_ascii=False,
        **dumps_kwargs: Any,
    ) -> str:
        """
        pydantic のデフォルトとは異なり、
        exclude_unset と exclude_none をデフォルトで有効にしている。
        また、ensure_ascii を無効にしている。
        """

        return super().json(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            encoder=encoder,
            models_as_dict=models_as_dict,
            ensure_ascii=ensure_ascii,
            **dumps_kwargs,
        )
