from .action import ApplicationAction, LockWalletAction, UnlockWalletAction
from .state import ApplicationState, lock_wallet, unlock_wallet


__all__ = (
    "application_state_reducer",
)


def application_state_reducer(
    state: ApplicationState,
    action: ApplicationAction
) -> ApplicationState:
    match action:
        case LockWalletAction():
            return lock_wallet(state)
        case UnlockWalletAction(master_key=master_key, wallet=wallet):
            return unlock_wallet(state, master_key, wallet)
        case _:
            raise NotImplementedError(
                f"'{type(action).__name__}' action not supported"
            )
