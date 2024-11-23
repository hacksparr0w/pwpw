from typing import Literal, Optional, Self

from argon2 import Argon2Variant, Argon2Version
from pydantic import BaseModel

from .cipher import AesGcmCipher, Cipher, CipherType
from .key_derivation import (
    Argon2KeyDerivation,
    KeyDerivation,
    KeyDerivationType
)


__all__ = (
    "AesGcmCipherConfiguration",
    "Argon2KeyDerivationConfiguration",
    "CipherConfiguration",
    "CryptographyConfiguration",
    "KeyDerivationConfiguration",
    "RecoveryCodeConfiguration",

    "build_aes_gcm_cipher",
    "build_argon2_key_derivation",
    "build_cipher",
    "build_key_derivation"
)


class AesGcmCipherConfiguration(BaseModel):
    type: Literal[CipherType.AES_GCM] = CipherType.AES_GCM
    key_length: int
    iv_length: int


type CipherConfiguration = AesGcmCipherConfiguration


class Argon2KeyDerivationConfiguration(BaseModel):
    type: Literal[KeyDerivationType.ARGON2] = KeyDerivationType.ARGON2
    salt_length: int
    hash_length: int
    iterations: int
    memory: int
    parallelism: int
    version: Argon2Version
    variant: Argon2Variant


type KeyDerivationConfiguration = Argon2KeyDerivationConfiguration


class RecoveryCodeConfiguration(BaseModel):
    segments: int
    segment_length: int


class CryptographyConfiguration(BaseModel):
    cipher: CipherConfiguration
    key_derivation: KeyDerivationConfiguration
    recovery_code: RecoveryCodeConfiguration

    @classmethod
    def default(cls) -> Self:
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
                parallelism=4,
                version=Argon2Version.V13,
                variant=Argon2Variant.D
            ),
            recovery_code=RecoveryCodeConfiguration(
                segments=5,
                segment_length=5
            )
        )


def build_aes_gcm_cipher(
    *,
    configuration: AesGcmCipherConfiguration,
    iv: bytes,
    ad: Optional[bytes] = None
) -> AesGcmCipher:
    return AesGcmCipher(iv=iv, ad=ad)


def build_cipher(*, configuration: CipherConfiguration, **kwargs) -> Cipher:
    match configuration:
        case AesGcmCipherConfiguration():
            return build_aes_gcm_cipher(configuration=configuration, **kwargs)
        case _:
            raise NotImplementedError(
                f"'{type(configuration).__name__}' configuration not "
                "supported"
            )


def build_argon2_key_derivation(
    *,
    configuration: Argon2KeyDerivationConfiguration,
    salt: bytes
) -> Argon2KeyDerivation:
    return Argon2KeyDerivation(
        salt=salt,
        iterations=configuration.iterations,
        memory=configuration.memory,
        parallelism=configuration.parallelism,
        length=configuration.hash_length,
        version=configuration.version,
        variant=configuration.variant
    )


def build_key_derivation(
    *,
    configuration: KeyDerivationConfiguration,
    **kwargs
) -> KeyDerivation:
    match configuration:
        case Argon2KeyDerivationConfiguration():
            return build_argon2_key_derivation(
                configuration=configuration,
                **kwargs
            )
        case _:
            raise NotImplementedError(
                f"'{type(configuration).__name__}' configuration not "
                "supported"
            )
