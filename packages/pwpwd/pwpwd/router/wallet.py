from fastapi import APIRouter

from pwpw_protocol.wallet import (
    WalletInitializationRequest,
    WalletInitializationResponse
)

from ..action import UnlockWalletAction
from ..core.wallet import initialize_wallet as _initialize_wallet
from ..store import store


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
    result = _initialize_wallet(request.username, request.password)

    action = UnlockWalletAction(
        master_key=result.master_key,
        challenges=result.challenges,
        wallet=result.wallet,
        wallet_path=result.wallet_path
    )

    response = WalletInitializationResponse(
        recovery_codes=result.recovery_codes
    )

    store.action.on_next(action)

    return response
