"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from perguntas import views
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app_operos/', include("app_operos.urls")),

    # paginas do site:
    path('home/', views.MainView.as_view(), name='home'),
    path('quem-somos/', views.QuemSomosView.as_view(), name='quem_somos'),

    # funcionalidades (ver pergunta, votar, etc.):
    path('perguntas/', include('perguntas.urls')),

    path('', RedirectView.as_view(url='/home/', permanent=False), name='inicio'),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)