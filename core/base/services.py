from __future__ import annotations

from typing import Generic, TypeVar, Type, Any
from django.core.paginator import Paginator
from core.exceptions import handle_error, NotFoundError
from core.utils import clean_none_params

TRespuesta = TypeVar("TRespuesta")
TCrear = TypeVar("TCrear")
TActualizar = TypeVar("TActualizar")

class Service(Generic[TRespuesta, TCrear, TActualizar]):
    def __init__(
            self,
            repo: Any,
            schema_resp: Type[TRespuesta],
            entity_name: str
    ):
        self.repo = repo
        self.schema_resp = schema_resp
        self.entity_name = entity_name

    async def get(self, page: int = 1, page_size: int = 10, **kwargs):
        cleaned_params = clean_none_params(kwargs)
        data = await self.repo.select(**cleaned_params)
        if not data:
            raise NotFoundError(f'No se encontraron {self.entity_name} {str(kwargs)}')

        paginator = Paginator(data, page_size)
        pagina = paginator.get_page(page)

        return {
            "data": [self.schema_resp.model_validate(e) for e in pagina.object_list],
            "pagination": {
                "paginas_totales": paginator.num_pages,
                "pagina_actual": page,
                "pagina_siguiente": pagina.next_page_number() if pagina.has_next() else None,
                "pagina_previa": pagina.previous_page_number() if pagina.has_previous() else None,
            }
        }

    async def create(self, payload: TCrear):
        cleaned_payload = payload.model_dump(exclude_none=True)
        return await self.repo.create(**cleaned_payload)

    async def delete(self, id: int):
        reg = await self.get(id=id)
        was_deleted = await self.repo.delete_by_id(id)
        if not was_deleted: raise NotFoundError(f'No se encontraron {self.entity_name} {str(id)}')
        return reg['data'][0]

    async def update(self, id: int, payload: TActualizar):
        cleaned_payload = payload.model_dump(exclude_none=True)
        new_reg = await self.repo.update(id, **cleaned_payload)
        if not new_reg:
            raise NotFoundError(f'No se encontraron {self.entity_name} al actualizar {str(id)}')
        return new_reg

    async def exists_reg(self, id: int):
        return await self.repo.ping(id=id)