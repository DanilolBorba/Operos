# Contribuindo com o Operos

Antes de tudo, agradecemos por dedicar seu tempo para contribuir! :)

Todos os tipos de contribuição são incentivados e valorizados. Consulte o [Índice](#índice) para conhecer as diferentes maneiras de ajudar e obter detalhes sobre como este projeto gerencia as contribuições. Leia a seção correspondente antes de realizar sua contribuição. Isso facilitará bastante o trabalho dos mantenedores e tornará a experiência mais tranquila para todos os envolvidos. A gente aguarda suas contribuições com entusiasmo!

> E se você gosta do projeto, mas simplesmente não tem tempo para contribuir, não tem problema. Existem outras maneiras simples de apoiar o projeto e demonstrar seu apreço, e também ficaremos muito felizes com elas:
> - Favorite o projeto
> - Publique sobre ele no Twitter ou em outras redes sociais
> - Faça referência a este projeto no README do seu próprio projeto
> - Mencione o projeto em encontros locais e conte aos seus amigos e colegas sobre ele

## Índice

- [Tenho uma dúvida](#tenho-uma-dúvida)
- [Quero contribuir](#quero-contribuir)
- [Relatando bugs](#relatando-bugs)
- [Sugerindo melhorias](#sugerindo-melhorias)
- [Mensagens de commit](#mensagens-de-commit)


## Tenho uma dúvida

> Se você deseja fazer uma pergunta, presumimos que já tenha consultado a [Documentação](https://github.com/DanilolBorba/Operos/) disponível.

Antes de fazer uma pergunta, recomendamos pesquisar [Issues](https://github.com/DanilolBorba/Operos/issues) existentes que possam ajudar. Caso encontre uma issue adequada, mas ainda precise de esclarecimentos, você pode publicar sua pergunta nela. Também é recomendável pesquisar primeiro na internet por respostas.

Se, mesmo assim, você ainda sentir necessidade de fazer uma pergunta ou obter esclarecimentos, recomendamos que:

- Abra uma [Issue](https://github.com/DanilolBorba/Operos/issues/new);
- Dê o máximo de contexto possível sobre o problema que está enfrentando.

Em seguida, cuidaremos da questão o mais rápido possível.


## Quero contribuir

> ### Aviso legal 
> Ao contribuir com este projeto, você deve concordar que é o autor de 100% do conteúdo enviado, que possui os direitos necessários sobre esse conteúdo e que o material contribuído poderá ser disponibilizado sob a licença do projeto.

### Relatando bugs


#### Antes de enviar um relato de bug 🚨

Pedimos que investigue cuidadosamente, reúna informações e descreva o problema em detalhes no seu relato, *evitanto que outras pessoas precisem entrar em contato com você para solicitar mais informações*. Siga as etapas abaixo antecipadamente para nos ajudar a corrigir possíveis bugs o mais rápido possível:

- Verifique se o problema realmente é um bug, e não um erro causado por você, como o uso de componentes ou versões incompatíveis no ambiente. (Certifique-se de que leu a [documentação](). Se estiver procurando suporte, consulte a [seção correspondente](#tenho-uma-dúvida)).
- Para verificar se outros usuários já enfrentaram (e possivelmente resolveram) o mesmo problema, confira se já existe algum relato de bug ou erro semelhante no [rastreador de bugs](https://github.com/DanilolBorba/Operos/issues?q=label%3Abug).
- Além disso, pesquise na internet, incluindo o Stack Overflow, para verificar se usuários fora da comunidade do GitHub já discutiram o problema.
- Reúna informações sobre o bug:
  - Rastreamento da pilha de execução (Stack Trace/Traceback).
  - Sistema operacional, plataforma e versão (Windows, Linux, macOS, x86, ARM).
  - Versão do interpretador, compilador, SDK, ambiente de execução ou gerenciador de pacotes, dependendo do que for relevante.
  - Possivelmente, os dados de entrada e os resultados obtidos.
  - Você consegue reproduzir o problema de maneira consistente? 

#### Como enviar um bom relato de bug?

> **Você nunca deve relatar problemas de segurança, vulnerabilidades ou bugs que contenham informações confidenciais no rastreador de issues ou em qualquer outro local público!!** Em vez disso, problemas de segurança que contenham informações confidenciais devem ser enviados por e-mail para jafv@cesar.school, fafs@cesar.school, ou dcmbr@cesar.school.

Utilizamos as issues do GitHub para acompanhar bugs e erros. Caso encontre algum problema no projeto:

- Abra uma [Issue](https://github.com/DanilolBorba/Operos/issues/new). (Como ainda não podemos ter certeza de que se trata de um bug, pedimos que não o classifique como tal nem adicione uma tag de bug neste momento.)
- Explique qual comportamento você esperava e qual comportamento realmente ocorreu.
- Forneça o máximo de contexto possível e descreva as *etapas para reproduzir o problema*, de modo que outra pessoa consiga seguir as instruções e recriá-lo por conta própria. Geralmente, isso inclui o seu código. Para elaborar bons relatos de bugs, você deve isolar o problema e criar um caso de teste reduzido.
- Forneça as informações reunidas na seção anterior.

**Após o envio:**

- Nós classificaremos a issue com as tags correspondentes.
- Um integrante da equipe tentará reproduzir o problema seguindo as etapas fornecidas. Caso não existam etapas para reprodução ou não haja uma maneira evidente de reproduzir o problema, a equipe solicitará essas informações e marcará a issue com a tag `needs-repro`. Bugs com a tag `needs-repro` não serão tratados até que possam ser reproduzidos.
- Se a equipe conseguir reproduzir o problema, ele será marcado com a tag `needs-fix`, além de possivelmente receber outras tags (como `critical`). Em seguida, a issue ficará disponível para ser [implementada por alguém](#sua-primeira-contribuição-de-código).



### Sugerindo melhorias

Esta seção orienta você sobre como enviar uma sugestão de melhoria para o Operos, **incluindo funcionalidades completamente novas e pequenas melhorias em funcionalidades existentes**, da alteração mais minuciosa até a mais gritante são muito bem-vindas. Seguir estas orientações abaixo ajudará os mantenedores e a comunidade a compreender sua sugestão e encontrar propostas relacionadas:

#### Antes de enviar uma sugestão de melhoria


- Leia atentamente a [documentação]() e verifique se a funcionalidade já está contemplada, talvez por meio de alguma configuração específica.
- Veja a parte de [Issues](https://github.com/DanilolBorba/Operos/issues) para verificar se a melhoria já foi sugerida. Caso tenha sido, adicione um comentário à issue existente em vez de abrir uma nova.
- Verifique se sua ideia está de acordo com o escopo e os objetivos do projeto. Cabe a você apresentar argumentos convincentes para demonstrar aos desenvolvedores do projeto os benefícios dessa funcionalidade. Tenha em mente que buscamos funcionalidades úteis para a maioria dos nossos usuários, e não apenas para um pequeno grupo. Caso sua ideia seja direcionada a uma parcela muito específica de usuários, considere desenvolver uma biblioteca complementar ou um plugin.


#### Como enviar uma boa sugestão de melhoria?

As sugestões de melhoria são acompanhadas por meio das [issues do GitHub](https://github.com/DanilolBorba/Operos/issues).

- Utilize um **título claro e descritivo** para identificar a sugestão.
- Forneça uma **descrição passo a passo da melhoria sugerida**, incluindo o máximo de detalhes possível.
- **Descreva o comportamento atual** e **explique qual comportamento você esperava encontrar em seu lugar**, além de justificar o motivo. Neste momento, você também pode informar quais alternativas não atendem às suas necessidades.
- Você pode **incluir capturas de tela ou gravações da tela** que ajudem a demonstrar as etapas ou destacar a parte do projeto à qual sua sugestão está relacionada. Você pode utilizar o [LICEcap](https://www.cockos.com/licecap/) para gravar GIFs no macOS e no Windows, e o [gravador de tela integrado ao GNOME](https://help.gnome.org/users/gnome-help/stable/screen-shot-record.html.en) ou o [SimpleScreenRecorder](https://github.com/MaartenBaert/ssr) no Linux. 
- **Explique por que essa melhoria seria útil** para a maioria dos usuários do Operos. Você também pode mencionar outros projetos que resolveram o problema de maneira mais eficiente e que possam servir de inspiração.

## Mensagens de commit
Para mensagens de commits, fale de maneira sucinta o que o commit faz no tempo verbal presente. Por exemplo:

> adiciona favicons

> apaga arquivo CSSpaginaHome.css

> cria html de sugestões

> edita estilo.css para criar classe de container

são mensagens de commits válidas.

## Agradecemos novamente pelo seu tempo e vontade de nos ajudar!!! 🤝