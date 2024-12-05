from typing import Optional, override

from aiohttp import ClientSession
from pwpw_protocol.client.wallet import PwpwWalletClient
from pwpw_protocol.wallet import (
    WalletInitializationRequest,
    WalletInitializationResponse,
    WalletLockRequest,
    WalletLockResponse,
    WalletUnlockRequest,
    WalletUnlockResponse
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
        username: str,
        password: str
    ) -> WalletInitializationResponse:
        return await http_request(
            self._session,
            HttpMethod.POST,
            self._build_url("/initialize"),
            response_type=SimpleHttpResponseType(
                model_type=WalletInitializationResponse
            ),
            data=WalletInitializationRequest(
                username=username,
                password=password
            )
        )

    @override
    async def lock(self) -> WalletLockResponse:
        return await http_request(
            self._session,
            HttpMethod.POST,
            self._build_url("/lock"),
            response_type=SimpleHttpResponseType(
                model_type=WalletLockResponse
            ),
            data=WalletLockRequest()
        )

    @override
    async def unlock(self, password: str) -> WalletUnlockResponse:
        return await http_request(
            self._session,
            HttpMethod.POST,
            self._build_url("/unlock"),
            response_type=SimpleHttpResponseType(
                model_type=WalletUnlockResponse
            ),
            data=WalletUnlockRequest(password=password)
        )
