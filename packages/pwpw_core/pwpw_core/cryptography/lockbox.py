from typing import Any

from pwpw_common.types import b64bytes
from pydantic import BaseModel, TypeAdapter

from .cipher import Cipher, decrypt, encrypt


__all__ = (
    "Lockbox",

    "lock_data",
    "lock_model",
    "unlock_data",
    "unlock_model"
)


class Lockbox(BaseModel):
    cipher: Cipher
    content: b64bytes


def lock_data(*, cipher: Cipher, key: bytes, data: bytes) -> Lockbox:
    content = encrypt(parameters=cipher, key=key, data=data)

    return Lockbox(
        cipher=cipher,
        content=content
    )


def lock_model[T](*, cipher: Cipher, key: bytes, model: T) -> Lockbox:
    data = TypeAdapter(Any).dump_json(model)

    return lock_data(cipher=cipher, key=key, data=data)


def unlock_data(*, lockbox: Lockbox, key: bytes) -> bytes:
    return decrypt(parameters=lockbox.cipher, key=key, data=lockbox.content)


def unlock_model[T](
    *,
    model_type: type[T],
    lockbox: Lockbox,
    key: bytes
) -> T:
    data = unlock_data(lockbox=lockbox, key=key)

    return TypeAdapter(model_type).validate_json(data)
