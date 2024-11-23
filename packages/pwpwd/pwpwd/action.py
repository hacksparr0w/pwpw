from pathlib import Path
from typing import Union

from pwpw_core.cryptography.challenge import Challenge
from pwpw_core.wallet import Wallet
from pydantic import BaseModel


__all__ = (
    "ApplicationAction",
    "LockWalletAction",
    "UnlockWalletAction"
)


class LockWalletAction(BaseModel):
    pass


class UnlockWalletAction(BaseModel):
    master_key: bytes
    challenges: list[Challenge]
    wallet: Wallet
    wallet_path: Path


ApplicationAction = Union[
    LockWalletAction,
    UnlockWalletAction
]
