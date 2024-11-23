from typing import Callable, Iterable


type ErrorFactory = Callable[[], Exception]
type Predicate[T] = Callable[[T], bool]


__all__ = (
    "ErrorFactory",
    "Predicate",

    "find"
)


def find[T](
    predicate: Predicate[T],
    items: Iterable[T],
    error_factory: ErrorFactory = LookupError
) -> T:
    for item in items:
        if predicate(item):
            return item

    raise error_factory()
