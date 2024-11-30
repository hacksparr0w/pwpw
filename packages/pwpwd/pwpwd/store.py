from solid import create_store

from .state.model import ApplicationState
from .state.reducer import application_state_reducer


__all__ = (
    "store",
)


store = create_store(
    application_state_reducer,
    ApplicationState.default()
)
