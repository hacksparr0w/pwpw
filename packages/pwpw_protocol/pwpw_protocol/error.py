from typing import (
    Any,
    ClassVar,
    Optional,
    Self,
    get_args as get_generic_args,
    get_origin as get_generic_origin
)

from pwpw_common.collection import find
from pydantic import BaseModel, TypeAdapter


__all__ = (
    "ApplicationError",
    "RequestValidationErrorData",
    "RequestValidationError",
    "UnexpectedError"
)


def _find_origin_base(cls: type[Any], hint: type[Any]) -> Any:
    for base in cls.__orig_bases__:
        if get_generic_origin(base) is hint:
            return base

    return None


class ApplicationError[T](Exception):
    __children__: ClassVar[set[type[Any]]] = set()

    data: T

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        base = _find_origin_base(cls, ApplicationError)

        if base is None:
            raise TypeError("Missing generic argument for ApplicationError")

        cls.__children__.add(cls)

    def __init__(self, *, data: Optional[T] = None) -> None:
        super().__init__()

        base = _find_origin_base(self.__class__, ApplicationError)
        hint = get_generic_args(base)[0]

        if not isinstance(data, hint):
            raise TypeError(
                f"'data' must be of type '{hint.__name__}', got "
                f"'{data.__class__.__name__}'"
            )

        self.data = data

    def dump(self) -> dict[str, Any]:
        return {
            "error": self.__class__.__name__,
            "data": TypeAdapter(Any).dump_python(self.data)
        }

    @classmethod
    def validate(cls, data: bytes) -> Self:
        name = data["error"]

        child = find(
            lambda x: x.__name__ == name,
            cls.__children__,
            error_factory=lambda: ValueError(f"Unknown error type '{name}'")
        )

        base = _find_origin_base(child, ApplicationError)
        hint = get_generic_args(base)[0]

        data = data["data"]
        data = TypeAdapter(hint).validate_json(data)

        return child(data=data)


class RequestValidationErrorData(BaseModel):
    detail: list[Any]


class RequestValidationError(ApplicationError[RequestValidationErrorData]):
    data: RequestValidationErrorData


class UnexpectedError(ApplicationError[None]):
    pass
