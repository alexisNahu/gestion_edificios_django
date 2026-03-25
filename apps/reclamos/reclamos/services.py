from apps.reclamos.models import Reclamos
from apps.reclamos.reclamos.schema import ReclamoRespuesta, ReclamoCrear, ReclamoActualizar
from apps.reclamos.reclamos.repository import ReclamosRepository
from apps.contratos.models import Contratos
from core.base.services import Service
from core.exceptions import NotFoundError


class ReclamosService(Service[ReclamoRespuesta, ReclamoCrear, ReclamoActualizar]):
    def __init__(self):
        super().__init__(
            repo=ReclamosRepository(),
            schema_resp=ReclamoRespuesta,
            entity_name="Reclamo"
        )

    async def create(self, payload: ReclamoCrear) -> ReclamoRespuesta:
        # Validamos que el contrato exista antes de intentar crear el reclamo
        contrato_id = payload.contrato_id
        if not await Contratos.objects.filter(id=contrato_id).aexists():
            raise NotFoundError(f"No se puede crear el reclamo: El contrato {contrato_id} no existe.")

        return await super().create(payload)

    async def update(self, id: int, payload: ReclamoActualizar) -> ReclamoRespuesta:
        # El update genérico ya maneja la limpieza de None y el error si el ID no existe
        return await super().update(id, payload)