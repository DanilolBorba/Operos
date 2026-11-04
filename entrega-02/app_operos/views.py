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
            ),
            'funcionalidades': [
                'Medição contínua de temperatura e umidade',
                'Registro das condições ambientais ao longo do tempo'
            ],
            'aplicacoes': [
                'Câmaras frias e armazenamento de alimentos',
                'Armazenamento e transporte de medicamentos'
            ],
            'beneficios': [
                'Ajuda a evitar perdas por armazenamento inadequado',
                'Facilita o acompanhamento das condições de conservação'
            ]
        },
        {
            'nome': 'Alertas de conservação',
            'descricao': (
                'Identifique alterações nas condições '
                'de conservação dos produtos.'
            ),
            'funcionalidades': [
                'Identificação de alterações nas condições ambientais',
                'Emissão de alertas quando os limites definidos são ultrapassados'
            ],
            'aplicacoes': [
                'Armazéns de produtos perecíveis',
                'Transporte refrigerado de alimentos e medicamentos'
            ],
            'beneficios': [
                'Permite uma resposta mais rápida a problemas de conservação',
                'Ajuda a reduzir desperdícios e perdas de produtos'
            ]
        },
    ],

    'industria': [
        {
            'nome': 'Monitoramento de máquinas',
            'descricao': (
                'Acompanhe dados operacionais dos equipamentos '
                'e identifique possíveis anomalias.'
            ),
            'funcionalidades': [
                'Coleta de dados sobre o funcionamento das máquinas',
                'Identificação de comportamentos operacionais incomuns'
            ],
            'aplicacoes': [
                'Linhas de produção industrial',
                'Equipamentos utilizados em processos de fabricação'
            ],
            'beneficios': [
                'Auxilia na identificação antecipada de falhas',
                'Contribui para reduzir paradas inesperadas dos equipamentos'
            ]
        },
        {
            'nome': 'Monitoramento da produção',
            'descricao': (
                'Monitore variáveis dos processos produtivos '
                'por meio de sensores conectados.'
            ),
            'funcionalidades': [
                'Coleta de informações dos processos produtivos',
                'Acompanhamento de indicadores operacionais'
            ],
            'aplicacoes': [
                'Fábricas e unidades industriais',
                'Linhas de montagem e processamento de materiais'
            ],
            'beneficios': [
                'Facilita a identificação de problemas na produção',
                'Apoia decisões voltadas à eficiência operacional'
            ]
        },
    ],

    'utilities': [
        {
            'nome': 'Monitoramento de consumo',
            'descricao': (
                'Acompanhe o consumo de água, gás e energia.'
            ),
            'funcionalidades': [
                'Medição do consumo de recursos em diferentes períodos',
                'Registro e acompanhamento dos dados coletados'
            ],
            'aplicacoes': [
                'Empresas com grande consumo de energia elétrica',
                'Condomínios e instalações comerciais'
            ],
            'beneficios': [
                'Facilita a identificação de desperdícios',
                'Auxilia no planejamento e controle dos gastos operacionais'
            ]
        },
        {
            'nome': 'Detecção de anomalias',
            'descricao': (
                'Identifique variações incomuns nas medições '
                'dos recursos monitorados.'
            ),
            'funcionalidades': [
                'Análise de alterações nos padrões de consumo',
                'Identificação de medições fora dos limites esperados'
            ],
            'aplicacoes': [
                'Sistemas de distribuição de água',
                'Redes internas de energia e gás'
            ],
            'beneficios': [
                'Auxilia na identificação de possíveis vazamentos e falhas',
                'Contribui para a redução de desperdícios de recursos'
            ]
        },
    ],

    'cidades_inteligentes': [
        {
            'nome': 'Monitoramento ambiental urbano',
            'descricao': (
                'Acompanhe indicadores ambientais por '
                'meio de sensores conectados.'
            ),
            'funcionalidades': [
                'Coleta de dados de temperatura e qualidade do ar',
                'Acompanhamento das condições ambientais da cidade'
            ],
            'aplicacoes': [
                'Parques e espaços públicos',
                'Regiões urbanas com grande circulação de pessoas'
            ],
            'beneficios': [
                'Fornece informações para o planejamento urbano',
                'Apoia ações voltadas à qualidade ambiental'
            ]
        },
        {
            'nome': 'Monitoramento de mobilidade',
            'descricao': (
                'Colete dados relacionados à mobilidade urbana.'
            ),
            'funcionalidades': [
                'Coleta de informações sobre o fluxo de veículos',
                'Acompanhamento de indicadores de circulação urbana'
            ],
            'aplicacoes': [
                'Avenidas e cruzamentos movimentados',
                'Sistemas de gestão do trânsito'
            ],
            'beneficios': [
                'Auxilia na identificação de pontos de congestionamento',
                'Apoia o planejamento de melhorias na mobilidade urbana'
            ]
        },
    ],

    'edificios_inteligentes': [
        {
            'nome': 'Monitoramento de ambientes',
            'descricao': (
                'Acompanhe temperatura, umidade e outras '
                'condições dos ambientes.'
            ),
            'funcionalidades': [
                'Medição das condições ambientais internas',
                'Registro de variações de temperatura e umidade'
            ],
            'aplicacoes': [
                'Escritórios e ambientes corporativos',
                'Hospitais e edifícios comerciais'
            ],
            'beneficios': [
                'Ajuda a manter condições ambientais adequadas',
                'Apoia melhorias no conforto dos ocupantes'
            ]
        },
        {
            'nome': 'Monitoramento de sistemas prediais',
            'descricao': (
                'Monitore equipamentos e instalações '
                'do edifício.'
            ),
            'funcionalidades': [
                'Coleta de dados operacionais de equipamentos prediais',
                'Acompanhamento do funcionamento de sistemas instalados'
            ],
            'aplicacoes': [
                'Sistemas de climatização e ventilação',
                'Instalações elétricas e hidráulicas de edifícios'
            ],
            'beneficios': [
                'Facilita o acompanhamento da infraestrutura predial',
                'Contribui para a identificação de necessidades de manutenção'
            ]
        },
    ],

    'agronegocio': [
        {
            'nome': 'Monitoramento agrícola',
            'descricao': (
                'Acompanhe condições ambientais relevantes '
                'para as atividades agrícolas.'
            ),
            'funcionalidades': [
                'Medição da umidade do solo e da temperatura ambiente',
                'Acompanhamento das condições das áreas de cultivo'
            ],
            'aplicacoes': [
                'Plantações e propriedades rurais',
                'Estufas e sistemas de cultivo controlado'
            ],
            'beneficios': [
                'Auxilia no uso mais eficiente da água',
                'Apoia decisões relacionadas ao manejo das plantações'
            ]
        },
        {
            'nome': 'Monitoramento operacional',
            'descricao': (
                'Monitore equipamentos e processos agrícolas.'
            ),
            'funcionalidades': [
                'Coleta de informações sobre equipamentos agrícolas',
                'Acompanhamento de indicadores das operações rurais'
            ],
            'aplicacoes': [
                'Máquinas e equipamentos utilizados no campo',
                'Sistemas de irrigação e outras operações agrícolas'
            ],
            'beneficios': [
                'Facilita a identificação de falhas operacionais',
                'Contribui para melhorar o planejamento das atividades rurais'
            ]
        },
    ],

    'geral': [
        {
            'nome': 'Monitoramento inteligente com sensores IoT',
            'descricao': (
                'Monitore condições e variáveis importantes '
                'da operação da empresa usando sensores conectados.'
            ),
            'funcionalidades': [
                'Coleta de dados por dispositivos e sensores conectados',
                'Acompanhamento de variáveis operacionais'
            ],
            'aplicacoes': [
                'Empresas de diferentes setores',
                'Ambientes que necessitam de monitoramento contínuo'
            ],
            'beneficios': [
                'Amplia a visibilidade sobre as operações da empresa',
                'Apoia a identificação de problemas e oportunidades de melhoria'
            ]
        },
        {
            'nome': 'Coleta e acompanhamento de dados IoT',
            'descricao': (
                'Acompanhe dados coletados por dispositivos IoT '
                'para identificar alterações nos processos.'
            ),
            'funcionalidades': [
                'Registro de informações recebidas dos dispositivos',
                'Organização de dados para acompanhamento operacional'
            ],
            'aplicacoes': [
                'Processos industriais e comerciais',
                'Operações que dependem de dados para tomada de decisões'
            ],
            'beneficios': [
                'Facilita o acesso a informações operacionais',
                'Contribui para decisões baseadas em dados'
            ]
        },
    ],
}



def index(request):
    nomes_areas = {
        'cadeia_fria': 'Cadeia Fria',
        'industria': 'Indústria 4.0',
        'utilities': 'Utilities',
        'cidades_inteligentes': 'Cidades Inteligentes',
        'edificios_inteligentes': 'Edifícios Inteligentes',
        'agronegocio': 'Agronegócio',
        'geral': 'Soluções Gerais'
    }

    grupos = []

    for area, solucoes in SOLUCOES_IOT.items():
        grupos.append({
            'nome': nomes_areas[area],
            'solucoes': solucoes
        })

    return render(
        request,
        'app_operos/catalogo.html',
        {'grupos': grupos}
    )


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