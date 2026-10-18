
from django.contrib import admin
from .models import Solicitacao


@admin.register(Solicitacao)
class SolicitacaoAdmin(admin.ModelAdmin):

    list_display = (
        'usuario',
        'porte_empresa',
        'servico',
        'data_solicitacao'
    )

    list_filter = ('porte_empresa',)
