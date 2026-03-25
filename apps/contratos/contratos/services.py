from fastapi import Depends

from apps.inquilinos.inquilinos.services import InquilinosService
from core.base.services import Service
from core.exceptions import handle_error, ConflictError
from apps.contratos.contratos.repository import ContratosRepository
from apps.contratos.contratos.schema import (
    ContratoRespuesta,
    ContratoCrear,
    ContratoActualizar
)
from apps.edificios.departamentos.services import DepartamentosService

class ContratosService(Service[ContratoRespuesta, ContratoCrear, ContratoActualizar]):
    def __init__(
            self,
            repo: ContratosRepository = Depends(),
            inquilinos_service: InquilinosService = Depends(),
            departamentos_service: DepartamentosService = Depends()
    ):
        super().__init__(
            repo=repo,
            schema_resp=ContratoRespuesta,
            entity_name="contratos",
        )
        self.inquilinos_service = inquilinos_service
        self.departamentos_service = departamentos_service

    async def create(self, payload: ContratoCrear):
            response = await self.departamentos_service.get(id=payload.departamento_id)
            departamento_relacionado = response['data'][0]
            if departamento_relacionado.ocupado:
                raise ConflictError(f"Departamento numero {departamento_relacionado.numero_departamento} ocupado")

            existe_contrato = await self.repo.exists_reg(departamento_id=payload.departamento_id)

            if existe_contrato: raise ConflictError('Ya existe un contrato a este departamento')

            await self.inquilinos_service.get(id=payload.inquilino_id)

            cleaned_payload = payload.model_dump(exclude_none=True)
            return await self.repo.create(**cleaned_payload)

    async def update(self, id: int, payload: ContratoActualizar):
            cleaned_payload = payload.model_dump(exclude_none=True)

            if "departamento_id" in cleaned_payload:
                nuevo_depto = await self.departamentos_service.get(id=cleaned_payload["departamento_id"])

                if nuevo_depto.ocupado:
                    raise ConflictError(f"El departamento N° {nuevo_depto.numero_departamento} ya está ocupado.")

                if await self.repo.exists_reg(departamento_id=cleaned_payload["departamento_id"]):
                    raise ConflictError(
                        f"Ya existe un contrato para el departamento {nuevo_depto.numero_departamento}.")

            if "inquilino_id" in cleaned_payload:
                await self.inquilinos_service.get(id=cleaned_payload["inquilino_id"])

            new_reg = await self.repo.update(id, **cleaned_payload)
            return new_reg

