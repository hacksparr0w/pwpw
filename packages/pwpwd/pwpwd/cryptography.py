from pwpw_core.cryptography.challenge import (
    Challenge,
    create_password_challenge
)

from pwpw_core.cryptography.configuration import (
    build_cipher,
    build_key_derivation
)

from pwpw_core.cryptography.csprng import generate_random_bytes
from pwpw_core.cryptography.recovery_code import (
    generate_random_recovery_code as _generate_random_recovery_code
)

from pwpw_core.cryptography.vault import (
    Vault,
    lock_model as _lock_model
)

from .configuration import configuration


__all__ = (
    "generate_random_password_challenge",
    "generate_random_password_challenges",
    "generate_random_recovery_code",
    "generate_random_recovery_codes",
    "lock_model",
    "parse_recovery_code_index"
)


def generate_random_password_challenge(
    *,
    password: bytes,
    master_key: bytes
) -> Challenge:
    iv = generate_random_bytes(configuration.cryptography.cipher.iv_length)
    cipher = build_cipher(
        configuration=configuration.cryptography.cipher,
        iv=iv,
        ad=None
    )

    salt = generate_random_bytes(
        configuration.cryptography.key_derivation.salt_length
    )

    encryption_key_derivation = build_key_derivation(
        configuration=configuration.cryptography.key_derivation,
        salt=salt
    )

    return create_password_challenge(
        cipher=cipher,
        encryption_key_derivation=encryption_key_derivation,
        password=password,
        master_key=master_key
    )


def generate_random_password_challenges(
    *,
    password: bytes,
    recovery_codes: list[bytes],
    master_key: bytes
) -> list[Challenge]:
    password_challenge = generate_random_password_challenge(
        password=password,
        master_key=master_key
    )

    recovery_code_challenges = [
        generate_random_password_challenge(
            password=recovery_code,
            master_key=master_key
        )
        for recovery_code in recovery_codes
    ]

    return [password_challenge, *recovery_code_challenges]


def generate_random_recovery_code(index: int) -> bytes:
    base = _generate_random_recovery_code(
        **dict(configuration.cryptography.recovery_code)
    ).decode()

    return f"PW{index:03}-{base}".encode()


def generate_random_recovery_codes(count: int = 3) -> list[bytes]:
    return [generate_random_recovery_code(index) for index in range(count)]


def lock_model[T](
    *,
    challenges: list[Challenge],
    master_key: bytes,
    model: T
) -> Vault:
    iv = generate_random_bytes(configuration.cryptography.cipher.iv_length)
    cipher = build_cipher(
        configuration=configuration.cryptography.cipher,
        iv=iv,
        ad=None
    )

    return _lock_model(
        cipher=cipher,
        challenges=challenges,
        master_key=master_key,
        model=model
    )


def parse_recovery_code_index(code: bytes) -> int:
    return int(code[2:5])
