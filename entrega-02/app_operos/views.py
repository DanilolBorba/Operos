from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Solicitacao


SOLUCOES_IOT = {
    'cadeia_fria': [
        {
            'nome': 'Monitoramento de temperatura e umidade',
            'descricao': (
                'Monitore as condições de armazenamento '
                'usando sensores conectados.'
            )
        },
        {
            'nome': 'Alertas de conservação',
            'descricao': (
                'Identifique alterações nas condições '
                'de conservação dos produtos.'
            )
        },
    ],

    'industria': [
        {
            'nome': 'Monitoramento de máquinas',
            'descricao': (
                'Acompanhe dados operacionais dos equipamentos '
                'e identifique possíveis anomalias.'
            )
        },
        {
            'nome': 'Monitoramento da produção',
            'descricao': (
                'Monitore variáveis dos processos produtivos '
                'por meio de sensores conectados.'
            )
        },
    ],

    'utilities': [
        {
            'nome': 'Monitoramento de consumo',
            'descricao': (
                'Acompanhe o consumo de água, gás e energia.'
            )
        },
        {
            'nome': 'Detecção de anomalias',
            'descricao': (
                'Identifique variações incomuns nas medições '
                'dos recursos monitorados.'
            )
        },
    ],

    'cidades_inteligentes': [
        {
            'nome': 'Monitoramento ambiental urbano',
            'descricao': (
                'Acompanhe indicadores ambientais por '
                'meio de sensores conectados.'
            )
        },
        {
            'nome': 'Monitoramento de mobilidade',
            'descricao': (
                'Colete dados relacionados à mobilidade urbana.'
            )
        },
    ],

    'edificios_inteligentes': [
        {
            'nome': 'Monitoramento de ambientes',
            'descricao': (
                'Acompanhe temperatura, umidade e outras '
                'condições dos ambientes.'
            )
        },
        {
            'nome': 'Monitoramento de sistemas prediais',
            'descricao': (
                'Monitore equipamentos e instalações '
                'do edifício.'
            )
        },
    ],

    'agronegocio': [
        {
            'nome': 'Monitoramento agrícola',
            'descricao': (
                'Acompanhe condições ambientais relevantes '
                'para as atividades agrícolas.'
            )
        },
        {
            'nome': 'Monitoramento operacional',
            'descricao': (
                'Monitore equipamentos e processos agrícolas.'
            )
        },
    ],

    'geral': [
        {
            'nome': 'Monitoramento inteligente com sensores IoT',
            'descricao': (
                'Monitore condições e variáveis importantes '
                'da operação da empresa usando sensores conectados.'
            )
        },
        {
            'nome': 'Coleta e acompanhamento de dados IoT',
            'descricao': (
                'Acompanhe dados coletados por dispositivos IoT '
                'para identificar alterações nos processos.'
            )
        },
    ],
}


def index(request):
    return HttpResponse("<h1>testando</h1>")


@login_required(login_url='perguntas:login')
def solicitar_servico(request):

    if request.method != 'POST':
        return redirect('perguntas:index')

    servico = request.POST.get('servico', '').strip()
    descricao = request.POST.get('descricao', '').strip()
    porte = request.POST.get('porte_empresa', '').strip()

    area = (
        getattr(request.user, 'area_atuacao', '') or ''
    ).strip().lower()

    solucoes = (
        SOLUCOES_IOT.get(area)
        or SOLUCOES_IOT['geral']
    )

    nomes_validos = [
        solucao['nome']
        for solucao in solucoes
    ]

    portes_validos = [
        opcao[0]
        for opcao in Solicitacao.PORTE_EMPRESA
    ]

    if servico not in nomes_validos:
        messages.error(
            request,
            'Selecione uma solução IoT válida.'
        )
        return redirect('perguntas:index')

    if porte not in portes_validos:
        messages.error(
            request,
            'Selecione um porte de empresa válido.'
        )
        return redirect('perguntas:index')

    solicitacao = Solicitacao.objects.create(
        usuario=request.user,
        servico=servico,
        descricao=descricao,
        porte_empresa=porte,
    )

    return render(
        request,
        'app_operos/solicitacao_sucesso.html',
        {'solicitacao': solicitacao}
    )

# Create your views here.