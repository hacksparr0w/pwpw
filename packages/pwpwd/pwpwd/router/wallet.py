from fastapi import APIRouter

from pwpw_protocol.wallet import (
    WalletInitializationRequest,
    WalletInitializationResponse
)

from ..action import UnlockWalletAction
from ..configuration import configuration
from ..home import get_wallet_path, initialize_home_directory
from ..wallet.common import initialize_wallet as _initialize_wallet
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
    initialize_home_directory()

    path = get_wallet_path()
    result = _initialize_wallet(
        configuration.cryptography,
        path,
        request.username,
        request.password
    )

    action = UnlockWalletAction(
        master_key=result.master_key,
        challenges=result.challenges,
        wallet=result.wallet,
        path=path
    )

    response = WalletInitializationResponse(
        recovery_codes=result.recovery_codes
    )

    store.action.on_next(action)

    return response
