from django.urls import path
from django.contrib.auth import views as auth_views
from .views import view_cadastro
from . import views 

app_name = 'perguntas'
urlpatterns = [
    # ex: /forum/
    path("", views.MainView.as_view(), name="index"),
    # ex: /forum/5/
    path("<int:pergunta_id>/", views.PerguntaView.as_view(), name="detalhe"),
    # ex: /forum/5/voto/
    path("<int:resposta_id>/voto/", views.VotoView.as_view(), name="voto"),
    # ex: /forum/inserir/
    path("inserir/", views.InserirPerguntaView.as_view(), name="inserir_pergunta"),
    # ex: /forum/5/resposta/
    path("<int:pergunta_id>/resposta/",
         views.InserirRespostaView.as_view(), name="inserir_resposta"),
    path('quem-somos/', views.QuemSomosView.as_view(), name='quem_somos'),
    path('home/', views.MainView.as_view(), name='home'),

    #partes login
    path('cadastro/', view_cadastro, name='cadastro'),
    path('login/', auth_views.LoginView.as_view(template_name='perguntas/login.html', next_page='perguntas:index'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='perguntas:index'), name='logout'),

]