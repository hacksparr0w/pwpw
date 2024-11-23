from abc import ABC, abstractmethod

from ..wallet import (
    WalletInitializationRequest,
    WalletInitializationResponse
)


class PwpwWalletClient(ABC):
    @abstractmethod
    async def initialize(
        self,
        request: WalletInitializationRequest
    ) -> WalletInitializationResponse:
        raise NotImplementedError
