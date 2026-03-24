from django.db import models
from django.db.models import Sum

class Pagos(models.Model):
    contrato = models.ForeignKey(
        'contratos.Contratos',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        db_column='contrato_id',
    )
    monto_pagado = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2)
    saldo_pendiente = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2)
    status = models.BooleanField(null=False, blank=False, default=True)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.contrato} - Pago: {self.monto_pagado}'

    class Meta:
        db_table = 'pagos'
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'

    def save(self, *args, **kwargs):
        self.saldo_pendiente = self.contrato.monto - self.monto_pagado
        if self.saldo_pendiente == 0:
            self.contrato.al_dia = True
            self.contrato.save()
        super().save(*args, **kwargs)

class Abonos(models.Model):
    pago = models.ForeignKey(
        'finanzas.Pagos',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        db_column='pago_id',
        related_name='abonos'
    )
    monto = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2)
    fecha = models.DateField(auto_now_add=True)
    tipo_pago = models.CharField(
        max_length=20,
        choices=[
            ('efectivo', 'Efectivo'),
            ('transferencia', 'Transferencia'),
            ('tarjeta', 'Tarjeta'),
        ],
        null=False,
        blank=False
    )
    descripcion = models.TextField(null=True, blank=True)
    ayuda_dep = models.BooleanField(null=False, blank=False, default=False)

    def __str__(self):
        return f'{self.pago} - Abono: {self.monto}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        pago_instancia = self.pago
        suma_abonos = Abonos.objects.filter(pago=pago_instancia).aggregate(Sum('monto'))['monto__sum'] or 0
        pago_instancia.monto_pagado = suma_abonos
        pago_instancia.save()

    class Meta:
        db_table = 'abonos'
        verbose_name = 'Abono'
        verbose_name_plural = 'Abonos'