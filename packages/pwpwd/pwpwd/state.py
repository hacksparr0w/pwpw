from pathlib import Path
from typing import Self, Union

from pwpw_core.cryptography.challenge import Challenge
from pwpw_core.wallet import Wallet
from pydantic import BaseModel


__all__ = (
    "ApplicationState",
    "InvalidStateError",
    "UnknownWalletState",
    "UnlockedWalletState",
    "WalletState",

    "lock_wallet",
    "unlock_wallet"
)


class InvalidStateError(Exception):
    pass


class UnknownWalletState(BaseModel):
    pass


class UnlockedWalletState(BaseModel):
    master_key: bytes
    challenges: list[Challenge]
    wallet: Wallet
    wallet_path: Path


type WalletState = Union[
    UnknownWalletState,
    UnlockedWalletState
]


class ApplicationState(BaseModel):
    wallet: WalletState

    @classmethod
    def default(cls) -> Self:
        return cls(
            wallet=UnknownWalletState()
        )


def lock_wallet(state: ApplicationState) -> ApplicationState:
    if not isinstance(state.wallet, UnlockedWalletState):
        raise InvalidStateError

    return state.model_copy(
        update={
            "wallet": UnknownWalletState()
        }
    )


def unlock_wallet(
    state: ApplicationState,
    master_key: bytes,
    challenges: list[Challenge],
    wallet: Wallet,
    wallet_path: Path
) -> ApplicationState:
    if not isinstance(state.wallet, UnknownWalletState):
        raise InvalidStateError

    return state.model_copy(
        update={
            "wallet": UnlockedWalletState(
                master_key=master_key,
                challenges=challenges,
                wallet=wallet,
                wallet_path=wallet_path
            )
        }
    )
