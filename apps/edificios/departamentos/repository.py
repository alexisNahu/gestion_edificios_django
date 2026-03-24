from apps.edificios.models import Departamentos
from core.repository import Repository


class DepartamentosRepository(Repository[Departamentos]):
    _table = 'departamentos'
    _model = Departamentos
    _objects = Departamentos.objects