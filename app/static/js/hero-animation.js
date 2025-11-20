const root = document.documentElement;

function updateSkyFade() {
    const max = document.body.scrollHeight - window.innerHeight;
    const progress = max > 0 ? window.scrollY / max : 0;
    const fade = Math.min(Math.max(progress * 1.3, 0), 1);
    root.style.setProperty("--sky-fade", fade.toString());
}

window.addEventListener("scroll", updateSkyFade);
window.addEventListener("load", updateSkyFade);

function attachTilt(selector) {
    const cards = document.querySelectorAll(selector);
    cards.forEach((card) => {
        card.addEventListener("mousemove", (event) => {
            const rect = card.getBoundingClientRect();
            const x = (event.clientX - rect.left) / rect.width - 0.5;
            const y = (event.clientY - rect.top) / rect.height - 0.5;
            const rotateX = y * -18;
            const rotateY = x * 18;
            card.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-10px)`;
        });
        card.addEventListener("mouseleave", () => {
            card.style.transform = "";
        });
    });
}

window.addEventListener("load", () => {
    attachTilt(".neo-card");
});
