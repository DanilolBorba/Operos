from django.shortcuts import render
import re
from django.http import HttpResponse, Http404
from .models import Pergunta, Resposta

from django.core.validators import validate_email

from django.views import View

from django.utils import timezone
from django.shortcuts import redirect
from django.urls import reverse

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import UsuarioPersonalizado, ESTADO_ESCOLHA, CARGO_ESCOLHA, AREA_ATUACAO_ESCOLHA
from app_operos.views import SOLUCOES_IOT


class MainView(View):
    def get(self, request):
        lista_ultimas_questoes = Pergunta.objects.order_by("-data_criacao")

        solucoes = []

        if request.user.is_authenticated:
            area = (
                getattr(request.user, 'area_atuacao', '') or ''
            ).strip().lower()

            solucoes = (
                SOLUCOES_IOT.get(area)
                or SOLUCOES_IOT['geral']
            )

        contexto = {
            'perguntas': lista_ultimas_questoes,
            'solucoes': solucoes
        }

        return render(request, 'perguntas/index.html', contexto)


class PerguntaView(View):
    def get(self, request, pergunta_id):
        try:
            pergunta = Pergunta.objects.get(pk=pergunta_id)
        except Pergunta.DoesNotExist:
            raise Http404("Pergunta inexistente")
        contexto = {'pergunta' : pergunta}
        return render(request, 'perguntas/detalhe.html', contexto)

class VotoView(View):
    def get(self, request, resposta_id):
        try:
            resposta = Resposta.objects.get(pk=resposta_id)
        except Resposta.DoesNotExist:
            raise Http404("Resposta inexistente")
        return HttpResponse(str(resposta) + "; votos: " + str(resposta.votos))

    def post(self, request, resposta_id):
        try:
            resposta = Resposta.objects.get(pk=resposta_id)
        except Resposta.DoesNotExist:
            raise Http404("Resposta inexistente")
        resposta.votos += 1
        resposta.save()
        return redirect(reverse('perguntas:detalhe', args=[resposta.pergunta.id]))

class InserirPerguntaView(View):
    def get(self, request):
        lista_ultimas_questoes = Pergunta.objects.order_by("-data_criacao")
        contexto = {'perguntas': lista_ultimas_questoes}

        return render(
            request,
            'perguntas/inserir_pergunta.html',
            contexto
        )

    def post(self, request):
        if request.user.is_authenticated:
            usuario = request.user.username
        else:
            usuario = 'anônimo'
        titulo = request.POST.get('titulo')
        detalhe = request.POST.get('detalhe')
        tentativa = request.POST.get('tentativa') or ''
        data_criacao = timezone.now()
        
        pergunta = Pergunta(titulo=titulo, detalhe=detalhe, 
tentativa=tentativa, 	data_criacao=data_criacao, usuario=usuario)
        pergunta.save()

        return redirect(reverse('perguntas:detalhe', args=[pergunta.id]))

class QuemSomosView(View):
    def get(self, request):
        return render(request, 'perguntas/quem_somos.html')
    
class InserirRespostaView(View):
    def get(self, request, pergunta_id):
        try:
            pergunta = Pergunta.objects.get(pk=pergunta_id)
        except Pergunta.DoesNotExist:
            raise Http404("Pergunta inexistente")
        contexto = {'pergunta' : pergunta}
        return render(request, 'perguntas/inserir_resposta.html', contexto)

    def post(self, request, pergunta_id):
        try:
            pergunta = Pergunta.objects.get(pk=pergunta_id)
        except Pergunta.DoesNotExist:
            raise Http404("Pergunta inexistente")

        if request.user.is_authenticated:
            usuario = request.user.username
        else:
            usuario = 'anônimo'
        texto = request.POST.get('texto_resposta')
        data_criacao = timezone.now()
        
        pergunta.resposta_set.create(texto=texto, data_criacao=data_criacao, usuario=usuario)

        return redirect(reverse('perguntas:detalhe', args=[pergunta.id]))
