from argon2 import Argon2Variant, Argon2Version
from locki.configuration import (
    AesGcmCipherConfiguration,
    Argon2KeyDerivationConfiguration,
    CryptographyConfiguration,
    RecoveryCodeConfiguration
)

from pydantic import BaseModel


class ApplicationConfiguration(BaseModel):
    cryptography: CryptographyConfiguration


configuration = ApplicationConfiguration(
    cryptography=CryptographyConfiguration(
        cipher=AesGcmCipherConfiguration(
            key_length=32,
            iv_length=12
        ),
        key_derivation=Argon2KeyDerivationConfiguration(
            salt_length=16,
            hash_length=32,
            iterations=2,
            memory=1024,
            parallelism=2,
            version=Argon2Version.V13,
            variant=Argon2Variant.D
        ),
        recovery_code=RecoveryCodeConfiguration(
            segments=5,
            segment_length=5
        )
    )
)
