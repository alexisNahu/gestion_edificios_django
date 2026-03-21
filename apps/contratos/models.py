
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


# Create your models here.

class Contratos(models.Model):
    inquilino = models.ForeignKey(
        'inquilinos.Inquilinos',
        on_delete=models.CASCADE,
        null=False, blank=False,
        db_column='id_inquilino'
    )
    departamento = models.ForeignKey(
        'edificios.Departamentos',
        on_delete=models.CASCADE,
        null=False, blank=False,
        db_column='id_departamento'
    )
    frecuencia_pago = models.CharField(
        choices=([
            ('semanal', 'Semanal'),
            ('quincenal', 'Quincenal'),
            ('mensual', 'Mensual'),
            ('bimestral', 'Bimestral'),
            ('trimestral', 'Trimestral'),
            ('semestral', 'Semestral'),
            ('anual', 'Anual'),
        ])
    )
    monto = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.BooleanField(null=False, blank=False, default=True)
    dia_pago = models.IntegerField(null=False, blank=False, default=15, validators=[MaxValueValidator(28), MinValueValidator(1)])
    fecha_inicio = models.DateField(null=False, blank=False, default=timezone.now)
    fecha_fin = models.DateField(null=False, blank=False)
    al_dia = models.BooleanField(null=False, blank=False, default=True)
    descripcion = models.TextField(null=False, blank=False)

    def __str__(self):
        return f"Contrato del inquilino: {self.inquilino.nombre}"

    class Meta:
        db_table = 'contratos'

