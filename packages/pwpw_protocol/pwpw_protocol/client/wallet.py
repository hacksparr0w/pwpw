from abc import ABC, abstractmethod

from ..wallet import WalletInitializationResponse


class PwpwWalletClient(ABC):
    @abstractmethod
    async def initialize(
        self,
        username: str,
        password: str
    ) -> WalletInitializationResponse:
        raise NotImplementedError
