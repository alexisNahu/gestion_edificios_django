from apps.finanzas.abonos.repository import AbonosRepository
from apps.finanzas.abonos.schema import AbonoRespuesta, AbonoCrear, AbonoActualizar
from apps.finanzas.pagos.service import PagosService
from core.base.services import Service

class AbonosService(Service[AbonoRespuesta, AbonoCrear, AbonoActualizar]):
    def __init__(self):
        super().__init__(
            repo=AbonosRepository(),
            schema_resp=AbonoRespuesta,
            entity_name="Abonos"
        )
        # Inyectamos el service de Pagos para validaciones
        self.pagos_service = PagosService()

    async def create(self, payload: AbonoCrear) -> AbonoRespuesta:
        # Validamos que el pago asociado exista
        await self.pagos_service.get(id=payload.pago_id)

        cleaned_payload = payload.model_dump(exclude_none=True)

        # Al crear el abono, el método save() en Django se encargará
        # automáticamente de recalcular la suma en la tabla Pagos.
        return await self.repo.create(**cleaned_payload)

    async def update(self, id: int, payload: AbonoActualizar) -> AbonoRespuesta:
        cleaned_payload = payload.model_dump(exclude_none=True)

        # Si el payload intenta cambiar el pago_id, validamos que el nuevo exista
        if "pago_id" in cleaned_payload:
            await self.pagos_service.get(id=cleaned_payload["pago_id"])

        new_reg = await self.repo.update(id, **cleaned_payload)
        return new_reg