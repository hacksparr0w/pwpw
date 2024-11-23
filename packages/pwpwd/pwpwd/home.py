from pathlib import Path


__all__ = (
    "get_home_directory",
    "get_wallet_path",
    "initialize_home_directory"
)


def get_home_directory() -> Path:
    return Path.home() / ".pwpw"


def get_wallet_path() -> Path:
    return get_home_directory() / "wallet.json"


def initialize_home_directory() -> Path:
    directory = get_home_directory()
    directory.mkdir(exist_ok=True)

    return directory
