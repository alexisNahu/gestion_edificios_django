from fastapi import APIRouter

from apps.edificios.departamentos.controller import router as departamentos_router
from apps.edificios.edificios.controller import router as edificios_router
from apps.authentication.controller import router as authentication_router
from apps.contratos.contratos.controller import router as contratos_router
from apps.inquilinos.inquilinos.controller import router as inquilinos_router
from apps.reclamos.reclamos.controller import router as reclamos_router
from apps.contratos.deudas.controller import router as deudas_router
from apps.finanzas.abonos.controller import router as abonos_router
from apps.finanzas.pagos.controller import router as pagos_router
app_router = APIRouter()
app_router.include_router(abonos_router)
app_router.include_router(edificios_router)
app_router.include_router(departamentos_router)
app_router.include_router(authentication_router)
app_router.include_router(inquilinos_router)
app_router.include_router(contratos_router)
app_router.include_router(reclamos_router)
app_router.include_router(deudas_router)
app_router.include_router(pagos_router)
