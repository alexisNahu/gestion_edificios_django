from apps.finanzas.models import Abonos
from core.base.repository import Repository


class AbonosRepository(Repository[Abonos]):
    _table = 'abonos'
    _model = Abonos
    _objects = Abonos.objects