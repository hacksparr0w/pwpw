from types import TracebackType
from typing import Optional, Self

from aiohttp import ClientSession

from pwpw_protocol.client import PwpwClient
from pwpw_protocol.server import get_pwpw_server_url

from .wallet import PwpwWalletHttpClient


__all__ = (
    "PwpwHttpClient",
    "PwpwWalletHttpClient"
)


class PwpwHttpClient(PwpwClient):
    def __init__(self):
        self._session = ClientSession(base_url=get_pwpw_server_url())

        self.wallet = PwpwWalletHttpClient(self._session)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        error_type: Optional[type[BaseException]] = None,
        error_value: Optional[BaseException] = None,
        error_traceback: Optional[TracebackType] = None
    ) -> None:
        await self._session.close()
