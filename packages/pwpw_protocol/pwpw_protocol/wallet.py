from pydantic import BaseModel

from .error import ApplicationError


__all__ = (
    "WalletLockedError",
    "WalletNotFoundError",
    "WalletUnlockError",
    "WalletUnlockRequest",
    "WalletUnlockResponse"
)


class WalletDownloadRequest(BaseModel):
    url: str


class WalletDownloadResponse(BaseModel):
    pass


class WalletInitializationRequest(BaseModel):
    username: str
    password: bytes


class WalletInitializationResponse(BaseModel):
    recovery_codes: list[bytes]


class WalletNotFoundError(ApplicationError[None]):
    pass


class WalletLockedError(ApplicationError[None]):
    pass


class WalletUnlockError(ApplicationError[None]):
    pass


class WalletExistsError(ApplicationError[None]):
    pass


class WalletUnlockRequest(BaseModel):
    password: str


class WalletUnlockResponse(BaseModel):
    pass
