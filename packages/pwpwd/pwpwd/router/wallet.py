from fastapi import APIRouter

from pwpw_protocol.wallet import (
    WalletInitializationRequest,
    WalletInitializationResponse,
    WalletLockRequest,
    WalletLockResponse,
    WalletUnlockRequest,
    WalletUnlockResponse
)

from ..controller.wallet import (
    initialize_wallet as _initialize_wallet,
    lock_wallet as _lock_wallet,
    unlock_wallet as _unlock_wallet
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


@router.post("/unlock")
async def unlock_wallet(request: WalletUnlockRequest) -> WalletUnlockResponse:
    return await _unlock_wallet(request)
