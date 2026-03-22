from asgiref.sync import sync_to_async

from apps.edificios.models import Departamentos
from core.exceptions import NotFoundError


class DepartamentosRepository:
    @staticmethod
    async def select(**kwargs):
        try:
            queryset = Departamentos.objects.filter(**kwargs) if kwargs else Departamentos.objects.all()
            result = await sync_to_async(list)(queryset)

            if not result:
                raise NotFoundError("No se encontraron departamentos")

            return result

        except Exception as e:
            print(f'Error selecting departamentos: {e}')
            raise e
    @staticmethod
    async def create(**kwargs):
        try:
            return await sync_to_async(Departamentos.objects.create)(**kwargs)
        except Exception as e:
            print(f'Error creating departamentos: {e}')
            raise e
    @staticmethod
    async def delete_by_id(id: int):
        try:
            deleted, _ = await sync_to_async(Departamentos.objects.filter(id=id).delete)()
            return deleted
        except Exception as e:
            print(f'Error deleting departamentos: {e}')
            raise e
    @staticmethod
    async def update(id: int, **kwargs):
        try:
            queryset = Departamentos.objects.filter(id=id)
            await sync_to_async(queryset.update)(**kwargs)

            return await sync_to_async(queryset.first)()
        except Exception as e:
            print(f'Error updating departamentos: {e}')
            raise e