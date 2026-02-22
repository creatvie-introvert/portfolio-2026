(function () {
    const STORAGE_KEY = "portfolio-theme";
    const root = document.documentElement;

    function setTheme(theme) {
        if (theme === "dark") {
            root.setAttribute("data-theme", "dark");
        } else {
            root.removeAttribute("data-theme");
        }
    }

    function getSavedTheme() {
        return localStorage.getItem(STORAGE_KEY);
    }

    function getSystemTheme() {
        return window.matchMedia("(prefers-color-scheme: dark)").matches
        ? "dark"
        : "light";
    }

    // 1) Apply saved theme OR system theme on page load
    const savedTheme = getSavedTheme();
    const initialTheme = savedTheme || getSystemTheme();
    setTheme(initialTheme);

    // 2) Toggle when user clicks the button
    window.addEventListener("DOMContentLoaded", () => {
        const toggleButtons = document.querySelectorAll(".theme-toggle");

        toggleButtons.forEach((btn) => {
            btn.addEventListener("click", () => {
                const isDark = root.getAttribute("data-theme") === "dark";
                const newTheme = isDark ? "light" : "dark";

                setTheme(newTheme);
                localStorage.setItem(STORAGE_KEY, newTheme);
            });
        });

        const navbar = document.querySelector(".navbar");

        function setNavbarState() {
            if (!navbar) return;
            navbar.classList.toggle("is-scrolled", window.scrollY > 8);
        }

        window.addEventListener("scroll", setNavbarState, { passive: true });
        setNavbarState();
    });
})();