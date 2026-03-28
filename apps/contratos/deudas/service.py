from apps.contratos.models import Contratos, Deuda
from apps.contratos.deudas.schema import DeudaRespuesta, DeudaCrear, DeudaActualizar
from apps.contratos.deudas.repository import DeudaRepository
from core.base.services import Service
from core.exceptions import NotFoundError


class DeudaService(Service[DeudaRespuesta, DeudaCrear, DeudaActualizar]):
    def __init__(self):
        super().__init__(
            repo=DeudaRepository(),
            schema_resp=DeudaRespuesta,
            entity_name="Deuda"
        )

    async def create(self, payload: DeudaCrear) -> DeudaRespuesta:

        if not await Contratos.objects.filter(id=payload.contrato_id).aexists():
            raise NotFoundError(f"No se puede crear la deuda: El contrato {payload.contrato_id} no existe.")

        return await super().create(payload)

    async def update(self, id: int, payload: DeudaActualizar) -> Deuda:
        return await super().update(id, payload)