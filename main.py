from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from core.exceptions import ApiError
from core.setup_django import init_django

init_django()  # ← primero

from fastapi import FastAPI, Request

from apps.edificios.controller import router as edificios_router
from apps.authentication.controller import router as authentication_router
app = FastAPI()

@app.exception_handler(ApiError)
async def api_error_handler(request: Request, exc: ApiError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"msg": exc.detail, "status_code": exc.status_code}
    )
app.include_router(edificios_router)
app.include_router(authentication_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}