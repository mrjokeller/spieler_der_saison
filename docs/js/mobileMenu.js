export function initMobileMenu() {
    const hamburger = document.querySelector(".hamburger");
    const mobileMenu = document.querySelector(".mobile-menu");

    hamburger.addEventListener("click", () => {
        mobileMenu.classList.toggle("active");
        hamburger.classList.toggle("active");
    });

    mobileMenu.querySelectorAll("a").forEach((link) => {
        link.addEventListener("click", () => {
            mobileMenu.classList.remove("active");
            hamburger.classList.remove("active");
        });
    });
}