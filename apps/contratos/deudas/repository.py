from apps.contratos.models import Deuda
from core.base.repository import Repository


class DeudaRepository(Repository[Deuda]):
    _table = 'deuda'
    _model = Deuda
    _objects = Deuda.objects