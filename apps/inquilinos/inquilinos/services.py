from fastapi import Depends
from core.base.services import Service
from apps.inquilinos.inquilinos.repository import InquilinosRepository
from apps.inquilinos.inquilinos.schema import (
    InquilinoRespuesta,
    InquilinoCrear,
    InquilinoActualizar
)
from core.exceptions import handle_error, ConflictError


class InquilinosService(Service[InquilinoRespuesta, InquilinoCrear, InquilinoActualizar]):
    def __init__(self, repo: InquilinosRepository = Depends()):
        super().__init__(
            repo=repo,
            schema_resp=InquilinoRespuesta,
            entity_name="inquilinos"
        )

    async def create(self, payload: InquilinoCrear):
        """Valida que el número de identificación sea único al crear."""
        await self._check_unique_identificacion(payload.numero_identificacion)
        return await super().create(payload)

    async def update(self, id: int, payload: InquilinoActualizar):
        """Valida que el nuevo número de identificación no choque con otros al actualizar."""
        if payload.numero_identificacion:
            await self._check_unique_identificacion(payload.numero_identificacion, exclude_id=id)

        return await super().update(id, payload)

    async def _check_unique_identificacion(self, identificacion: str, exclude_id: int = None):
        exists = await self.repo.select(numero_identificacion=identificacion)

        if exists:
            # Si estamos en un update, verificamos que el que existe no sea el mismo que estamos editando
            if exclude_id and exists[0].id == exclude_id:
                return

            raise ConflictError(
                f"Ya existe un inquilino con el número de identificación: {identificacion}"
            )