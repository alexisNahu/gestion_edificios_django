from django.core.paginator import Paginator
from core.exceptions import handle_error, NotFoundError
from .repository import EdificiosRepository
from .schema import EdificioRespuesta, EdificioActualizar, EdificioCrear


class EdificiosService:

    def __init__(self):
        self.repo = EdificiosRepository()

    async def get(self, page: int = 1, page_size: int = 10, **kwargs):
        try:
            cleaned_params = {k: v for k, v in kwargs.items() if v is not None}

            edificios = await self.repo.select(**cleaned_params)
            if not edificios: raise NotFoundError('No se encontraron edificios '+str(kwargs))

            paginator = Paginator(edificios, page_size)
            pagina = paginator.get_page(page)

            return {
                "data": [EdificioRespuesta.model_validate(e) for e in pagina.object_list],
                "pagination": {
                    "paginas_totales": paginator.num_pages,
                    "pagina_actual": page,
                    "pagina_siguiente": pagina.next_page_number() if pagina.has_next() else None,
                    "pagina_previa": pagina.previous_page_number() if pagina.has_previous() else None,
                }
            }
        except Exception as e:
            handle_error(e)


    async def create(self, payload: EdificioCrear):
        try:
            cleaned_payload = payload.model_dump(exclude_none=True)
            return await self.repo.create(**cleaned_payload)
        except Exception as e:
            raise handle_error(e)

    async def delete(self, id: int):
        try:
            reg = await self.get(id=id)
            was_deleted = await self.repo.delete_by_id(id)
            if not was_deleted: raise NotFoundError('No se encontraron edificios'+str(id))
            return reg['data'][0]
        except Exception as e:
            raise handle_error(e)

    async def update(self, id: int, payload: EdificioActualizar):
        try:
            cleaned_payload = payload.model_dump(exclude_none=True)
            new_reg = await self.repo.update(id, **cleaned_payload)
            if not new_reg: raise NotFoundError('No se encontraron edificios al actualizar'+str(id))
            return new_reg
        except Exception as e:
            raise handle_error(e)


