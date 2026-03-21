from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from core.exceptions import ApiError
from core.setup_django import init_django

init_django()  # ← primero

from fastapi import FastAPI, Request

from apps.edificios.controller import router as edificios_router
app = FastAPI()
app.include_router(edificios_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}