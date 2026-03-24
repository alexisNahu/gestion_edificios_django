from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from apps.edificios.models import Departamentos



class Contratos(models.Model):
    inquilino = models.ForeignKey(
        'inquilinos.Inquilinos',
        on_delete=models.CASCADE,
        null=False, 
        blank=False,
        db_column='inquilino_id'
    )
    departamento = models.ForeignKey(
        'edificios.Departamentos',
        on_delete=models.CASCADE,
        null=False, 
        blank=False,
        db_column='departamento_id'
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
    dia_pago = models.IntegerField(null=False, blank=False, default=15, validators=[MaxValueValidator(31), MinValueValidator(1)])
    fecha_inicio = models.DateField(null=False, blank=False, default=timezone.now)
    fecha_fin = models.DateField(null=False, blank=False)
    al_dia = models.BooleanField(null=False, blank=False, default=True)
    descripcion = models.TextField(null=False, blank=False)

    def __str__(self):
        return f"Contrato del inquilino: {self.inquilino.nombre_completo}"

    class Meta:
        db_table = 'contratos'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.departamento:
            if self.status: self.departamento.ocupado = True
            if not self.status: self.departamento.ocupado = False
            self.departamento.save(update_fields=['ocupado'])


    def delete(self, *args, **kwargs):
        departamento_relacionado = self.departamento

        result = super().delete(*args, **kwargs)

        if departamento_relacionado:
            departamento_relacionado.ocupado = False
            departamento_relacionado.save(update_fields=['ocupado'])

        return result



class Deuda(models.Model):
    contrato = models.ForeignKey(
        'contratos.Contratos',
        on_delete=models.CASCADE,
        related_name='deudas',
        db_column='contrato_id'
    )

    status = models.IntegerField(default=1)

    motivo = models.CharField(
        max_length=20,
        choices=([
            ('Departamento','departamento'),
            ('Ande', 'ande')
        ]),
    )

    monto = models.IntegerField()

    fecha_comienzo = models.DateField()

    fecha_final = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'deudas'
        verbose_name = 'Deuda'
        verbose_name_plural = 'Deudas'

    def __str__(self):
        return f"Deuda {self.motivo} - Contrato {self.contrato} - ${self.monto}"

