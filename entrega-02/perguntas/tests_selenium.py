from django.test import override_settings
from django.utils import timezone
from os import link

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select  
from webdriver_manager.chrome import ChromeDriverManager

import time

from perguntas.models import UsuarioPersonalizado, Pergunta  
from app_operos.models import Solicitacao  


class BaseTestCase(StaticLiveServerTestCase):
    """
    Classe-base que inicializa e encerra o Chrome antes e depois dos testes.
    O StaticLiveServerTestCase disponibiliza um servidor temporário e um
    banco de dados isolado para cada teste.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        opts = Options()
        opts.add_argument("--headless")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--window-size=1280,800")

        service = Service(ChromeDriverManager().install())
        cls.driver = webdriver.Chrome(service=service, options=opts)
        cls.wait = WebDriverWait(cls.driver, 10)

    def setUp(self):  
        super().setUp()  
        self.driver.delete_all_cookies() 
    
    def tearDown(self):
        #time.sleep(8)
        super().tearDown() 

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "driver"):
            cls.driver.quit()
        super().tearDownClass()

    def abrir_pagina(self, caminho="/"):  #abre uma url relativa ao servidor temporário do teste 
        self.driver.get(self.live_server_url + caminho)
        print("URL REAL DO SELENIUM:", self.driver.current_url)
        #time.sleep(3)  

    def criar_usuario(self, username, email, senha="SenhaForte#2026", **dados):  
        return UsuarioPersonalizado.objects.create_user(  
            username=username,  
            email=email,  
            password=senha,  
            nome_completo=dados.get("nome_completo", "Pessoa Teste"),  
            nome_exibicao=dados.get("nome_exibicao", "Pessoa"),  
            telefone=dados.get("telefone", "81987654321"),  
            estado=dados.get("estado", "PE"),  
            empresa=dados.get("empresa", "Empresa Teste"),  
            cpf_cnpj=dados.get("cpf_cnpj", "12345678901"),  
            cargo=dados.get("cargo", "ceo"),  
            setor=dados.get("setor", "Tecnologia"),  
            area_atuacao=dados.get("area_atuacao", "industria"),  
        )  

    def fazer_login_pelo_navegador(self, username, senha="SenhaForte#2026"):  
        self.abrir_pagina("/login/")  
        self.wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)  
        self.driver.find_element(By.NAME, "password").send_keys(senha)  
        self.driver.find_element(By.CSS_SELECTOR, "form.auth-form button[type='submit']").click()  
        self.wait.until(EC.url_to_be(self.live_server_url + "/"))  

    
    
    def preencher_cadastro(self, username, email, **dados):
        valores = {
            "username": username,
            "email": email,
            "password1": "SenhaForte#2026",
            "password2": "SenhaForte#2026",
            "nome_completo": "Pessoa Teste",
            "nome_exibicao": "Pessoa",
            "telefone": "81987654321",
            "estado": "PE",
            "empresa": "Empresa Teste",
            "cpf_cnpj": "12345678901",
            "cargo": "ceo",
            "setor": "Tecnologia",
            "area_atuacao": "industria",
        }

        valores.update(dados)
        self.abrir_pagina("/cadastro/")

        for nome, valor in valores.items():
            campo = self.wait.until(
                EC.presence_of_element_located((By.NAME, nome))
            )

            if campo.tag_name.lower() == "select":
                Select(campo).select_by_value(valor)
            else:
                if nome == "nome_exibicao" and len(valor) > 16:
                    self.driver.execute_script(
                        "arguments[0].removeAttribute('maxlength');",
                        campo
                    )

                campo.send_keys(valor)

        formulario = self.wait.until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "form.auth-form"
            ))
        )

        botao = formulario.find_element(
            By.CSS_SELECTOR,
            "button[type='submit']"
        )

        self.driver.execute_script(
            "arguments[0].requestSubmit(arguments[1]);",
            formulario,
            botao
        )

        self.wait.until(
            lambda navegador: (
                navegador.current_url == self.live_server_url + "/"
                or len(
                    navegador.find_elements(
                        By.CSS_SELECTOR,
                        ".form-alert"
                    )
                ) > 0
            )
        )


 

              

    def fazer_login_administrativo(self, username, senha="SenhaForte#2026"):
        self.abrir_pagina("/admin/login/")

        self.wait.until(
            EC.presence_of_element_located((By.NAME, "username"))
        ).send_keys(username)

        self.driver.find_element(By.NAME, "password").send_keys(senha)

        self.driver.find_element(By.TAG_NAME, "form").submit()

        self.wait.until(
            EC.url_to_be(self.live_server_url + "/admin/")
        )
  


class testeH4_solicitacaoServico(BaseTestCase):

    def teste4_solicitacaoServico_com_sucesso(self):
        usuario = self.criar_usuario("cliente_hu04", "cliente.hu04@example.com")

        self.fazer_login_pelo_navegador(usuario.username)

        formulario = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".recommendation-card form")))

        nome_servico = formulario.find_element(By.NAME, "servico").get_attribute("value")

        Select(formulario.find_element(By.NAME, "porte_empresa")).select_by_value("medio")

        formulario.find_element(By.NAME, "descricao").send_keys("Necessidade de monitoramento para teste automatizado.")

        botao = formulario.find_element(By.CSS_SELECTOR, "button[type='submit']")

        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});",
            botao
        )

        self.wait.until(EC.element_to_be_clickable(botao)).click()

        self.wait.until(
            EC.text_to_be_present_in_element(
                (By.TAG_NAME, "body"),
                "Solicitação registrada com sucesso!"
            )
        )

        body = self.driver.find_element(By.TAG_NAME, "body")

        solicitacao = Solicitacao.objects.get(
            usuario=usuario,
            servico=nome_servico
        )

        self.assertIn(nome_servico, body.text)
        self.assertIn("Médio", body.text)
        self.assertIn("PROTOCOLO", body.text)
        self.assertIn(str(solicitacao.protocolo), body.text)

    def teste4_solicitacaoServico_exige_login(self):
        self.abrir_pagina("/servicos/solicitar/")

        self.wait.until(EC.url_contains("/login/"))

        self.assertIn("/login/", self.driver.current_url)
 


class teste5_cadastro(BaseTestCase):

    
    def teste5_cadastro_com_sucesso(self):
        username = "cadastro_hu05_valido"
        email = "cadastro.hu05.valido@example.com"

        self.preencher_cadastro(username, email)

        self.wait.until(
            EC.url_to_be(self.live_server_url + "/")
        )

        self.assertTrue(
            UsuarioPersonalizado.objects.filter(
                username=username,
                email=email
            ).exists()
        )

        solucoes = self.wait.until(
            EC.presence_of_element_located((
                By.ID,
                "solucoes"
            ))
        )

        texto = solucoes.get_attribute("textContent")

        self.assertIn("Soluções IoT recomendadas", texto)

        recomendacoes = solucoes.find_elements(
            By.CLASS_NAME,
            "recommendation-card"
        )

        self.assertGreater(len(recomendacoes), 0)


    def teste5_cadastro_nome_exibicao_acima_de_16_caracteres(self):
        self.preencher_cadastro(
            "cadastro_hu05_nome_longo",
            "cadastro.hu05.nome.longo@example.com",
            nome_exibicao="NomeDeExibicaoMaiorQue16",
        )

        erro = self.wait.until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "[name='nome_exibicao'] + .field-error"
            ))
        )

        self.assertIn(
            "O nome de exibição não pode ter mais de 16 caracteres.",
            erro.get_attribute("textContent")
        )

        self.assertFalse(
            UsuarioPersonalizado.objects.filter(
                username="cadastro_hu05_nome_longo"
            ).exists()
        )

    def teste5_cadastro_cpf_cnpj_invalido(self):
        self.preencher_cadastro(
            "cadastro_hu05_documento_invalido",
            "cadastro.hu05.documento@example.com",
            cpf_cnpj="123",
        )

        erro = self.wait.until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "[name='cpf_cnpj'] + .field-error"
            ))
        )

        self.assertIn(
            "Informe um CPF com 11 dígitos ou um CNPJ com 14 dígitos.",
            erro.get_attribute("textContent")
        )

        self.assertFalse(
            UsuarioPersonalizado.objects.filter(
                username="cadastro_hu05_documento_invalido"
            ).exists()
        )

    def teste5_cadastro_email_ja_existente(self):
        self.criar_usuario(
            "usuario_email_existente",
            "email.existente@example.com"
        )

        self.preencher_cadastro(
            "cadastro_hu05_email_repetido",
            "email.existente@example.com",
        )

        erro = self.wait.until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "[name='email'] + .field-error"
            ))
        )

        self.assertIn(
            "Este e-mail já está cadastrado.",
            erro.get_attribute("textContent")
        )

        self.assertFalse(
            UsuarioPersonalizado.objects.filter(
                username="cadastro_hu05_email_repetido"
            ).exists()
        )  


class teste6_painelAdm(BaseTestCase):  #testes historia 6 -> painel adm de solicitações por porte

    def criar_administrador(self): 
        administrador = self.criar_usuario("admin_hu06", "admin.hu06@example.com") 
        administrador.is_staff = True 
        administrador.is_superuser = True 
        administrador.save(update_fields=["is_staff", "is_superuser"]) 
        return administrador 

    def abrir_painel_solicitacoes(self, administrador): 
        self.fazer_login_administrativo(administrador.username) 
        self.abrir_pagina("/admin/app_operos/solicitacao/") 
        self.wait.until(EC.presence_of_element_located((By.ID, "content"))) 

    def teste6_painelAdm_exibe_solicitacoes_agrupadas_por_porte(self): 
        administrador = self.criar_administrador() 
        for indice in range(2): 
            Solicitacao.objects.create(usuario=administrador, porte_empresa="pequeno", servico=f"Serviço pequeno {indice}") 
        Solicitacao.objects.create(usuario=administrador, porte_empresa="medio", servico="Serviço médio") 
        Solicitacao.objects.create(usuario=administrador, porte_empresa="grande", servico="Serviço grande") 
        self.abrir_painel_solicitacoes(administrador) 
        pequeno = self.driver.find_element(By.XPATH, "//h3[normalize-space()='Pequeno porte']/following-sibling::h1[1]").text 
        medio = self.driver.find_element(By.XPATH, "//h3[normalize-space()='Médio porte']/following-sibling::h1[1]").text 
        grande = self.driver.find_element(By.XPATH, "//h3[normalize-space()='Grande porte']/following-sibling::h1[1]").text 
        self.assertEqual(pequeno, "2") 
        self.assertEqual(medio, "1") 
        self.assertEqual(grande, "1") 

    def teste6_painelAdm_informa_quando_nao_existirem_solicitacoes(self): 
        administrador = self.criar_administrador() 
        self.abrir_painel_solicitacoes(administrador) 
        body = self.driver.find_element(By.TAG_NAME, "body") 
        self.assertIn("Não existem pedidos de serviços registrados.", body.text)
class teste1_conhecendoIoT(BaseTestCase):
    def teste1_home_apresenta_conceito_beneficios_e_dados(self):
        self.abrir_pagina("/")
        introducao = self.wait.until(
            EC.presence_of_element_located((By.ID, "conhecendo-iot"))
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            introducao
        )
        #time.sleep(4)
        texto = introducao.get_attribute("textContent")
        self.assertIn("O que é Internet das Coisas?", texto)
        self.assertIn("conectar objetos", texto)
        self.assertIn("coletar", texto)
        self.assertIn("Sensores", texto)
        self.assertIn("Conectividade", texto)
        beneficios = self.driver.find_elements(
            By.CSS_SELECTOR, ".innovation-card"
        )
        self.assertGreaterEqual(len(beneficios), 3)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            beneficios[0]
        )
        #time.sleep(4)
        texto_beneficios = self.driver.find_element(
            By.ID, "inovacoes"
        ).get_attribute("textContent")
        self.assertIn("Monitoramento inteligente", texto_beneficios)
        self.assertIn("Análise de dados", texto_beneficios)
        self.assertIn("Alertas em tempo real", texto_beneficios)
        etapas = self.driver.find_elements(
            By.CSS_SELECTOR, ".steps-grid .step-card"
        )
        self.assertEqual(len(etapas), 4)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            etapas[0]
        )
        time.sleep(4)
        texto_etapas = self.driver.find_element(
            By.CLASS_NAME, "steps-grid"
        ).get_attribute("textContent")
        self.assertIn("Sensores", texto_etapas)
        self.assertIn("Gateway", texto_etapas)
        self.assertIn("Nuvem", texto_etapas)
        self.assertIn("Decisões inteligentes", texto_etapas)
class teste2_catalogoSolucoes(BaseTestCase):
    def teste2_catalogo_apresenta_solucoes_completas(self):
        self.abrir_pagina("/servicos/")
        titulo = self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        self.assertIn("Soluções IoT", titulo.text)
        grupos = self.driver.find_elements(
            By.CLASS_NAME, "grupo-solucoes"
        )
        self.assertEqual(len(grupos), 7)
        solucoes = self.driver.find_elements(
            By.CSS_SELECTOR, ".grupo-solucoes .homebox"
        )
        self.assertEqual(len(solucoes), 14)
        for solucao in solucoes:
            nome = solucao.find_element(By.TAG_NAME, "h3")
            descricao = solucao.find_element(By.TAG_NAME, "p")
            self.assertTrue(nome.get_attribute("textContent").strip())
            self.assertTrue(descricao.get_attribute("textContent").strip())
            titulos = [
                elemento.get_attribute("textContent").strip()
                for elemento in solucao.find_elements(By.TAG_NAME, "h4")
            ]
            self.assertIn("Funcionalidades", titulos)
            self.assertIn("Aplicações", titulos)
            self.assertIn("Benefícios", titulos)
            listas = solucao.find_elements(By.TAG_NAME, "ul")
            self.assertEqual(len(listas), 3)
            for lista in listas:
                itens = lista.find_elements(By.TAG_NAME, "li")
                self.assertGreater(len(itens), 0)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            solucoes[0]
        )
        #time.sleep(4)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            solucoes[-1]
        )
        #time.sleep(4)