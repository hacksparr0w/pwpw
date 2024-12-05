from abc import ABC, abstractmethod

from ..wallet import (
    WalletInitializationResponse,
    WalletLockResponse,
    WalletUnlockResponse
)


class PwpwWalletClient(ABC):
    @abstractmethod
    async def initialize(
        self,
        username: str,
        password: str
    ) -> WalletInitializationResponse:
        raise NotImplementedError

    @abstractmethod
    async def lock(self) -> WalletLockResponse:
        raise NotImplementedError

    @abstractmethod
    async def unlock(self, password: str) -> WalletUnlockResponse:
        raise NotImplementedError
