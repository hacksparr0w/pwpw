from __future__ import annotations

from enum import StrEnum, auto
from typing import Literal, Self

from pydantic import BaseModel


__all__ = (
    "BasicAccessCredentials",
    "Wallet",
    "WalletStorage",
    "WalletStorageEntry",
    "WalletStorageEntryType",
    "WalletUser"
)


class WalletUser(BaseModel):
    username: str


class WalletStorageEntryType(StrEnum):
    BASIC_ACCESS_CREDENTIALS = auto()


class BasicAccessCredentials(BaseModel):
    type: Literal[WalletStorageEntryType.BASIC_ACCESS_CREDENTIALS] = \
        WalletStorageEntryType.BASIC_ACCESS_CREDENTIALS

    url: str
    username: str
    password: str


type WalletStorageEntry = BasicAccessCredentials


WalletStorage = list[WalletStorageEntry]


class Wallet(BaseModel):
    user: WalletUser
    storage: WalletStorage

    @classmethod
    def empty(cls, username: str) -> Self:
        return cls(
            user=WalletUser(
                username=username
            ),
            storage=[]
        )
