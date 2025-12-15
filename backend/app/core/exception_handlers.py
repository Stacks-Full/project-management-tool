from fastapi import Request
from fastapi.responses import JSONResponse
from app.services.exceptions import UserAlreadyExistsError
from starlette import status


async def user_exists_exception_handler(
    request: Request, exc: UserAlreadyExistsError  # exception object raised by service
) -> JSONResponse:
    """Handles UserAlreadyExistsError and returns a 400 Bad Request JSON response"""
    # Determine the HTTP status code
    http_status_code = status.HTTP_400_BAD_REQUEST

    # Construct the JSON response body
    response_body = {
        "status": "error",
        "code": http_status_code,
        "message": str(exc),
        "details": None,
    }

    # Return the JSONResponse object
    return JSONResponse(status_code=http_status_code, content=response_body)
