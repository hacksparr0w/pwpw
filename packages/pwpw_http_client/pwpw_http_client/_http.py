from enum import StrEnum
from typing import Optional

from aiohttp import ClientResponse, ClientSession
from pwpw_protocol.error import ApplicationError
from pydantic import BaseModel


__all__ = (
    "HttpMethod",
    "HttpResponseType",
    "SimpleHttpResponseType",

    "http_request"
)


class HttpMethod(StrEnum):
    GET = "GET"
    PATCH = "PATCH"
    POST = "POST"
    PUT = "PUT"


class SimpleHttpResponseType[T: BaseModel](BaseModel):
    model_type: type[T]


type HttpResponseType[T: BaseModel] = SimpleHttpResponseType[T]


def _is_http_response_ok(response: ClientResponse) -> bool:
    return (response.status // 100) not in (4, 5)


async def http_request[T: BaseModel](
    session: ClientSession,
    method: HttpMethod,
    url: str,
    *,
    response_type: HttpResponseType[T],
    data: Optional[BaseModel] = None
) -> T:
    request_data = data

    response = await session.request(
        method.value,
        url,
        json=request_data.model_dump() if request_data else None
    )

    if not _is_http_response_ok(response):
        response_data = await response.json()
        response.close()

        error = ApplicationError.validate(response_data)

        raise error

    if isinstance(response_type, SimpleHttpResponseType):
        response_data = await response.read()
        response.close()

        result = response_type.model_type.model_validate_json(response_data)

        return result

    raise NotImplementedError
