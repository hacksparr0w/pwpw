from pathlib import Path
from typing import Sequence

from locki.configuration import CryptographyConfiguration
from locki.csprng import generate_random_bytes
from timecapsule import Challenge
from pwpw_protocol.wallet import WalletExistsError
from pydantic import BaseModel

from .cryptography import (
    generate_random_password_challenges,
    generate_random_recovery_codes,
    lock_model
)

from .base import Wallet


__all__ = (
    "WalletInitializationResult",

    "initialize_wallet"
)


class WalletInitializationResult(BaseModel):
    master_key: bytes
    recovery_codes: Sequence[str]
    challenges: Sequence[Challenge]
    wallet: Wallet


def initialize_wallet(
    configuration: CryptographyConfiguration,
    path: Path,
    username: str,
    password: str
) -> WalletInitializationResult:
    if path.exists():
        raise WalletExistsError

    master_key = generate_random_bytes(configuration.cipher.key_length)

    recovery_codes = generate_random_recovery_codes(
        configuration=configuration,
        count=3
    )

    challenges = generate_random_password_challenges(
        configuration=configuration,
        password=password,
        recovery_codes=recovery_codes,
        master_key=master_key
    )

    wallet = Wallet.empty(username)
    capsule = lock_model(
        configuration=configuration,
        challenges=challenges,
        master_key=master_key,
        model=wallet
    )

    path.write_text(capsule.model_dump_json())

    result = WalletInitializationResult(
        master_key=master_key,
        recovery_codes=recovery_codes,
        challenges=challenges,
        wallet=wallet
    )

    return result
