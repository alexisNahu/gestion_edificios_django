from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from core.exceptions import ApiError

def register_exception_handlers(app: FastAPI):
    """
    Registra todos los manejadores de excepciones globales para la aplicación.
    """

    @app.exception_handler(ApiError)
    async def api_error_handler(request: Request, exc: ApiError):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "msg": exc.detail,
                "status_code": exc.status_code,
                "success": False
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "msg": "Error de validación",
                "details": exc.errors(),
                "status_code": 422,
                "success": False
            },
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        # Este captura errores no controlados (IndexError, AttributeError, etc.)
        return JSONResponse(
            status_code=500,
            content={
                "msg": "Error interno del servidor",
                "details": str(exc),
                "status_code": 500,
                "success": False
            },
        )