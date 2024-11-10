import secrets

from typing import Iterable


__all__ = (
    "generate_random_bytes",
    "generate_random_choice"
)


def generate_random_bytes(length: int) -> bytes:
    return secrets.token_bytes(length)


def generate_random_choice[T](items: Iterable[T]) -> T:
    return secrets.choice(items)
