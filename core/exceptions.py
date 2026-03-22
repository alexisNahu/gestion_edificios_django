from fastapi import HTTPException

# Base
class ApiError(HTTPException):
    def __init__(self, message: str, status_code: int):
        super().__init__(status_code=status_code, detail=message)

# Errores cliente
class BadRequestError(ApiError):
    def __init__(self, message='BAD_REQUEST'):
        super().__init__(message, 400)

class UnauthorizedError(ApiError):
    def __init__(self, message='UNAUTHORIZED'):
        super().__init__(message, 401)

class ForbiddenError(ApiError):
    def __init__(self, message='FORBIDDEN'):
        super().__init__(message, 403)

class NotFoundError(ApiError):
    def __init__(self, message='NOT_FOUND'):
        super().__init__(message, 404)

class ConflictError(ApiError):
    def __init__(self, message='CONFLICT'):
        super().__init__(message, 409)

class UnprocessableEntityError(ApiError):
    def __init__(self, message='UNPROCESSABLE_ENTITY'):
        super().__init__(message, 422)

# Errores servidor
class InternalServerError(ApiError):
    def __init__(self, message='INTERNAL_SERVER_ERROR'):
        super().__init__(message, 500)

# Handle error
def handle_error(e: Exception):
    print(e)
    if hasattr(e, 'status_code') and e.status_code < 500:
        raise e
    raise InternalServerError()