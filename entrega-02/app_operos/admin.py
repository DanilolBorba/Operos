from django.contrib import admin
from .models import Solicitacao

# Register your models here.

@admin.register(Solicitacao)
class SolicitacaoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'usuario',
        'servico',
        'porte_empresa',
        'data_solicitacao',
        'protocolo',
    )

    list_filter = ('porte_empresa', 'data_solicitacao')

    search_fields = (
        'usuario__username',
        'servico',
        'protocolo',
    )