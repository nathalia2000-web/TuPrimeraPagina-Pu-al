

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Mensaje(models.Model):
    remitente = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='mensajes_enviados'
    )
    destinatario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='mensajes_recibidos'
    )
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)

    class Meta:
        ordering = ['fecha']

    def __str__(self):
        return f'{self.remitente} → {self.destinatario}: {self.contenido[:30]}'
    