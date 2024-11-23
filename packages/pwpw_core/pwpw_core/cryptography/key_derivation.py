from enum import StrEnum, auto
from typing import Literal

import argon2

from argon2 import Argon2Variant, Argon2Version
from pwpw_common.types import b64bytes
from pydantic import BaseModel


__all__ = (
    "Argon2KeyDerivation",
    "KeyDerivation",
    "KeyDerivationType",

    "derive_key",
    "derive_key_argon2"
)


class KeyDerivationType(StrEnum):
    ARGON2 = auto()


class Argon2KeyDerivation(BaseModel):
    type: Literal[KeyDerivationType.ARGON2] = KeyDerivationType.ARGON2
    salt: b64bytes
    iterations: int
    memory: int
    parallelism: int
    length: int
    version: Argon2Version
    variant: Argon2Variant


type KeyDerivation = Argon2KeyDerivation


def derive_argon2_key(
    parameters: Argon2KeyDerivation,
    password: bytes
) -> bytes:
    return argon2.argon2(
        password=password,
        salt=parameters.salt,
        iterations=parameters.iterations,
        memory=parameters.memory,
        parallelism=parameters.parallelism,
        length=parameters.length,
        version=parameters.version,
        variant=parameters.variant
    )


def derive_key(
    parameters: KeyDerivation,
    password: bytes
) -> bytes:
    match parameters:
        case Argon2KeyDerivation():
            return derive_argon2_key(parameters, password)
        case _:
            raise NotImplementedError(
                f"'{type(parameters).__name__}' key derivation not supported"
            )
