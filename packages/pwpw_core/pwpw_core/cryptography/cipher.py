from enum import StrEnum, auto
from typing import Literal, Optional

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from pwpw_common.types import b64bytes
from pydantic import BaseModel


__all__ = (
    "AesGcmCipher",
    "Cipher",
    "CipherOperation",
    "CipherType",

    "cipher",
    "cipher_aes_gcm",
    "decrypt",
    "encrypt"
)


class CipherOperation(StrEnum):
    ENCRYPT = auto()
    DECRYPT = auto()


class CipherType(StrEnum):
    AES_GCM = auto()


class AesGcmCipher(BaseModel):
    type: Literal[CipherType.AES_GCM] = CipherType.AES_GCM
    iv: b64bytes
    ad: Optional[b64bytes]


type Cipher = AesGcmCipher


def cipher_aes_gcm(
    *,
    parameters: AesGcmCipher,
    operation: CipherOperation,
    key: bytes,
    data: bytes
) -> bytes:
    aes = AESGCM(key)
    nonce = parameters.iv
    associated_data = parameters.ad
    function = aes.encrypt if operation == CipherOperation.ENCRYPT \
        else aes.decrypt

    return function(nonce=nonce, data=data, associated_data=associated_data)


def cipher(
    *,
    parameters: Cipher,
    operation: CipherOperation,
    key: bytes,
    data: bytes
) -> bytes:
    match parameters:
        case AesGcmCipher():
            return cipher_aes_gcm(
                parameters=parameters,
                operation=operation,
                key=key,
                data=data
            )
        case _:
            raise NotImplementedError(
                f"'{type(parameters).__name__}' cipher not supported"
            )


def decrypt(*, parameters: Cipher, key: bytes, data: bytes) -> bytes:
    return cipher(
        parameters=parameters,
        operation=CipherOperation.DECRYPT,
        key=key,
        data=data
    )


def encrypt(*, parameters: Cipher, key: bytes, data: bytes) -> bytes:
    return cipher(
        parameters=parameters,
        operation=CipherOperation.ENCRYPT,
        key=key,
        data=data
    )
