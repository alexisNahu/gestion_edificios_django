
from apps.inquilinos.models import Inquilinos
from core.base.repository import Repository


class InquilinosRepository(Repository[Inquilinos]):
    _table = 'inquilinos'
    _model = Inquilinos
    _objects = Inquilinos.objects