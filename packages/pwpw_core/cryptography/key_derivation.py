import base64

from enum import StrEnum, auto
from typing import Annotated, Literal

import argon2

from argon2 import Argon2Variant, Argon2Version
from pydantic import BaseModel, PlainSerializer, PlainValidator


__all__ = (
    "Argon2KeyDerivation",
    "KeyDerivation",
    "KeyDerivationType",

    "derive_key",
    "derive_key_argon2",
    "get_key_derivation_class"
)


class KeyDerivationType(StrEnum):
    ARGON2 = auto()


class Argon2KeyDerivation(BaseModel):
    type: Literal[KeyDerivationType.ARGON2] = KeyDerivationType.ARGON2
    salt: Annotated[
        bytes,
        PlainValidator(base64.b64decode),
        PlainSerializer(base64.b64encode)
    ]

    iterations: int
    memory: int
    parallelism: int
    length: int
    version: Argon2Version
    variant: Argon2Variant


type KeyDerivation = Argon2KeyDerivation


def derive_key_argon2(
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
    if parameters.type == KeyDerivationType.ARGON2:
        return derive_key_argon2(parameters, password)

    raise NotImplementedError(
        f"'{parameters.type}' key derivation not supported"
    )


def get_key_derivation_class(
    key_derivation_type: KeyDerivationType
) -> type[KeyDerivation]:
    if key_derivation_type == KeyDerivationType.ARGON2:
        return Argon2KeyDerivation

    raise NotImplementedError(
        f"'{key_derivation_type}' key derivation not supported"
    )
