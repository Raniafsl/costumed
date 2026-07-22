// Costumed — small interactivity layer. No framework, no build step.
document.addEventListener("DOMContentLoaded", () => {
  initSpotlight();
  initReveal();
  initSearchShortcut();
  initAutoSubmitSearch();
});

// A soft flashlight that follows the cursor over the main content —
// only turns on once the visitor actually moves the mouse (keeps it
// from flashing on load, and stays off entirely on touch devices).
function initSpotlight() {
  if (window.matchMedia("(pointer: coarse)").matches) return;

  const glow = document.createElement("div");
  glow.className = "spotlight";
  document.body.appendChild(glow);

  let raf = null;
  window.addEventListener("mousemove", (e) => {
    glow.classList.add("is-active");
    if (raf) return;
    raf = requestAnimationFrame(() => {
      glow.style.setProperty("--mx", `${e.clientX}px`);
      glow.style.setProperty("--my", `${e.clientY}px`);
      raf = null;
    });
  });
  window.addEventListener("mouseleave", () => glow.classList.remove("is-active"));
}

// Fade + rise cards and hero content into view as they enter the viewport.
function initReveal() {
  const targets = document.querySelectorAll(".look-card, .hero, .detail-layout");
  targets.forEach((el) => el.classList.add("reveal"));

  if (!("IntersectionObserver" in window)) {
    targets.forEach((el) => el.classList.add("is-visible"));
    return;
  }

  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry, i) => {
        if (entry.isIntersecting) {
          setTimeout(() => entry.target.classList.add("is-visible"), i * 40);
          io.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12 }
  );
  targets.forEach((el) => io.observe(el));
}

// Press "/" anywhere to jump into the search field, like a quiet card catalog.
function initSearchShortcut() {
  const search = document.getElementById("q");
  if (!search) return;

  document.addEventListener("keydown", (e) => {
    if (e.key === "/" && document.activeElement !== search) {
      e.preventDefault();
      search.focus();
    }
    if (e.key === "Escape" && document.activeElement === search) {
      search.blur();
    }
  });

  const wrap = search.closest(".search-wrap");
  if (wrap) {
    search.addEventListener("focus", () => wrap.classList.add("is-focused"));
    search.addEventListener("blur", () => wrap.classList.remove("is-focused"));
  }
}

// Debounced auto-submit so typing a title/character feels like live search.
function initAutoSubmitSearch() {
  const search = document.getElementById("q");
  if (!search) return;
  const form = search.closest("form");
  if (!form) return;

  let timer = null;
  search.addEventListener("input", () => {
    clearTimeout(timer);
    timer = setTimeout(() => form.requestSubmit(), 450);
  });
}
