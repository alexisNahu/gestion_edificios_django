from asgiref.sync import sync_to_async
from apps.edificios.models import Edificios
from core.exceptions import NotFoundError


class EdificiosRepository:
    @staticmethod
    async def select(**kwargs):
        try:
            queryset = Edificios.objects.filter(**kwargs) if kwargs else Edificios.objects.all()
            result = await sync_to_async(list)(queryset)

            if not result:
                raise NotFoundError("No se encontraron edificios")

            return result

        except Exception as e:
            print(f'Error selecting edificios: {e}')
            raise e
    @staticmethod
    async def create(**kwargs):
        try:
            return await sync_to_async(Edificios.objects.create)(**kwargs)
        except Exception as e:
            print(f'Error creating edificios: {e}')
    @staticmethod
    async def delete_by_id(id: int):
        try:
            deleted, _ = await sync_to_async(Edificios.objects.filter(id=id).delete)()
            return deleted
        except Exception as e:
            print(f'Error deleting edificio: {e}')
            raise e
    @staticmethod
    async def update(id: int, **kwargs):
        try:
            queryset = Edificios.objects.filter(id=id)
            await sync_to_async(queryset.update)(**kwargs)

            return await sync_to_async(queryset.first)()
        except Exception as e:
            print(f'Error updating edificio: {e}')
            raise e
