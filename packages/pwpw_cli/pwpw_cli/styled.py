import click


__all__ = (
    "default",
    "error",
    "info"
)


def default(message):
    return click.style(message, fg="white")


def info(message):
    return click.style(message, fg="cyan")


def error(message):
    return click.style(message, fg="red")
