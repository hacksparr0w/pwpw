from abc import ABC, abstractmethod

from ..wallet import WalletInitializationResponse, WalletLockResponse


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
