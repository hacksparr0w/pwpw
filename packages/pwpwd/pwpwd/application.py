from fastapi import FastAPI, Request, status
from fastapi.exceptions import (
    RequestValidationError as FastAPIRequestValidationError
)

from fastapi.responses import JSONResponse

from pwpw_protocol.error import (
    ApplicationError,
    RequestValidationError as PwpwRequestValidationError,
    RequestValidationErrorData,
    UnexpectedError
)

from .router import wallet_router


__all__ = (
    "application",
)


async def error_handler(request, on_next):
    try:
        return await on_next(request)
    except Exception as error:
        match error:
            case FastAPIRequestValidationError():
                return JSONResponse(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    content=PwpwRequestValidationError(
                        data=RequestValidationErrorData(
                            detail=error.errors()
                        )
                    ).dump()
                )
            case ApplicationError():
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content=error.dump()
                )
            case _:
                return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content=UnexpectedError().dump()
                )


application = FastAPI()
application.middleware("http")(error_handler)
application.include_router(wallet_router)


@application.exception_handler(FastAPIRequestValidationError)
def handle_request_validation_error(
    request: Request,
    error: FastAPIRequestValidationError
) -> None:
    raise error