# Create your views here.
def view_cadastro(request):
    campos = [
        'username', 'email', 'password1', 'password2',
        'nome_completo', 'nome_exibicao', 'telefone', 'estado',
        'empresa', 'cpf_cnpj', 'cargo', 'setor', 'area_atuacao',
    ]
    dados = {campo: '' for campo in campos}
    erros = {}

    if request.method == 'POST':
        dados = {campo: (request.POST.get(campo) or '').strip() for campo in campos}
        senha = request.POST.get('password1') or ''
        confirmar_senha = request.POST.get('password2') or ''

        
        campos_obrigatorios = [
            'username',
            'email',
            'nome_completo',
            'telefone',
            'estado',
            'empresa',
            'cpf_cnpj',
            'cargo',
            'setor',
            'area_atuacao',
        ]

        for campo in campos_obrigatorios:
            if not dados[campo]:
                erros[campo] = 'Este campo é obrigatório.'

        if not dados['username']:
            erros['username'] = 'Informe um nome de usuário.'
        elif UsuarioPersonalizado.objects.filter(username=dados['username']).exists():
            erros['username'] = 'Esse nome de usuário já está em uso.'

        if not dados['email']:
            erros['email'] = 'Informe seu e-mail.'
        elif len(dados['email']) > 254:
            erros['email'] = 'O e-mail deve ter no máximo 254 caracteres.'
        elif UsuarioPersonalizado.objects.filter(
            email__iexact=dados['email']
        ).exists():
            erros['email'] = 'Este e-mail já está cadastrado.'
        else:
            try:
                validate_email(dados['email'])
            except ValidationError:
                erros['email'] = 'Informe um e-mail válido.'


        if not senha:
            erros['password1'] = 'Informe uma senha.'
        if senha != confirmar_senha:
            erros['password2'] = 'As senhas não coincidem.'


        cpf_cnpj = dados['cpf_cnpj']

        if cpf_cnpj:
            digitos = ''.join(filter(str.isdigit, cpf_cnpj))

            if len(digitos) not in (11, 14):
                erros['cpf_cnpj'] = (
                    'Informe um CPF com 11 dígitos '
                    'ou um CNPJ com 14 dígitos.'
                )
            elif len(set(digitos)) == 1:
                erros['cpf_cnpj'] = 'Informe um CPF/CNPJ válido.'
            else:
                dados['cpf_cnpj'] = digitos

        
        if len(dados['nome_exibicao']) > 16:
            erros['nome_exibicao'] = (
                'O nome de exibição não pode ter mais de 16 caracteres.'
            )

        opcoes = {
            'estado': dict(ESTADO_ESCOLHA),
            'cargo': dict(CARGO_ESCOLHA),
            'area_atuacao': dict(AREA_ATUACAO_ESCOLHA),
        }
        for campo, escolhas in opcoes.items():
            if dados[campo] and dados[campo] not in escolhas:
                erros[campo] = 'Selecione uma opção válida.'

        if len(dados['nome_completo']) > 32:
            erros['nome_completo'] = 'O nome completo deve ter no máximo 32 caracteres.'
        if len(dados['telefone']) > 20:
            erros['telefone'] = 'O telefone deve ter no máximo 20 caracteres.'
        if len(dados['empresa']) > 255:
            erros['empresa'] = 'O nome da empresa deve ter no máximo 255 caracteres.'
        if len(dados['setor']) > 100:
            erros['setor'] = 'O setor deve ter no máximo 100 caracteres.'

        usuario = UsuarioPersonalizado(
            username=dados['username'],
            email=dados['email'],
            nome_completo=dados['nome_completo'],
            nome_exibicao=dados['nome_exibicao'] or None,
            telefone=dados['telefone'],
            estado=dados['estado'],
            empresa=dados['empresa'],
            cpf_cnpj=dados['cpf_cnpj'],
            cargo=dados['cargo'],
            setor=dados['setor'],
            area_atuacao=dados['area_atuacao'],
        )

        if senha and senha == confirmar_senha:
            try:
                validate_password(senha, user=usuario)
            except ValidationError as exc:
                erros['password1'] = ' '.join(exc.messages)

        if not erros:
            usuario.set_password(senha)
            usuario.save()
            login(request, usuario)
            return redirect('perguntas:index')

    contexto = {
        'dados': dados,
        'erros': erros,
        'estados': ESTADO_ESCOLHA,
        'cargos': CARGO_ESCOLHA,
        'areas_atuacao': AREA_ATUACAO_ESCOLHA,
    }
    return render(request, 'perguntas/cadastro.html', contexto)


def view_login(request):
    erro_login = False
    if request.method == 'POST':
        username = (request.POST.get('username') or '').strip()
        password = request.POST.get('password') or ''
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            destino = request.POST.get('next') or 'perguntas:index'
            if not destino.startswith('/') or destino.startswith('//'):
                destino = reverse('perguntas:index')
            return redirect(destino)
        erro_login = True

    return render(request, 'perguntas/login.html', {
        'erro_login': erro_login,
        'next': request.GET.get('next', ''),
    })