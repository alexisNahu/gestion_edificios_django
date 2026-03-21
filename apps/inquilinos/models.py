from django.db import models

TIPO_IDENTIFICACION = [
            ('Cedula', 'cedula'),
            ('Pasaporte', 'pasaporte'),
            ('Ruc', 'ruc'),
            ('Licencia','licencia')
        ]

class Inquilinos(models.Model):
    nombre_completo = models.CharField(max_length=60)
    status = models.BooleanField(default=True)
    telefono = models.CharField(max_length=60)
    email = models.EmailField()
    numero_identificion = models.CharField(max_length=60)
    tipo_identificacion = models.CharField(
        max_length=60,
        choices=TIPO_IDENTIFICACION
    )

    def __str__(self):
        return f"Nombre inquilino: {self.nombre_completo}"

    class Meta:
        db_table = 'inquilinos'
