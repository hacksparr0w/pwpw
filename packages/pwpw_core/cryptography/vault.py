from .challenge import Challenge, solve_challenge
from .cipher import Cipher
from .lockbox import (
    Lockbox,
    lock_data as _lock_data,
    lock_model as _lock_model,
    unlock_data as _unlock_data,
    unlock_model as _unlock_model
)

from pydantic import conlist


__all__ = (
    "Vault",

    "lock_data",
    "lock_model",
    "unlock_data",
    "unlock_model"
)


class Vault(Lockbox):
    challenges: conlist(Challenge, min_items=1)


def lock_data(
    *,
    cipher: Cipher,
    challenges: list[Challenge],
    master_key: bytes,
    data: bytes
) -> Vault:
    lockbox = _lock_data(cipher=cipher, key=master_key, data=data)

    return Vault(
        **dict(lockbox),
        challenges=challenges
    )


def lock_model[T](
    *,
    cipher: Cipher,
    challenges: list[Challenge],
    master_key: bytes,
    model: T
) -> Vault:
    lockbox = _lock_model(cipher=cipher, key=master_key, model=model)

    return Vault(
        **dict(lockbox),
        challenges=challenges
    )


def unlock_data(
    *,
    vault: Vault,
    challenge: Challenge,
    secret: bytes
) -> bytes:
    master_key = solve_challenge(challenge=challenge, secret=secret)

    return _unlock_data(
        lockbox=vault,
        key=master_key
    )


def unlock_model[T](
    *,
    model_type: type[T],
    vault: Vault,
    challenge: Challenge,
    secret: bytes
) -> T:
    master_key = solve_challenge(challenge=challenge, secret=secret)

    return _unlock_model(
        model_type=model_type,
        lockbox=vault,
        key=master_key
    )
