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

// ================= Finisaje =================
(function () {
  var root = document.documentElement;
  var ro = root.lang === "ro";
  var calm = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // ---- Zi / noapte: după sistem sau ales cu butonul; alegerea rămâne doar în browserul vizitatorului ----
  var THEME = "lanruj-tema";
  var darkSys = window.matchMedia("(prefers-color-scheme: dark)");
  function current() { return root.getAttribute("data-theme") || (darkSys.matches ? "dark" : "light"); }
  function syncPictures() {
    // Capturile de noapte au <source media="(prefers-color-scheme: dark)">; le potrivim cu alegerea.
    var t = root.getAttribute("data-theme");
    document.querySelectorAll('source[data-dark]').forEach(function (s) {
      s.media = t === "dark" ? "all" : t === "light" ? "not all" : "(prefers-color-scheme: dark)";
    });
  }
  document.querySelectorAll('source[media="(prefers-color-scheme: dark)"]').forEach(function (s) { s.setAttribute("data-dark", ""); });
  syncPictures();
  var btn = document.querySelector(".theme");
  if (btn) {
    function label() {
      var dark = current() === "dark";
      btn.setAttribute("aria-label", ro ? (dark ? "Treci la modul de zi" : "Treci la modul de noapte") : (dark ? "Switch to light mode" : "Switch to dark mode"));
      btn.title = btn.getAttribute("aria-label");
    }
    label();
    btn.addEventListener("click", function () {
      var next = current() === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem(THEME, next); } catch (e) {}
      syncPictures(); label();
    });
  }

  // ---- Data de azi, scrisă de mână, cu un salut după oră ----
  var today = document.querySelector(".today");
  if (today) {
    var d = new Date(), h = d.getHours();
    var hello = h >= 5 && h < 11 ? (ro ? "Bună dimineața!" : "Good morning!")
              : h >= 11 && h < 18 ? (ro ? "Bună ziua!" : "Good afternoon!")
              : (ro ? "Bună seara!" : "Good evening!");
    var date = d.toLocaleDateString(ro ? "ro-RO" : "en-GB", { weekday: "long", day: "numeric", month: "long" });
    today.innerHTML = "";
    today.appendChild(document.createTextNode((ro ? "Azi e " : "Today is ") + date + "."));
    var small = document.createElement("small");
    small.textContent = hello + (ro ? " Pagina ta te așteaptă." : " Your page is waiting.");
    today.appendChild(small);
  }

  // ---- Caietul care se scrie: scrii, bifezi, muți pe mâine ----
  var book = document.querySelector(".notebook");
  if (book) {
    var list = book.querySelector("ol"), field = book.querySelector(".field");
    var hint = field.textContent;
    var steps = ro
      ? [[".", "•", "Cumpără pâine"], ["o", "○", "10:00 Dentist"], ["-", "–", "Autobuzul a întârziat"], [".", "•", "Sună-l pe Andrei"]]
      : [[".", "•", "Buy bread"], ["o", "○", "10:00 Dentist"], ["-", "–", "The bus was late"], [".", "•", "Call Andrei"]];
    var tomorrow = ro ? "pe mâine" : "to tomorrow";
    function line(sign, text) {
      var li = document.createElement("li");
      li.innerHTML = '<span class="sg"></span><span class="tx"></span><span class="tag"></span>';
      li.querySelector(".sg").textContent = sign;
      li.querySelector(".tx").textContent = text;
      li.querySelector(".tag").textContent = "> " + tomorrow;
      return li;
    }
    function finalState() {
      list.innerHTML = "";
      steps.forEach(function (s) { list.appendChild(line(s[1], s[2])); });
      list.children[0].classList.add("done"); list.children[0].querySelector(".sg").textContent = "×";
      list.children[3].classList.add("moved"); list.children[3].querySelector(".sg").textContent = ">";
    }
    if (calm) { finalState(); }
    else {
      var wait = function (ms) { return new Promise(function (r) { setTimeout(r, ms); }); };
      var typeIn = async function (txt) {
        field.classList.add("typing"); field.textContent = "";
        var caret = document.createElement("span"); caret.className = "caret";
        for (var i = 0; i < txt.length; i++) { field.textContent = txt.slice(0, i + 1); field.appendChild(caret); await wait(55 + Math.random() * 45); }
        await wait(350);
      };
      var run = async function () {
        for (;;) {
          list.innerHTML = ""; field.textContent = hint; field.classList.remove("typing");
          await wait(900);
          for (var k = 0; k < steps.length; k++) {
            await typeIn(steps[k][0] + " " + steps[k][2]);
            list.appendChild(line(steps[k][1], steps[k][2]));
            field.textContent = hint; field.classList.remove("typing");
            await wait(500);
          }
          await wait(700);
          var first = list.children[0]; first.querySelector(".sg").textContent = "×"; first.classList.add("done");
          await wait(1300);
          var last = list.children[3]; last.querySelector(".sg").textContent = ">"; last.classList.add("moved");
          await wait(4200);
        }
      };
      // Pornește abia când caietul ajunge pe ecran.
      if ("IntersectionObserver" in window) {
        var started = false;
        new IntersectionObserver(function (en, obs) { if (en[0].isIntersecting && !started) { started = true; obs.disconnect(); run(); } }, { threshold: 0.3 }).observe(book);
      } else { run(); }
    }
  }

  // ---- Capturile, mari: clic pe una o deschide; săgeți între ele, Esc închide ----
  var shots = Array.prototype.slice.call(document.querySelectorAll(".shot img"));
  if (shots.length && typeof HTMLDialogElement === "function") {
    var dlg = document.createElement("dialog");
    dlg.className = "zoom";
    dlg.innerHTML = '<figure><img alt=""><figcaption></figcaption></figure>' +
      '<button class="close" type="button">×</button><button class="prev" type="button">‹</button><button class="next" type="button">›</button>';
    document.body.appendChild(dlg);
    var big = dlg.querySelector("img"), cap = dlg.querySelector("figcaption"), at = 0;
    dlg.querySelector(".close").setAttribute("aria-label", ro ? "Închide" : "Close");
    dlg.querySelector(".prev").setAttribute("aria-label", ro ? "Captura de dinainte" : "Previous screenshot");
    dlg.querySelector(".next").setAttribute("aria-label", ro ? "Captura următoare" : "Next screenshot");
    function show(i) {
      at = (i + shots.length) % shots.length;
      var img = shots[at];
      big.src = img.currentSrc || img.src;
      big.src = big.src.replace(/-(640|960)\.webp$/, "-1280.webp");
      big.alt = img.alt; cap.textContent = img.alt;
    }
    shots.forEach(function (img, i) {
      img.setAttribute("tabindex", "0");
      img.setAttribute("role", "button");
      img.addEventListener("click", function () { show(i); dlg.showModal(); });
      img.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); show(i); dlg.showModal(); } });
    });
    dlg.querySelector(".close").addEventListener("click", function () { dlg.close(); });
    dlg.querySelector(".prev").addEventListener("click", function () { show(at - 1); });
    dlg.querySelector(".next").addEventListener("click", function () { show(at + 1); });
    dlg.addEventListener("click", function (e) { if (e.target === dlg) dlg.close(); });
    dlg.addEventListener("keydown", function (e) {
      if (e.key === "ArrowLeft") show(at - 1);
      if (e.key === "ArrowRight") show(at + 1);
    });
  }
})();
