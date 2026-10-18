from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UsuarioPersonalizado


class FormularioCadastroUsuario(UserCreationForm):

    class Meta:
        model = UsuarioPersonalizado
        fields = [
            'username',
            'nome_completo',
            'nome_exibicao',
            'email',
            'telefone',
            'estado',
            'empresa',
            'cpf_cnpj',
            'cargo',
            'setor',
            'area_atuacao'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'estado': 'Selecione um estado',
            'cargo': 'Selecione um cargo',
            'area_atuacao': 'Selecione uma área de atuação',
        }

        for campo, texto in placeholders.items():
            if campo not in self.fields:
                continue

            escolhas = list(self.fields[campo].choices)

            if escolhas and escolhas[0][0] == '':
                escolhas[0] = ('', texto)
            else:
                escolhas.insert(0, ('', texto))

            self.fields[campo].choices = escolhas

    def clean_cpf_cnpj(self):
        cpf_cnpj = self.cleaned_data.get('cpf_cnpj') or ''
        digitos = ''.join(filter(str.isdigit, cpf_cnpj))

        if len(digitos) not in [11, 14]:
            raise forms.ValidationError(
                "O CPF deve ter 11 dígitos ou o CNPJ deve ter 14 dígitos."
            )

        return digitos

    def clean_nome_exibicao(self):
        nome_exibicao = self.cleaned_data.get('nome_exibicao')
        nome_completo = self.cleaned_data.get('nome_completo')

        if not nome_exibicao and nome_completo:
            return nome_completo[:16]

        if nome_exibicao and len(nome_exibicao) > 16:
            raise forms.ValidationError(
                "O nome de exibição não pode ter mais de 16 caracteres."
            )

        return nome_exibicao