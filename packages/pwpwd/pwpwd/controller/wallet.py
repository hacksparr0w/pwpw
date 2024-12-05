from pwpw_protocol.wallet import (
    WalletInitializationRequest,
    WalletInitializationResponse,
    WalletLockRequest,
    WalletLockResponse,
    WalletUnlockedError,
    WalletUnlockRequest,
    WalletUnlockResponse,
    WalletInaccessibleError
)

from ..configuration import configuration
from ..home import get_wallet_path, initialize_home_directory
from ..wallet.operation import (
    initialize_wallet as _initialize_wallet,
    unlock_wallet as _unlock_wallet
)

from ..state.model import UnknownWalletState, UnlockedWalletState
from ..state.action import LockWalletAction, UnlockWalletAction
from ..store import store


async def initialize_wallet(
    request: WalletInitializationRequest
) -> WalletInitializationResponse:
    state = store.state.value

    if not isinstance(state.wallet, UnknownWalletState):
        raise WalletUnlockedError

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


async def lock_wallet(request: WalletLockRequest) -> WalletLockResponse:
    state = store.state.value

    if not isinstance(state.wallet, UnlockedWalletState):
        raise WalletInaccessibleError

    store.action.on_next(LockWalletAction())

    return WalletLockResponse()


async def unlock_wallet(request: WalletUnlockRequest) -> WalletUnlockResponse:
    state = store.state.value

    if not isinstance(state.wallet, UnknownWalletState):
        raise WalletUnlockedError
 
    path = get_wallet_path()
    result = _unlock_wallet(path, request.password)

    action = UnlockWalletAction(
        master_key=result.master_key,
        challenges=result.challenges,
        wallet=result.wallet,
        path=path
    )

    store.action.on_next(action)

    return WalletUnlockResponse()
