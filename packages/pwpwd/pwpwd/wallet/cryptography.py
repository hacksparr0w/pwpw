from typing import Sequence

from timecapsule import (
    Capsule,
    Challenge,
    PasswordChallenge,
    generate_random_password_challenge,
    lock_model,
    solve_password_challenge,
    unlock_model
)

from locki.configuration import CryptographyConfiguration, build_cipher
from locki.csprng import generate_random_bytes
from locki.recovery_code import generate_random_recovery_code

from pydantic import BaseModel

from .model import Wallet


__all__ = (
    "WalletInitializationResult",
    "WalletUnlockResult",

    "initialize_wallet",
    "lock_wallet",
    "unlock_wallet"
)


class WalletUnlockResult(BaseModel):
    master_key: bytes
    challenges: Sequence[Challenge]
    wallet: Wallet


class WalletInitializationResult(WalletUnlockResult):
    recovery_codes: Sequence[str]


def _generate_random_password_challenges(
    *,
    configuration: CryptographyConfiguration,
    password: str,
    recovery_codes: Sequence[str],
    master_key: bytes
) -> list[PasswordChallenge]:
    password_challenge = generate_random_password_challenge(
        configuration=configuration,
        password=password.encode(),
        master_key=master_key
    )

    recovery_code_challenges = [
        generate_random_password_challenge(
            configuration=configuration,
            password=recovery_code.encode(),
            master_key=master_key
        )
        for recovery_code in recovery_codes
    ]

    return [password_challenge, *recovery_code_challenges]


def _generate_random_recovery_code(
    *,
    configuration: CryptographyConfiguration,
    index: int
) -> str:
    base = generate_random_recovery_code(
        segments=configuration.recovery_code.segments,
        segment_length=configuration.recovery_code.segment_length
    )

    return f"PW{index:03}-{base}"


def _generate_random_recovery_codes(
    *,
    configuration: CryptographyConfiguration,
    count: int
) -> list[str]:
    return [
        _generate_random_recovery_code(
            configuration=configuration,
            index=index + 1
        )
        for index in range(count)
    ]


def _parse_recovery_code_index(code: str) -> int:
    return int(code[2:5])


def initialize_wallet(
    *,
    configuration: CryptographyConfiguration,
    username: str,
    password: str
) -> WalletInitializationResult:
    master_key = generate_random_bytes(configuration.cipher.key_length)

    recovery_codes = _generate_random_recovery_codes(
        configuration=configuration,
        count=3
    )

    challenges = _generate_random_password_challenges(
        configuration=configuration,
        password=password,
        recovery_codes=recovery_codes,
        master_key=master_key
    )

    wallet = Wallet.empty(username)

    return WalletInitializationResult(
        master_key=master_key,
        recovery_codes=recovery_codes,
        challenges=challenges,
        wallet=wallet
    )


def lock_wallet(
    *,
    configuration: CryptographyConfiguration,
    challenges: Sequence[Challenge],
    master_key: bytes,
    wallet: Wallet
) -> Capsule[None]:
    iv = generate_random_bytes(configuration.cipher.iv_length)
    cipher = build_cipher(
        configuration=configuration.cipher,
        iv=iv,
        ad=None
    )

    return lock_model(
        cipher=cipher,
        challenges=challenges,
        master_key=master_key,
        model=wallet
    )


def unlock_wallet(
    *,
    capsule: Capsule[None],
    password: str
) -> WalletUnlockResult:
    challenges = capsule.challenges
    challenge = challenges[0]

    if not isinstance(challenge, PasswordChallenge):
        raise ValueError("Invalid challenge type")

    master_key = solve_password_challenge(
        challenge=challenge,
        password=password.encode()
    )

    wallet = unlock_model(
        model_type=Wallet,
        capsule=capsule,
        master_key=master_key
    )

    return WalletUnlockResult(
        master_key=master_key,
        challenges=challenges,
        wallet=wallet
    )
