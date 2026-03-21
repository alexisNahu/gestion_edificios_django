from fastapi import params

from core.exceptions import BadRequestError, handle_error
from .repository import EdificiosRepository
from .schema import EdificioFiltros


class EdificiosService:

    def __init__(self):
        self.repo = EdificiosRepository()

    async def get_edificios(self, params):
        cleaned_params = params.model_dump(exclude_none=True)
        if not cleaned_params or cleaned_params == {}:
            raise BadRequestError(f"Filtros invalidos - {params}")
        return await self.repo.select(**cleaned_params)

    async def create_edificio(self, payload):
        try:
            cleaned_payload = payload.model_dump(exclude_none=True)
            edificio = await self.repo.create(**cleaned_payload)
            return edificio
        except Exception as e:
            raise handle_error(e)

