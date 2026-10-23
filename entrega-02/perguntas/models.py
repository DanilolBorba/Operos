from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models

class Pergunta(models.Model):
    titulo = models.CharField(max_length=200)
    detalhe = models.TextField()
    tentativa = models.TextField()
    data_criacao = models.DateTimeField("Criado em ")
    usuario = models.CharField(max_length=200, null=False, default="anônimo")

    def __str__(self):
        return "[" + str(self.id) + "] " + self.titulo
    
    def foi_publicado_recentemente(self):
        return self.data_criacao >= timezone.now() - datetime.timedelta(days=1)

    def string_detalhada(self):
        return "id: " + str(self.id) + "; titulo: " + self.titulo + "; detalhe: " + self.detalhe + "; tentativa: " + self.tentativa + "; data criação: " + str(self.data_criacao) + "; usuario: " + self.usuario


class Resposta(models.Model):
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    texto = models.TextField()
    votos = models.IntegerField(default=0)
    data_criacao = models.DateTimeField("Criado em ")
    usuario = models.CharField(max_length=200, default="anônimo")


    def __str__(self):
        return "[" + str(self.id) + "] " + self.texto
    
    def foi_publicado_recentemente(self):
        return self.data_criacao >= timezone.now() - datetime.timedelta(days=1)
# Create your models here.


ESTADO_ESCOLHA = [
    ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
    ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
    ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
]

CARGO_ESCOLHA = [
    ('ceo', 'CEO'),
    ('gerente', 'Gerente'),
    ('diretora', 'Diretora'),
    ('presidente', 'Presidente'),
    ('vice-presidente', 'Vice-Presidente'),
    ('analista', 'Analista'),
    ('sindico', 'Síndico'),
    ('uso_pessoal', 'Uso Pessoal'),
]

AREA_ATUACAO_ESCOLHA = [
    ('cadeia_fria', 'Cadeia fria (monitoramento de temperatura e humidade constante)'),
    ('industria', 'Indústria 4.0'),
    ('utilities', 'Utilities (medição contínua de água, gás e energia)'),
    ('cidades_inteligentes', 'Cidades inteligentes (monitoramento urbano para clima, qualidade ambiental e mobilidade)'),
    ('edificios_inteligentes', 'Edifícios inteligentes (monitoramento de ambientes e sistemas prediais)'),
    ('agronegocio', 'Agronegócio (monitoramento de condições ambientais e operacionais)'),
]

class UsuarioPersonalizado(AbstractUser):
    nome_completo = models.CharField(max_length=32, blank=True, null=True)
    nome_exibicao = models.CharField(max_length=16, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    estado = models.CharField(max_length=2, choices=ESTADO_ESCOLHA, blank=True, null=True)
    empresa = models.CharField(max_length=255, blank=True, null=True)
    cpf_cnpj = models.CharField(max_length=14, blank=True, null=True)
    cargo = models.CharField(max_length=50, choices=CARGO_ESCOLHA, blank=True, null=True)
    setor = models.CharField(max_length=100, blank=True, null=True)
    area_atuacao = models.CharField(max_length=100, choices=AREA_ATUACAO_ESCOLHA, blank=True, null=True)

    def save(auto_self, *args, **kwargs):
        if not auto_self.nome_exibicao:
            auto_self.nome_exibicao = ((auto_self.nome_completo or '')[:16] or None)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username