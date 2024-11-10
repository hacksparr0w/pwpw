from typing import Literal, Self

from .cipher import CipherType
from .key_derivation import KeyDerivationType


__all__ = (
    "AesGcmCipherConfiguration",
    "Argon2KeyDerivationConfiguration",
    "CipherConfiguration",
    "CryptographyConfiguration",
    "KeyDerivationConfiguration"
)


class AesGcmCipherConfiguration:
    type: Literal[CipherType.AES_GCM] = CipherType.AES_GCM
    key_length: int
    iv_length: int


type CipherConfiguration = AesGcmCipherConfiguration


class Argon2KeyDerivationConfiguration:
    type: Literal[KeyDerivationType.ARGON2] = KeyDerivationType.ARGON2
    salt_length: int
    hash_length: int
    iterations: int
    memory: int
    parallelism: int


type KeyDerivationConfiguration = Argon2KeyDerivationConfiguration


class CryptographyConfiguration:
    cipher: CipherConfiguration
    key_derivation: KeyDerivationConfiguration

    @classmethod
    def default(cls: type[Self]) -> Self:
        return cls(
            cipher=AesGcmCipherConfiguration(
                key_length=32,
                iv_length=12
            ),
            key_derivation=Argon2KeyDerivationConfiguration(
                salt_length=32,
                hash_length=32,
                iterations=8,
                memory=8 * 1024 ** 2,
                parallelism=4
            )
        )
