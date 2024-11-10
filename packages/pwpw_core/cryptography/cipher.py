from enum import StrEnum, auto
from typing import Literal, Optional

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from pydantic import BaseModel


__all__ = (
    "AesGcmCipher",
    "Cipher",
    "CipherOperation",
    "CipherType",

    "cipher",
    "cipher_aes_gcm",
    "decrypt",
    "encrypt",
    "get_cipher_class"
)


class CipherOperation(StrEnum):
    ENCRYPT = auto()
    DECRYPT = auto()


class CipherType(StrEnum):
    AES_GCM = auto()


class AesGcmCipher(BaseModel):
    type: Literal[CipherType.AES_GCM] = CipherType.AES_GCM
    ad: Optional[bytes]
    iv: bytes


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
    if parameters.type == CipherType.AES_GCM:
        return cipher_aes_gcm(
            parameters=parameters,
            operation=operation,
            key=key,
            data=data
        )

    raise NotImplementedError(f"'{parameters.type}' cipher not supported")


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


def get_cipher_class(cipher_type: CipherType) -> type[Cipher]:
    if cipher_type == CipherType.AES_GCM:
        return AesGcmCipher

    raise NotImplementedError(f"'{cipher_type}' cipher not supported")
