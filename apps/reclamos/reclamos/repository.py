from apps.reclamos.models import Reclamos
from core.base.repository import Repository


class ReclamosRepository(Repository[Reclamos]):
    _table = 'reclamos'
    _model = Reclamos
    _objects = Reclamos.objects