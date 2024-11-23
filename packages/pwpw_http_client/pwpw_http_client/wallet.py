from typing import Optional, override

from aiohttp import ClientSession
from pwpw_protocol.client.wallet import PwpwWalletClient
from pwpw_protocol.wallet import (
    WalletInitializeRequest,
    WalletInitializeResponse
)

from pydantic import BaseModel

from ._http import (
    HttpMethod,
    HttpResponseType,
    SimpleHttpResponseType,

    http_request
)


__all__ = (
    "PwpwWalletHttpClient",
)


class PwpwWalletHttpClient(PwpwWalletClient):
    def __init__(self, session: ClientSession) -> None:
        self._session = session

    def _build_url(self, path: str) -> str:
        return "/wallet" + path

    async def _http_request[T: BaseModel](
        self,
        method: HttpMethod,
        path: str,
        *,
        response_type: HttpResponseType[T],
        data: Optional[BaseModel] = None
    ) -> T:
        return await http_request(
            self._session,
            method,
            self._build_url(path),
            response_type=response_type,
            data=data
        )

    @override
    async def initialize(
        self,
        request: WalletInitializeRequest
    ) -> WalletInitializeResponse:
        return await http_request(
            HttpMethod.POST,
            "/wallet/initialize",
            response_type=SimpleHttpResponseType(WalletInitializeResponse),
            data=request
        )