from pathlib import Path
from typing import Sequence, Union

from pydantic import BaseModel
from timecapsule import Challenge

from ..wallet.model import Wallet


__all__ = (
    "ApplicationAction",
    "LockWalletAction",
    "UnlockWalletAction"
)


class LockWalletAction(BaseModel):
    pass


class UnlockWalletAction(BaseModel):
    master_key: bytes
    challenges: Sequence[Challenge]
    wallet: Wallet
    path: Path


ApplicationAction = Union[
    LockWalletAction,
    UnlockWalletAction
]
