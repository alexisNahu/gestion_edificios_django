from core.error_handlers import register_exception_handlers
from core.setup_django import init_django

init_django()

from core.router import app_router

from fastapi import FastAPI
app = FastAPI()

register_exception_handlers(app)
app.include_router(app_router)