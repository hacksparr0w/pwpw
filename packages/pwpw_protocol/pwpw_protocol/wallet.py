from typing import Sequence

from pydantic import BaseModel

from .error import ApplicationError


__all__ = (
    "WalletDownloadRequest",
    "WalletDownloadResponse",
    "WalletExistsError",
    "WalletInitializationRequest",
    "WalletInitializationResponse",
    "WalletInaccessibleError",
    "WalletLockRequest",
    "WalletLockResponse",
    "WalletNotFoundError",
    "WalletUnlockedError",
    "WalletUnlockError",
    "WalletUnlockRequest",
    "WalletUnlockResponse"
)


class WalletDownloadRequest(BaseModel):
    url: str


class WalletDownloadResponse(BaseModel):
    pass


class WalletExistsError(ApplicationError[None]):
    pass


class WalletInitializationRequest(BaseModel):
    username: str
    password: str


class WalletInitializationResponse(BaseModel):
    recovery_codes: Sequence[str]


class WalletInaccessibleError(ApplicationError[None]):
    pass


class WalletLockRequest(BaseModel):
    pass


class WalletLockResponse(BaseModel):
    pass


class WalletNotFoundError(ApplicationError[None]):
    pass


class WalletUnlockError(ApplicationError[None]):
    pass


class WalletUnlockedError(ApplicationError[None]):
    pass


class WalletUnlockRequest(BaseModel):
    password: str


class WalletUnlockResponse(BaseModel):
    pass
