from fastapi import Depends
from core.services import Service
from apps.edificios.departamentos.repository import DepartamentosRepository
from apps.edificios.departamentos.schema import (
    DepartamentoRespuesta,
    DepartamentoCrear,
    DepartamentoActualizar
)
from apps.edificios.edificios.services import EdificiosService
from core.exceptions import handle_error


class DepartamentosService(Service[DepartamentoRespuesta, DepartamentoCrear, DepartamentoActualizar]):
    def __init__(
            self,
            repo: DepartamentosRepository = Depends(),
            edificios_service: EdificiosService = Depends()
    ):
        # Inicialización básica del padre
        super().__init__(
            repo=repo,
            schema_resp=DepartamentoRespuesta,
            entity_name="departamentos",
        )
        # Guardamos el servicio de edificios para usarlo manualmente
        self.edificios_service = edificios_service

    async def create(self, payload: DepartamentoCrear):
        try:
            # Validación manual de la FK (Edificio)
            await self.edificios_service.get(id=payload.edificio_id)

            # Si el get no lanzó NotFoundError, procedemos
            cleaned_payload = payload.model_dump(exclude_none=True)
            return await self.repo.create(**cleaned_payload)
        except Exception as e:
            raise handle_error(e)

    async def update(self, id: int, payload: DepartamentoActualizar):
        try:
            cleaned_payload = payload.model_dump(exclude_none=True)

            # Si el usuario intenta cambiar el edificio, validamos que el nuevo exista
            if "edificio_id" in cleaned_payload:
                await self.edificios_service.get(id=cleaned_payload["edificio_id"])

            new_reg = await self.repo.update(id, **cleaned_payload)
            return new_reg
        except Exception as e:
            raise handle_error(e)