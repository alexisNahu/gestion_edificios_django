from apps.contratos.models import Contratos
from core.base.repository import Repository


class ContratosRepository(Repository[Contratos]):
    _table = 'contratos'
    _model = Contratos
    _objects = Contratos.objects