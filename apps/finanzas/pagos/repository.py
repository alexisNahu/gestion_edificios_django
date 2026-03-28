from apps.finanzas.models import Pagos
from core.base.repository import Repository

class PagosRepository(Repository[Pagos]):
    _table = 'pagos'
    _model = Pagos
    _objects = Pagos.objects