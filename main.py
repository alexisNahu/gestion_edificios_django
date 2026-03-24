from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from core.exceptions import ApiError
from core.setup_django import init_django

init_django()

from fastapi import FastAPI, Request

from apps.edificios.edificios.controller import edificios_router
from apps.edificios.departamentos.controller import departamentos_router
from apps.authentication.controller import router as authentication_router
from apps.inquilinos.inquilinos.controller import inquilinos_router
from apps.contratos.contratos.controller import contratos_router

app = FastAPI()

@app.exception_handler(ApiError)
async def api_error_handler(request: Request, exc: ApiError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"msg": exc.detail, "status_code": exc.status_code}
    )

@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"msg": "Error de validación", "details": exc.errors(), "status_code": 422, "success": False},
    )

app.include_router(edificios_router)
app.include_router(departamentos_router)
app.include_router(authentication_router)
app.include_router(inquilinos_router)
app.include_router(contratos_router)
@app.get("/")
async def root():
    return {"message": "Hello World"}