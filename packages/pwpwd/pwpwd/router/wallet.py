from fastapi import APIRouter

from pwpw_protocol.wallet import (
    WalletInitializationRequest,
    WalletInitializationResponse,
    WalletLockRequest,
    WalletLockResponse
)

from ..controller.wallet import (
    initialize_wallet as _initialize_wallet,
    lock_wallet as _lock_wallet
)


__all__ = (
    "router",
)


router = APIRouter(
    prefix="/wallet",
    tags=["wallet"]
)


@router.post("/initialize")
async def initialize_wallet(
    request: WalletInitializationRequest
) -> WalletInitializationResponse:
    return await _initialize_wallet(request)


@router.post("/lock")
async def lock_wallet(request: WalletLockRequest) -> WalletLockResponse:
    return await _lock_wallet(request)
