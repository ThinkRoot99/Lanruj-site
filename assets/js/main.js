// Lanruj - site: limba aleasă, bara de sus la derulare, apariția secțiunilor.
(function () {
  var root = document.documentElement;
  root.classList.remove("no-js");

  // Limba: engleza e implicită; alegerea rămâne în browserul vizitatorului.
  // Fiecare pagină își anunță perechea în cealaltă limbă prin <link rel="alternate" hreflang>.
  var KEY = "lanruj-limba";
  var here = root.getAttribute("lang") || "en";
  function pageFor(l) {
    var link = document.querySelector('link[rel="alternate"][hreflang="' + l + '"]');
    // data-rel: legătura relativă (merge și pe calculator, și pe orice domeniu); href e adresa publică.
    return link ? (link.getAttribute("data-rel") || link.getAttribute("href")) : null;
  }
  var saved = null;
  try { saved = localStorage.getItem(KEY); } catch (e) {}
  if (here === "en" && saved && saved !== "en" && !/[?&]lang=en/.test(location.search) && pageFor(saved)) {
    location.replace(pageFor(saved));
    return;
  }
  var pick = document.getElementById("lang");
  if (pick) {
    pick.value = here;
    pick.addEventListener("change", function () {
      try { localStorage.setItem(KEY, pick.value); } catch (e) {}
      var to = pageFor(pick.value);
      if (to) location.href = to + (pick.value === "en" ? "?lang=en" : "");
    });
  }

  // Bara de sus primește o umbră după ce pagina e derulată.
  var top = document.querySelector(".top");
  function onScroll() { if (top) top.classList.toggle("scrolled", window.scrollY > 8); }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // Secțiunile apar ușor când ajung pe ecran.
  var items = document.querySelectorAll(".reveal");
  if (!("IntersectionObserver" in window)) {
    items.forEach(function (el) { el.classList.add("seen"); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) {
        en.target.classList.add("seen");
        io.unobserve(en.target);
      }
    });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.12 });
  items.forEach(function (el) { io.observe(el); });
})();
