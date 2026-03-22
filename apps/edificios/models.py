from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.db import models

# Create your models here.

class Edificios(models.Model):
    nombre = models.CharField(max_length=20, null=False, blank=False, validators=[MinLengthValidator(4)])
    descripcion = models.CharField(max_length=100, null=True, blank=True)
    status = models.BooleanField(default=True)
    direccion = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Nombre: {self.nombre}"

    class Meta:
        db_table = 'edificios'

class Departamentos(models.Model):
    numero_departamento = models.CharField(max_length=20, null=False, blank=False)
    piso = models.IntegerField(
        null=False, blank=False, validators=[MinValueValidator(0), MaxValueValidator(3)])
    descripcion = models.CharField(max_length=100, null=True, blank=True)
    edificio = models.ForeignKey(
        'edificios.Edificios',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        db_column='id_edificio'
    )
    status = models.BooleanField(default=True)
    ocupado = models.BooleanField(default=False)

    def __str__(self):
        return f"Num_depto: {self.numero_departamento} - Piso: {self.piso}"

    class Meta:
        db_table = 'departamentos'