from django.db import models
from django.conf import settings


class Solicitacao(models.Model):

    PORTE_EMPRESA = [
        ('pequeno', 'Pequeno'),
        ('medio', 'Médio'),
        ('grande', 'Grande')
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    porte_empresa = models.CharField(
        max_length=10,
        choices=PORTE_EMPRESA
    )

    servico = models.CharField(max_length=150)

    data_solicitacao = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.usuario.username} - {self.servico}"
