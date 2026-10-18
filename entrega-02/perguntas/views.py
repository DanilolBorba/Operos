
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.views import View
from django.utils import timezone
from django.urls import reverse

from .models import Pergunta, Resposta
from .forms import FormularioCadastroUsuario

from app_operos.views import SOLUCOES_IOT


class MainView(View):
    def get(self, request):
        lista_ultimas_questoes = Pergunta.objects.order_by(
            "-data_criacao"
        )

        solucoes = []

        if request.user.is_authenticated:
            area = (
                getattr(request.user, "area_atuacao", "") or ""
            ).strip().lower()

            solucoes = (
                SOLUCOES_IOT.get(area)
                or SOLUCOES_IOT.get("geral", [])
            )

        contexto = {
            "perguntas": lista_ultimas_questoes,
            "solucoes": solucoes,
        }

        return render(
            request,
            "perguntas/index.html",
            contexto
        )


class PerguntaView(View):
    def get(self, request, pergunta_id):
        try:
            pergunta = Pergunta.objects.get(pk=pergunta_id)
        except Pergunta.DoesNotExist:
            raise Http404("Pergunta inexistente")

        contexto = {
            "pergunta": pergunta
        }

        return render(
            request,
            "perguntas/detalhe.html",
            contexto
        )


class VotoView(View):
    def get(self, request, resposta_id):
        try:
            resposta = Resposta.objects.get(pk=resposta_id)
        except Resposta.DoesNotExist:
            raise Http404("Resposta inexistente")

        return HttpResponse(
            str(resposta) + "; votos: " + str(resposta.votos)
        )

    def post(self, request, resposta_id):
        try:
            resposta = Resposta.objects.get(pk=resposta_id)
        except Resposta.DoesNotExist:
            raise Http404("Resposta inexistente")

        resposta.votos += 1
        resposta.save()

        return redirect(
            reverse(
                "perguntas:detalhe",
                args=[resposta.pergunta.id]
            )
        )


class InserirPerguntaView(View):
    def get(self, request):
        lista_ultimas_questoes = Pergunta.objects.order_by(
            "-data_criacao"
        )

        contexto = {
            "perguntas": lista_ultimas_questoes
        }

        return render(
            request,
            "perguntas/inserir_pergunta.html",
            contexto
        )

    def post(self, request):
        if request.user.is_authenticated:
            usuario = request.user.username
        else:
            usuario = "anônimo"

        titulo = request.POST.get("titulo")
        detalhe = request.POST.get("detalhe")
        tentativa = request.POST.get("tentativa") or ""
        data_criacao = timezone.now()

        pergunta = Pergunta(
            titulo=titulo,
            detalhe=detalhe,
            tentativa=tentativa,
            data_criacao=data_criacao,
            usuario=usuario
        )

        pergunta.save()

        return redirect(
            reverse(
                "perguntas:detalhe",
                args=[pergunta.id]
            )
        )


class QuemSomosView(View):
    def get(self, request):
        return render(
            request,
            "perguntas/quem_somos.html"
        )


class InserirRespostaView(View):
    def get(self, request, pergunta_id):
        try:
            pergunta = Pergunta.objects.get(pk=pergunta_id)
        except Pergunta.DoesNotExist:
            raise Http404("Pergunta inexistente")

        contexto = {
            "pergunta": pergunta
        }

        return render(
            request,
            "perguntas/inserir_resposta.html",
            contexto
        )

    def post(self, request, pergunta_id):
        try:
            pergunta = Pergunta.objects.get(pk=pergunta_id)
        except Pergunta.DoesNotExist:
            raise Http404("Pergunta inexistente")

        if request.user.is_authenticated:
            usuario = request.user.username
        else:
            usuario = "anônimo"

        texto = request.POST.get("texto_resposta")
        data_criacao = timezone.now()

        pergunta.resposta_set.create(
            texto=texto,
            data_criacao=data_criacao,
            usuario=usuario
        )

        return redirect(
            reverse(
                "perguntas:detalhe",
                args=[pergunta.id]
            )
        )


def view_cadastro(request):
    if request.method == "POST":
        form = FormularioCadastroUsuario(request.POST)

        if form.is_valid():
            form.save()

            # Após o cadastro, o usuário precisa fazer login.
            return redirect("perguntas:login")

    else:
        form = FormularioCadastroUsuario()

    return render(
        request,
        "perguntas/cadastro.html",
        {"form": form}
    )
