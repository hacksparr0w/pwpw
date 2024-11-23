from pathlib import Path

from pwpw_core.cryptography.challenge import Challenge
from pwpw_core.cryptography.csprng import generate_random_bytes
from pwpw_core.cryptography.vault import lock_model
from pwpw_core.wallet import Wallet
from pwpw_protocol.wallet import WalletExistsError
from pydantic import BaseModel

from ..configuration import configuration
from ..cryptography import (
    generate_random_password_challenges,
    generate_random_recovery_codes,
    lock_model
)

from ..home import get_wallet_path, initialize_home_directory


__all__ = (
    "WalletInitializationResult",

    "initialize_wallet"
)


class WalletInitializationResult(BaseModel):
    master_key: bytes
    recovery_codes: list[str]
    challenges: list[Challenge]
    wallet: Wallet
    wallet_path: Path


def initialize_wallet(
    username: str,
    password: str
) -> WalletInitializationResult:
    initialize_home_directory()
    wallet_path = get_wallet_path()

    if wallet_path.exists():
        raise WalletExistsError

    master_key = generate_random_bytes(
        configuration.cryptography.cipher.key_length
    )

    recovery_codes = generate_random_recovery_codes()
    challenges = generate_random_password_challenges(
        password=password,
        recovery_codes=recovery_codes,
        master_key=master_key
    )

    wallet = Wallet.empty(username)
    vault = lock_model(
        challenges=challenges,
        master_key=master_key,
        model=wallet
    )

    wallet_path.write_text(vault.model_dump_json())

    result = WalletInitializationResult(
        master_key=master_key,
        recovery_codes=recovery_codes,
        challenges=challenges,
        wallet=wallet,
        wallet_path=wallet_path
    )

    return result
