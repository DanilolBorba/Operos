from django.urls import path
from . import views
app_name = 'app_operos' 

urlpatterns = [
    path("", views.index),
    path('solicitar/', views.solicitar_servico, name='solicitar_servico'),
]
