import sys

import click

from pwpw_http_client import PwpwHttpClient
from pwpw_protocol.wallet import WalletExistsError

from . import styled
from .asyncly import asyncly


@click.group()
def cli():
    pass


@cli.group()
def wallet():
    pass


@wallet.command("init")
@click.option(
    "--username",
    prompt=styled.info("Username")
)
@click.option(
    "--password",
    prompt=styled.info("Password"),
    hide_input=True,
    confirmation_prompt=styled.info("Confirm password")
)
@asyncly
async def initialize_wallet(username: str, password: str):
    click.echo()

    try:
        async with PwpwHttpClient() as client:
            result = await client.wallet.initialize(username, password)
    except WalletExistsError:
        click.echo(styled.error("Wallet already exists"))
        sys.exit(1)

    click.echo(
        styled.info(
            "Wallet initialized successfully, "
            "following are your recovery codes:"
        )
    )

    click.echo()

    for recovery_code in result.recovery_codes:
        click.echo(styled.default(f"    - {recovery_code}"))

    click.echo()
    click.prompt(
        styled.info(
            "Store your recovery codes in a safe place, then continue by "
            "pressing [Enter] to clear the screen."
        ),
        default="",
        prompt_suffix="",
        show_default=False
    )

    click.clear()
