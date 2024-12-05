from pathlib import Path

from locki.configuration import CryptographyConfiguration
from pwpw_protocol.wallet import WalletExistsError, WalletNotFoundError
from timecapsule import Capsule

from .cryptography import (
    initialize_wallet as _initialize_wallet,
    lock_wallet as _lock_wallet,
    unlock_wallet as _unlock_wallet
)

from .cryptography import WalletInitializationResult, WalletUnlockResult


__all__ = (
    "initialize_wallet",
    "unlock_wallet"
)


def initialize_wallet(
    configuration: CryptographyConfiguration,
    path: Path,
    username: str,
    password: str
) -> WalletInitializationResult:
    if path.exists():
        raise WalletExistsError

    result = _initialize_wallet(
        configuration=configuration,
        username=username,
        password=password
    )

    capsule = _lock_wallet(
        configuration=configuration,
        challenges=result.challenges,
        master_key=result.master_key,
        wallet=result.wallet
    )

    path.write_text(capsule.model_dump_json())

    return result


def unlock_wallet(path: Path, password: str) -> WalletUnlockResult:
    try:
        capsule = Capsule[None].model_validate_json(path.read_text())
    except FileNotFoundError as error:
        raise WalletNotFoundError from error

    result = _unlock_wallet(capsule=capsule, password=password)

    return result
