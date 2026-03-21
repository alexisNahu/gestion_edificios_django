from asgiref.sync import sync_to_async
from apps.edificios.models import Edificios
from core.exceptions import NotFoundError


class EdificiosRepository:

    async def select(self, **kwargs):
        try:
            queryset = Edificios.objects.filter(**kwargs) if kwargs else Edificios.objects.all()
            result = await sync_to_async(list)(queryset.values())

            if not result:
                raise NotFoundError("No se encontraron edificios")

            return result

        except Exception as e:
            print(f'Error selecting edificios: {e}')
            raise e

    async def create(self, **kwargs):
        try:
            return await sync_to_async(Edificios.objects.create)(**kwargs)
        except Exception as e:
            print(f'Error creating edificios: {e}')
