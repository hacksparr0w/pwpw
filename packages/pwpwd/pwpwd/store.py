from solid import create_store

from .state import ApplicationState, application_state_reducer


__all__ = (
    "store",
)


store = create_store(
    application_state_reducer,
    ApplicationState.default()
)
