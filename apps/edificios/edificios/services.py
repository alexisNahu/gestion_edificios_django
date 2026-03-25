from fastapi import Depends
from core.base.services import Service
from .repository import EdificiosRepository
from .schema import EdificioRespuesta, EdificioCrear, EdificioActualizar

class EdificiosService(Service[EdificioRespuesta, EdificioCrear, EdificioActualizar]):
    def __init__(self, repo: EdificiosRepository = Depends()):
        # Llamamos al constructor del genérico pasando:
        # 1. El repositorio
        # 2. El schema de respuesta para las validaciones
        # 3. El nombre de la entidad para los mensajes de error
        super().__init__(repo, EdificioRespuesta, "edificios")