// Lanruj - site: limba aleasă, bara de sus la derulare, apariția secțiunilor.
(function () {
  var root = document.documentElement;
  root.classList.remove("no-js");

  // Limba: pagina în engleză e cea implicită; alegerea rămâne în browserul vizitatorului.
  var KEY = "lanruj-limba";
  var here = root.getAttribute("lang") || "en";
  var base = root.getAttribute("data-base") || "";
  function pageFor(l) { return l === "en" ? base + "index.html" : base + "lang/" + l + ".html"; }
  var saved = null;
  try { saved = localStorage.getItem(KEY); } catch (e) {}
  if (here === "en" && saved && saved !== "en" && !/[?&]lang=en/.test(location.search)) {
    location.replace(pageFor(saved));
    return;
  }
  var pick = document.getElementById("lang");
  if (pick) {
    pick.value = here;
    pick.addEventListener("change", function () {
      try { localStorage.setItem(KEY, pick.value); } catch (e) {}
      location.href = pageFor(pick.value) + (pick.value === "en" ? "?lang=en" : "");
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
