# core/repositories.py
from asgiref.sync import sync_to_async
from django.db import connection

from core.interfaces import IRepository, T
from core.exceptions import NotFoundError

class Repository(IRepository[T]):
    """Aquí vive la lógica pesada de Django y async"""

    async def select(self, **kwargs):
        try:
            # Normalizamos los filtros para PostgreSQL
            filtros = {}
            for clave, valor in kwargs.items():
                # Si es un string y no tiene filtros especiales (__gte, __in, etc)
                if isinstance(valor, str) and "__" not in clave:
                    filtros[f"{clave}__icontains"] = valor
                else:
                    filtros[clave] = valor

            # Ejecutamos la query con ILIKE (gracias a icontains)
            queryset = self._objects.filter(**filtros) if filtros else self._objects.all()
            result = await sync_to_async(list)(queryset)

            if not result:
                raise NotFoundError(f"No se encontraron registros en {self._table}")
            return result
        except Exception as e:
            if not isinstance(e, NotFoundError):
                print(f'Error selecting {self._table}: {e}')
            raise e

    async def create(self, **kwargs):
        try:
            return await sync_to_async(self._objects.create)(**kwargs)
        except Exception as e:
            print(f'Error creating {self._table}: {e}')
            raise e

    async def update(self, id: int, **kwargs) -> T:
        try:
            instance = await sync_to_async(self._objects.filter(id=id).first)()

            if not instance:
                raise NotFoundError(f"Registro con ID {id} no encontrado en {self._table}")

            for clave, valor in kwargs.items():
                if hasattr(instance, clave):
                    setattr(instance, clave, valor)

            await sync_to_async(instance.save)()

            return instance
        except Exception as e:
            if not isinstance(e, NotFoundError):
                print(f'Error updating {self._table}: {e}')
            raise e

    async def delete_by_id(self, id: int) -> bool:
        try:
            instance = await sync_to_async(self._objects.filter(id=id).first)()

            if instance:
                await sync_to_async(instance.delete)()
                return True

            return False
        except Exception as e:
            print(f'Error deleting in {self._table}: {e}')
            raise e

    async def exists_reg(self, **kwargs) -> bool:
        """
        Verifica la existencia de un registro sin traer sus datos.
        Retorna True si existe, False si no.
        """
        try:
            # Creamos el queryset con los filtros dinámicos
            queryset = self._objects.filter(**kwargs)

            # .exists() es la forma más ligera de consultar en Django/Postgres
            return await sync_to_async(queryset.exists)()
        except Exception as e:
            print(f'Error checking existence in {self._table}: {e}')
            return False