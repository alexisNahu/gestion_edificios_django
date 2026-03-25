from apps.edificios.models import Edificios
from core.base.repository import Repository


class EdificiosRepository(Repository[Edificios]):
    _table = 'edificios'
    _model = Edificios
    _objects = Edificios.objects