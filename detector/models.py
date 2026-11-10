from django.db import models

class Recurso(models.Model):
    ESTADO_CHOICES = [
        ('DISPONIBLE', 'Disponible'),
        ('EN_USO', 'En uso'),
    ]
    
    CATEGORIA_CHOICES = [
        ('INSTRUMENTACION', 'Instrumentación'),
        ('BIBLIOGRAFIA', 'Bibliografía'),
        ('ELECTRONICA', 'Electrónica'),
    ]

    codigo = models.CharField(max_length=20, unique=True, verbose_name="ID (Ej: EQ-001)")
    nombre = models.CharField(max_length=200, verbose_name="Nombre del Equipo / Libro")
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='DISPONIBLE')

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"