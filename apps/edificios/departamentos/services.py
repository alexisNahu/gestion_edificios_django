from django.core.paginator import Paginator

from apps.edificios.departamentos.repository import DepartamentosRepository
from apps.edificios.departamentos.schema import DepartamentoRespuesta, DepartamentoCrear, DepartamentoActualizar
from apps.edificios.edificios.repository import EdificiosRepository
from apps.edificios.edificios.services import EdificiosService
from core.exceptions import NotFoundError, handle_error


class DepartamentosService:

    def __init__(self):
        self.repo = DepartamentosRepository()
        self.edificios_service = EdificiosService()

    async def get(self, page: int = 1, page_size: int = 10, **kwargs):
        try:
            cleaned_params = {k: v for k, v in kwargs.items() if v is not None}

            data = await self.repo.select(**cleaned_params)
            if not data: raise NotFoundError('No se encontraron departamentos '+str(kwargs))

            paginator = Paginator(data, page_size)
            pagina = paginator.get_page(page)

            return {
                "data": [DepartamentoRespuesta.model_validate(e) for e in pagina.object_list],
                "pagination": {
                    "paginas_totales": paginator.num_pages,
                    "pagina_actual": page,
                    "pagina_siguiente": pagina.next_page_number() if pagina.has_next() else None,
                    "pagina_previa": pagina.previous_page_number() if pagina.has_previous() else None,
                }
            }
        except Exception as e:
            raise handle_error(e)


    async def create(self, payload: DepartamentoCrear):
        try:
            cleaned_payload = payload.model_dump(exclude_none=True)
            edificio = await self.edificios_service.get(id=cleaned_payload['edificio_id'])
            if not edificio or edificio == []: raise NotFoundError('No se encontraron edificios al crear'+str(id))
            return await self.repo.create(**cleaned_payload)
        except Exception as e:
            raise handle_error(e)

    async def delete(self, id: int):
        try:
            reg = await self.get(id=id)
            was_deleted = await self.repo.delete_by_id(id)
            if not was_deleted: raise NotFoundError('No se encontraron departamentos'+str(id))
            return reg['data'][0]
        except Exception as e:
            raise handle_error(e)

    async def update(self, id: int, payload: DepartamentoActualizar):
        try:
            cleaned_payload = payload.model_dump(exclude_none=True)
            new_reg = await self.repo.update(id, **cleaned_payload)
            if not new_reg: raise NotFoundError('No se encontraron departamentos al actualizar'+str(id))
            return new_reg
        except Exception as e:
            raise handle_error(e)
