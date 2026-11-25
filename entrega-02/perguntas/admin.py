
from django.contrib import admin
from django.db.models import Count, Q
from .models import Pergunta, Resposta, VisualizacaoVideo

admin.site.register(Pergunta)
admin.site.register(Resposta)


@admin.register(VisualizacaoVideo)
class VisualizacaoVideoAdmin(admin.ModelAdmin):
    list_display = ('video', 'autenticado', 'data_reproducao')
    list_filter = ('video', 'autenticado', 'data_reproducao')

    def changelist_view(self, request, extra_context=None):
        visualizacoes = VisualizacaoVideo.objects.all()

        contexto = {
            'total': visualizacoes.count(),
            'logados': visualizacoes.filter(autenticado=True).count(),
            'nao_logados': visualizacoes.filter(autenticado=False).count(),
            'videos': visualizacoes.values('video').annotate(
                total=Count('id'),
                logados=Count('id', filter=Q(autenticado=True)),
                nao_logados=Count('id', filter=Q(autenticado=False))
            ).order_by('video')
        }

        contexto.update(extra_context or {})

        return super().changelist_view(
            request,
            extra_context=contexto
        )
