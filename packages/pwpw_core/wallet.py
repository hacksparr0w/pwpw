from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


__all__ = (
    "Wallet",
)


class User(BaseModel):
    username: str


class BasicAccessCredentials(BaseModel):
    type: Literal["basic_access"] = "basic_access"
    url: str
    username: str
    password: str


type StorageItem = BasicAccessCredentials


Storage = list[StorageItem]


class Wallet(BaseModel):
    user: User
    storage: Storage
