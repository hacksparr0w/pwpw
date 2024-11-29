from pathlib import Path
from typing import Self, Sequence, Union

from pydantic import BaseModel
from timecapsule import Challenge

from .wallet.base import Wallet


__all__ = (
    "ApplicationAction",
    "ApplicationState",
    "InvalidStateError",
    "LockWalletAction",
    "UnknownWalletState",
    "UnlockedWalletState",
    "UnlockWalletAction",
    "WalletState",

    "application_state_reducer",
    "lock_wallet",
    "unlock_wallet"
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


class InvalidStateError(Exception):
    pass


class UnknownWalletState(BaseModel):
    pass


class UnlockedWalletState(BaseModel):
    master_key: bytes
    challenges: Sequence[Challenge]
    wallet: Wallet
    path: Path


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
    challenges: Sequence[Challenge],
    wallet: Wallet,
    path: Path
) -> ApplicationState:
    if not isinstance(state.wallet, UnknownWalletState):
        raise InvalidStateError

    return state.model_copy(
        update={
            "wallet": UnlockedWalletState(
                master_key=master_key,
                challenges=challenges,
                wallet=wallet,
                path=path
            )
        }
    )


def application_state_reducer(
    state: ApplicationState,
    action: ApplicationAction
) -> ApplicationState:
    match action:
        case LockWalletAction():
            return lock_wallet(state)
        case UnlockWalletAction(
            master_key=master_key,
            challenges=challenges,
            wallet=wallet,
            path=path
        ):
            return unlock_wallet(state, master_key, challenges, wallet, path)
        case _:
            raise NotImplementedError(
                f"'{type(action).__name__}' action not supported"
            )
