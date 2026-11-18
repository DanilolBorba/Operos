(function () {
    function iniciarOperos() {
        iniciarAssistenteOperos();
        if (window.__operosInicializado) return;
        window.__operosInicializado = true;

        const menuToggle = document.querySelector("[data-menu-toggle]");
        const menu = document.querySelector("[data-menu]");

        if (menuToggle && menu) {
            menuToggle.addEventListener("click", function () {
                const aberto = menu.classList.toggle("is-open");
                menuToggle.setAttribute("aria-expanded", String(aberto));
            });

            menu.querySelectorAll("a").forEach(function (link) {
                link.addEventListener("click", function () {
                    menu.classList.remove("is-open");
                    menuToggle.setAttribute("aria-expanded", "false");
                });
            });
        }

        document.querySelectorAll("[data-toggle-password]").forEach(function (button) {
            const input = document.getElementById(
                button.getAttribute("data-toggle-password")
            );

            if (!input) return;

            button.addEventListener("click", function () {
                const mostrar = input.type === "password";

                input.type = mostrar ? "text" : "password";

                button.innerHTML = mostrar
                    ? '<i data-lucide="eye-off"></i>'
                    : '<i data-lucide="eye"></i>';

                button.setAttribute(
                    "aria-label",
                    mostrar ? "Ocultar senha" : "Mostrar senha"
                );

                if (window.lucide) {
                    window.lucide.createIcons({ root: button });
                }
            });
        });

        const prefereMovimentoReduzido = window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches;

        if (prefereMovimentoReduzido) return;

        const seletores = [
            ".page-section .section-heading",
            ".intro-visual",
            ".intro-text",
            ".segment-card",
            ".innovation-card",
            ".step-card",
            ".recommendation-card",
            ".account-cta-card",
            ".about-copy",
            ".about-visual",
            ".team-member",
            ".team-card",
            ".team-section-heading"
        ];

        const elementos = document.querySelectorAll(seletores.join(","));

        if (!elementos.length) return;
        if (!("IntersectionObserver" in window)) return;

        elementos.forEach(function (elemento) {
            const grupo = Array.from(elemento.parentElement.children).filter(
                function (irmao) {
                    return irmao.matches(seletores.join(","));
                }
            );

            const indice = Math.max(0, grupo.indexOf(elemento));

            const atraso = elemento.matches(".step-card, .segment-card")
                ? Math.min(indice, 3) * 130
                : Math.min(indice, 5) * 85;

            elemento.style.setProperty("--reveal-delay", atraso + "ms");
            elemento.classList.add("reveal-on-scroll");
        });

        const observador = new IntersectionObserver(
            function (entradas, observer) {
                entradas.forEach(function (entrada) {
                    if (entrada.isIntersecting) {
                        entrada.target.classList.add("is-visible");
                        observer.unobserve(entrada.target);
                    }
                });
            },
            {
                threshold: 0.12,
                rootMargin: "0px 0px -40px 0px"
            }
        );

        elementos.forEach(function (elemento) {
            observador.observe(elemento);
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", iniciarOperos, { once: true });
    } else {
        iniciarOperos();
    }

    function iniciarAssistenteOperos() {
    const container = document.querySelector(".operos-chat");

    if (!container) return;

    const toggle = container.querySelector("[data-chat-toggle]");
    const painel = container.querySelector("[data-chat-panel]");
    const fechar = container.querySelector("[data-chat-close]");
    const limpar = container.querySelector("[data-chat-clear]");
    const formulario = container.querySelector("[data-chat-form]");
    const campo = container.querySelector("[data-chat-input]");
    const mensagens = container.querySelector("[data-chat-messages]");
    const sugestoes = container.querySelector("[data-chat-suggestions]");
    const botaoEnviar = container.querySelector("[data-chat-send]");

    const url = container.dataset.chatUrl;
    const chaveHistorico = "operos_chat_history_v1";

    const mensagemInicial =
        "Olá! Sou o assistente virtual do Operos. Como posso te ajudar?";

    let historico = carregarHistorico();
    let enviando = false;

    function carregarHistorico() {
        try {
            const salvo = sessionStorage.getItem(chaveHistorico);
            const dados = salvo ? JSON.parse(salvo) : [];

            if (!Array.isArray(dados)) return [];

            return dados.filter(function (item) {
                return item &&
                    (item.role === "user" || item.role === "assistant") &&
                    typeof item.content === "string";
            }).slice(-10);

        } catch (erro) {
            return [];
        }
    }

    function salvarHistorico() {
        try {
            sessionStorage.setItem(
                chaveHistorico,
                JSON.stringify(historico.slice(-10))
            );
        } catch (erro) {
        }
    }

function escaparHTML(texto) {
    return texto.replace(/[&<>"']/g, function (caractere) {
        const entidades = {
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#39;"
        };

        return entidades[caractere];
    });
}

function formatarMarkdown(texto) {
    const linhas = escaparHTML(texto).split(/\r?\n/);

    let html = "";
    let listaAberta = false;

    linhas.forEach(function (linha) {
        const item = linha.match(/^\s*[-*]\s+(.+)$/);

        if (item) {
            if (!listaAberta) {
                html += "<ul>";
                listaAberta = true;
            }

            html += "<li>" + formatarTexto(item[1]) + "</li>";
            return;
        }

        if (listaAberta) {
            html += "</ul>";
            listaAberta = false;
        }

        if (!linha.trim()) {
            return;
        }

        let conteudo = linha.trim();

        conteudo = conteudo.replace(
            /^\#{1,3}\s+/,
            ""
        );

        html += "<p>" + formatarTexto(conteudo) + "</p>";
    });

    if (listaAberta) {
        html += "</ul>";
    }

    return html;
}

function formatarTexto(texto) {
    return texto
        .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
        .replace(/\*([^*]+)\*/g, "<em>$1</em>");
}

function criarMensagem(texto, papel) {
    const mensagem = document.createElement("div");

    mensagem.className =
        "operos-chat-message operos-chat-message-" + papel;

    if (
        papel === "assistant" &&
        window.marked &&
        window.DOMPurify
    ) {
        const html = window.marked.parse(texto, {
            gfm: true,
            breaks: true
        });

        mensagem.innerHTML = window.DOMPurify.sanitize(html, {
            USE_PROFILES: {
                html: true
            }
        });

    } else {
        mensagem.textContent = texto;
    }

    mensagens.appendChild(mensagem);

    mensagens.scrollTop = mensagens.scrollHeight;

    return mensagem;
}

    function mostrarMensagemInicial() {
        mensagens.innerHTML = "";

        criarMensagem(mensagemInicial, "assistant");

        sugestoes.hidden = false;
    }

    function renderizarHistorico() {
        mensagens.innerHTML = "";

        if (!historico.length) {
            mostrarMensagemInicial();
            return;
        }

        historico.forEach(function (item) {
            criarMensagem(item.content, item.role);
        });

        sugestoes.hidden = true;
    }

    function abrirPainel() {
        painel.hidden = false;
        painel.setAttribute("aria-hidden", "false");

        toggle.setAttribute("aria-expanded", "true");

        container.classList.add("is-open");

        campo.focus();

        mensagens.scrollTop = mensagens.scrollHeight;
    }

    function fecharPainel() {
        painel.hidden = true;
        painel.setAttribute("aria-hidden", "true");

        toggle.setAttribute("aria-expanded", "false");

        container.classList.remove("is-open");

        toggle.focus();
    }

    function obterTokenCSRF() {
        const token = formulario.querySelector(
            "[name=csrfmiddlewaretoken]"
        );

        return token ? token.value : "";
    }

    function ajustarCampo() {
        campo.style.height = "auto";

        campo.style.height =
            Math.min(campo.scrollHeight, 110) + "px";
    }

    function definirEnvioAtivo(ativo) {
        enviando = ativo;

        campo.disabled = ativo;
        botaoEnviar.disabled = ativo;
        limpar.disabled = ativo;

        formulario.classList.toggle("is-sending", ativo);
    }

    async function enviarMensagem(texto) {
        if (enviando || !texto.trim()) return;

        const pergunta = texto.trim();

        historico.push({
            role: "user",
            content: pergunta
        });

        historico = historico.slice(-10);

        salvarHistorico();

        criarMensagem(pergunta, "user");

        sugestoes.hidden = true;

        campo.value = "";

        ajustarCampo();

        definirEnvioAtivo(true);

        const digitando = document.createElement("div");

        digitando.className = "operos-chat-typing";

        digitando.setAttribute(
            "aria-label",
            "Assistente está digitando"
        );

        digitando.innerHTML =
            "<span></span><span></span><span></span>";

        mensagens.appendChild(digitando);

        mensagens.scrollTop = mensagens.scrollHeight;

        try {
            const resposta = await fetch(url, {
                method: "POST",

                credentials: "same-origin",

                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": obterTokenCSRF()
                },

                body: JSON.stringify({
                    messages: historico
                })
            });

            const dados = await resposta.json();

            digitando.remove();

            if (!resposta.ok) {
                throw new Error(
                    dados.erro || "Não foi possível enviar a mensagem."
                );
            }

            historico.push({
                role: "assistant",
                content: dados.reply
            });

            historico = historico.slice(-10);

            salvarHistorico();

            criarMensagem(dados.reply, "assistant");

        } catch (erro) {
            digitando.remove();

            if (
                historico.length &&
                historico[historico.length - 1].role === "user" &&
                historico[historico.length - 1].content === pergunta
            ) {
                historico.pop();
                salvarHistorico();
            }

            criarMensagem(
                erro.message || "Não consegui responder agora. Tente novamente.",
                "error"
            );

        } finally {
            definirEnvioAtivo(false);
            campo.focus();
        }
    }

    toggle.addEventListener("click", function () {
        if (painel.hidden) {
            abrirPainel();
        } else {
            fecharPainel();
        }
    });

    fechar.addEventListener("click", fecharPainel);

    limpar.addEventListener("click", function () {
        historico = [];

        salvarHistorico();

        mostrarMensagemInicial();

        campo.focus();
    });

    formulario.addEventListener("submit", function (evento) {
        evento.preventDefault();

        enviarMensagem(campo.value);
    });

    campo.addEventListener("input", ajustarCampo);

    campo.addEventListener("keydown", function (evento) {
        if (evento.key === "Enter" && !evento.shiftKey) {
            evento.preventDefault();

            formulario.requestSubmit();
        }
    });

    container.querySelectorAll("[data-chat-suggestion]").forEach(
        function (botao) {
            botao.addEventListener("click", function () {
                enviarMensagem(botao.dataset.chatSuggestion);
            });
        }
    );

    document.addEventListener("keydown", function (evento) {
        if (evento.key === "Escape" && !painel.hidden) {
            fecharPainel();
        }
    });

    renderizarHistorico();

    if (window.lucide) {
        window.lucide.createIcons({ root: container });
    }
}


})();