from typing import Sequence

from timecapsule import (
    Capsule,
    Challenge,
    PasswordChallenge,
    generate_random_password_challenge,
    lock_model as _lock_model
)

from locki.configuration import CryptographyConfiguration, build_cipher
from locki.csprng import generate_random_bytes
from locki.recovery_code import (
    generate_random_recovery_code as _generate_random_recovery_code
)


__all__ = (
    "generate_random_password_challenges",
    "generate_random_recovery_code",
    "generate_random_recovery_codes",
    "lock_model",
    "parse_recovery_code_index"
)


def generate_random_password_challenges(
    *,
    configuration: CryptographyConfiguration,
    password: bytes,
    recovery_codes: list[bytes],
    master_key: bytes
) -> list[PasswordChallenge]:
    password_challenge = generate_random_password_challenge(
        configuration=configuration,
        password=password,
        master_key=master_key
    )

    recovery_code_challenges = [
        generate_random_password_challenge(
            configuration=configuration,
            password=recovery_code,
            master_key=master_key
        )
        for recovery_code in recovery_codes
    ]

    return [password_challenge, *recovery_code_challenges]


def generate_random_recovery_code(
    *,
    configuration: CryptographyConfiguration,
    index: int
) -> bytes:
    base = _generate_random_recovery_code(
        segments=configuration.recovery_code.segments,
        segment_length=configuration.recovery_code.segment_length
    )

    base = base.decode()

    result = f"PW{index:03}-{base}"
    result = result.encode()

    return result


def generate_random_recovery_codes(
    *,
    configuration: CryptographyConfiguration,
    count: int
) -> list[bytes]:
    return [
        generate_random_recovery_code(
            configuration=configuration,
            index=index + 1
        )
        for index in range(count)
    ]


def lock_model[P](
    *,
    configuration: CryptographyConfiguration,
    challenges: Sequence[Challenge],
    master_key: bytes,
    model: object,
    public: P = None
) -> Capsule[P]:
    iv = generate_random_bytes(configuration.cipher.iv_length)
    cipher = build_cipher(
        configuration=configuration.cipher,
        iv=iv,
        ad=None
    )

    return _lock_model(
        cipher=cipher,
        challenges=challenges,
        master_key=master_key,
        model=model,
        public=public
    )


def parse_recovery_code_index(code: bytes) -> int:
    return int(code[2:5])
