from django.db import models

# Create your models here.
class Reclamos(models.Model):
    contrato = models.ForeignKey(
        'contratos.Contratos',
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        db_column='id_contrato',
        related_name='reclamos'
    )
    descripcion = models.TextField(null=False, blank=False)
    status = models.BooleanField(null=False, blank=False, default=True)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Departamento {self.contrato.departamento} - Reclamo: {self.status} - Inquilino: {self.contrato.inquilino}'

    class Meta:
        db_table = 'reclamos'
        verbose_name = 'Reclamo'
        verbose_name_plural = 'Reclamos'