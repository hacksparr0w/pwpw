from solid import create_store

from .reducer import application_state_reducer
from .state import ApplicationState


__all__ = (
    "store",
)


store = create_store(
    application_state_reducer,
    ApplicationState.default()
)
