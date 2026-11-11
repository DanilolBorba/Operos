(function () {
    function iniciarOperos() {
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
})();