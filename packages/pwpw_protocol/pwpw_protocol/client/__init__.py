from .wallet import PwpwWalletClient


__all__ = (
    "PwpwClient",
    "PwpwWalletClient"
)


class PwpwClient:
    wallet: PwpwWalletClient
