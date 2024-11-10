from . import prng


_RECOVERY_CODE_ALPHABET = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


__all__ = (
    "generate_random_recovery_code",
)


def _generate_random_recovery_code_segment(length: int) -> bytes:
    return bytes(
        prng.generate_random_choice(_RECOVERY_CODE_ALPHABET)
        for _ in range(length)
    )


def generate_random_recovery_code(
    segments: int = 5,
    segment_length: int = 5
) -> bytes:
    return b"-".join(
        _generate_random_recovery_code_segment(segment_length)
        for _ in range(segments)
    )
