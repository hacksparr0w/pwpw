from enum import StrEnum, auto
from typing import Annotated, Literal, Self, Union

import argon2

from argon2 import Argon2Variant, Argon2Version
from pydantic import BaseModel, Field, field_validator


class CipherType(StrEnum):
    AES_GCM = auto()


class AesGcmCipher(BaseModel):
    type: Literal[CipherType.AES_GCM] = CipherType.AES_GCM
    iv: bytes
    size: int = 256


Cipher = AesGcmCipher


class Secret(BaseModel):
    cipher: Cipher
    content: bytes


class KeyDerivationType(StrEnum):
    ARGON2 = auto()


class Argon2KeyDerivation(BaseModel):
    type: Literal[KeyDerivationType.ARGON2] = KeyDerivationType.ARGON2
    salt: bytes
    iterations: int = 16
    memory: int = 8 * 1024 ** 2
    parallelism: int = 4
    length: int = 32
    version: Argon2Version = Argon2Version.V13
    variant: Argon2Variant = Argon2Variant.D


type KeyDerivation = Argon2KeyDerivation


class ChallengeType(StrEnum):
    KEY = auto()
    PASSWORD = auto()


class KeyChallenge(BaseModel):
    type: Literal[ChallengeType.KEY] = ChallengeType.KEY
    key: Secret


class PasswordChallenge(BaseModel):
    type: Literal[ChallengeType.PASSWORD] = ChallengeType.PASSWORD
    key_derivation: KeyDerivation
    key: Secret


type Challenge = Annotated[
    Union[
        KeyChallenge,
        PasswordChallenge
    ],
    Field(discriminator="type")
]


class Vault(Secret):
    challenges: list[Challenge]

    def get_primary_challenge(self) -> Challenge:
        return self.challenges[0]

    def get_secondary_challenge(self, index: int) -> Challenge:
        return self.challenges[1:][index]

    @field_validator("challenges")
    @classmethod
    def validate_challenges(cls, challenges):
        if not challenges:
            raise ValueError("At least one challenge must be present")

        return challenges


def derive_key(password: bytes, parameters: KeyDerivation) -> bytes:
    type = parameters.type

    parameters = dict(parameters)
    parameters.pop("type")

    if type == KeyDerivationType.ARGON2:
        return argon2.argon2(password=password, **parameters)

    raise NotImplementedError(
        f"Key derivation type '{parameters.type}' is not supported"
    )


def encrypt(key: bytes, iv: bytes, data: bytes) -> bytes:
    pass


def decrypt(key: bytes, iv: bytes, data: bytes) -> bytes:
    pass
