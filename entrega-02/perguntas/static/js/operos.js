
document.addEventListener("DOMContentLoaded", function () {

    // Menu responsivo
    const menuToggle = document.querySelector("[data-menu-toggle");
    const menu = document.querySelector("[data-menu]");

    if (menuToggle && menu) {

        menuToggle.addEventListener("click", function () {

            const aberto = menu.classList.toggle("is-open");

            menuToggle.setAttribute("aria-expanded", aberto);

        });

        const links = menu.querySelectorAll("a");

        links.forEach(function (link) {

            link.addEventListener("click", function () {

                menu.classList.remove("is-open");

                menuToggle.setAttribute("aria-expanded", "false");

            });

        });

    }


    // Mostrar e ocultar senha
    const botoesSenha = document.querySelectorAll("[data-toggle-password]");

    botoesSenha.forEach(function (botao) {

        botao.addEventListener("click", function () {

            const id = botao.getAttribute("data-toggle-password");

            const campo = document.getElementById(id);

            if (!campo) {
                return;
            }

            if (campo.type === "password") {

                campo.type = "text";

                botao.textContent = "◎";

                botao.setAttribute("aria-label", "Ocultar senha");

            } else {

                campo.type = "password";

                botao.textContent = "◉";

                botao.setAttribute("aria-label", "Mostrar senha");

            }

        });

    });

});