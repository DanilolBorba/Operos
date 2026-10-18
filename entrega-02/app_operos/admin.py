from django.contrib import admin
from django.db.models import Count
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

    def changelist_view(self, request, extra_context=None):

        dados = (
            Solicitacao.objects
            .values('porte_empresa')
            .annotate(
                total=Count('id')
            )
        )

        totais = {
            item['porte_empresa']: item['total']
            for item in dados
        }

        contexto = {
            'pequenas': totais.get('pequeno', 0),
            'medias': totais.get('medio', 0),
            'grandes': totais.get('grande', 0)
        }

        contexto.update(extra_context or {})

        return super().changelist_view(
            request,
            extra_context=contexto
        )
