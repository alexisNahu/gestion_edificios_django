from fastapi import Depends

from apps.contratos.contratos.services import ContratosService
from apps.finanzas.models import Pagos
from apps.finanzas.pagos.repository import PagosRepository
from apps.finanzas.pagos.schema import PagoRespuesta, PagoCrear, PagoFiltros, PagoActualizar
from core.base.services import Service

class PagosService(Service[PagoRespuesta, PagoCrear, PagoActualizar]):
    def __init__(
            self,
            repo: PagosRepository = Depends(),
            contratos_service: ContratosService = Depends(),
    ):
        super().__init__(
            repo=repo,
            schema_resp=PagoRespuesta,
            entity_name="Pagos"
        )

        self.contratos_service = contratos_service

    async def create(self, payload: PagoCrear) -> PagoRespuesta:
        await self.contratos_service.get(id=payload.contrato_id)

        cleaned_payload = payload.model_dump(exclude_none=True)

        return await self.repo.create(**cleaned_payload)

    async def update(self, id: int, payload: PagoActualizar) -> Pagos:
        cleaned_payload = payload.model_dump(exclude_none=True)

        if "contrato_id" in cleaned_payload:
            await self.contratos_service.get(id=cleaned_payload["contrato_id"])

        new_reg = await self.repo.update(id, **cleaned_payload)
        return new_reg