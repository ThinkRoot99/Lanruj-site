#!/usr/bin/env python3
"""Paginile site-ului Lanruj: meniul de sus și subsolul comune, plus paginile Despre, Contact
și Politica de confidențialitate, în engleză (rădăcina) și română (lang/ro/).
Paginile de început (index.html, lang/ro/index.html) își păstrează conținutul; li se refac
doar meniul și subsolul. Folosire: python3 site/tools/pagini.py"""
import os
import re

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Adresa de contact: de completat de autor (până atunci apare un loc marcat).
EMAIL = "lanruj@thinkopen.site"

# Adresa site-ului (fără / la final): pentru adresele canonice, hreflang, imaginile pentru rețele și sitemap.
SITE_URL = "https://lanruj.thinkopen.site"


# Versiunea publicată și adresele pachetelor de la Releases (de schimbat la fiecare versiune nouă).
VERSION = "0.4.2"
REPO = "https://github.com/ThinkRoot99/Lanruj"
APPIMAGE_URL = f"{REPO}/releases/download/v{VERSION}/Lanruj-{VERSION}-x86_64.AppImage"
FLATPAK_URL = f"{REPO}/releases/download/v{VERSION}/lanruj.flatpak"

PAGES = {
    # cheie: (fișier EN, fișier RO)
    "home": ("index.html", "lang/ro/index.html"),
    "docs": ("docs.html", "lang/ro/documentatie.html"),
    "about": ("about.html", "lang/ro/despre.html"),
    "contact": ("contact.html", "lang/ro/contact.html"),
    "privacy": ("privacy.html", "lang/ro/confidentialitate.html"),
}
NAV = {
    "en": [("home", "Home"), ("docs", "Docs"), ("about", "About"), ("contact", "Contact"), ("privacy", "Privacy")],
    "ro": [("home", "Acasă"), ("docs", "Documentație"), ("about", "Despre"), ("contact", "Contact"), ("privacy", "Confidențialitate")],
}


def rel(frm, to):
    """Legătura relativă de la fișierul `frm` la fișierul `to` (amândouă față de rădăcina site-ului)."""
    return os.path.relpath(os.path.join(SITE, to), os.path.dirname(os.path.join(SITE, frm)))


def header(lang, key):
    me = PAGES[key][0 if lang == "en" else 1]
    a = lambda k: rel(me, PAGES[k][0 if lang == "en" else 1])
    links = "\n".join(
        f'      <a href="{a(k)}"{" aria-current=\"page\"" if k == key else ""}>{name}</a>' for k, name in NAV[lang]
    )
    label = "Language" if lang == "en" else "Limba"
    return f'''<header class="top">
  <div class="wrap">
    <a class="brand" href="{a("home")}"><img src="{rel(me, "assets/img/lanruj.svg")}" alt="" width="34" height="34"> Lanruj</a>
    <nav>
{links}
    </nav>
    <label class="lang-pick">
      <select id="lang" aria-label="{label}">
        <option value="en">English</option>
        <option value="ro">Română</option>
      </select>
    </label>
  </div>
</header>'''


def footer(lang, key):
    me = PAGES[key][0 if lang == "en" else 1]
    a = lambda k: rel(me, PAGES[k][0 if lang == "en" else 1])
    home = a("home")
    if lang == "en":
        return f'''<footer>
  <div class="wrap">
    <div class="cols">
      <div>
        <a class="brand" href="{home}"><img src="{rel(me, "assets/img/lanruj.svg")}" alt="" width="28" height="28"> Lanruj</a>
        <p>A bullet journal app for Linux.</p>
        <p class="sign">built by Claude AI, tested by ThinkRoot</p>
      </div>
      <div>
        <h4>App</h4>
        <ul>
          <li><a href="{home}#features">Features</a></li>
          <li><a href="{home}#faq">Questions</a></li>
          <li><a href="{home}#download">Download</a></li>
        </ul>
      </div>
      <div>
        <h4>Project</h4>
        <ul>
          <li><a href="{a("docs")}">Docs</a></li>
          <li><a href="{a("about")}">About</a></li>
          <li><a href="{a("contact")}">Contact</a></li>
          <li><a href="{a("privacy")}">Privacy policy</a></li>
        </ul>
      </div>
    </div>
    <p class="legal copy"><span class="copyleft" role="img" aria-label="Copyleft">©</span> 2026 Lanruj</p>
    <p class="legal">Lanruj is free software, released under the GPL-3.0-or-later licence. Bullet Journal is a method created by Ryder Carroll; Lanruj is an independent app and is not affiliated with it or its creator.</p>
  </div>
</footer>'''
    return f'''<footer>
  <div class="wrap">
    <div class="cols">
      <div>
        <a class="brand" href="{home}"><img src="{rel(me, "assets/img/lanruj.svg")}" alt="" width="28" height="28"> Lanruj</a>
        <p>Jurnal de tip „bullet journal” pentru Linux.</p>
        <p class="sign">construit de Claude AI, testat de ThinkRoot</p>
      </div>
      <div>
        <h4>Aplicația</h4>
        <ul>
          <li><a href="{home}#caracteristici">Caracteristici</a></li>
          <li><a href="{home}#intrebari">Întrebări</a></li>
          <li><a href="{home}#descarca">Descarcă</a></li>
        </ul>
      </div>
      <div>
        <h4>Proiectul</h4>
        <ul>
          <li><a href="{a("docs")}">Documentație</a></li>
          <li><a href="{a("about")}">Despre</a></li>
          <li><a href="{a("contact")}">Contact</a></li>
          <li><a href="{a("privacy")}">Politica de confidențialitate</a></li>
        </ul>
      </div>
    </div>
    <p class="legal copy"><span class="copyleft" role="img" aria-label="Copyleft">©</span> 2026 Lanruj</p>
    <p class="legal">Lanruj este un program liber, sub licența GPL-3.0-or-later. Bullet Journal este o metodă creată de Ryder Carroll; Lanruj este o aplicație independentă și nu are legătură cu metoda sau cu autorul ei.</p>
  </div>
</footer>'''


def url_of(path):
    """Adresa completă a unei pagini; index.html devine dosarul lui."""
    path = path[: -len("index.html")] if path.endswith("index.html") else path
    return f"{SITE_URL}/{path}"


def version(path):
    """O amprentă scurtă a fișierului, pusă în adresă (?v=…): browserul îl poate ține minte mult, iar o
    schimbare ajunge imediat la vizitatori."""
    import hashlib
    with open(os.path.join(SITE, path), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:10]


def head(lang, key, title, description):
    me = PAGES[key][0 if lang == "en" else 1]
    other = "ro" if lang == "en" else "en"
    ld = ""
    if key == "home":
        import json
        ld = '<script type="application/ld+json">' + json.dumps({
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": "Lanruj",
            "operatingSystem": "Linux",
            "applicationCategory": "ProductivityApplication",
            "description": description,
            "url": url_of(me),
            "image": f"{SITE_URL}/assets/img/og-{lang}.jpg",
            "license": "https://www.gnu.org/licenses/gpl-3.0.html",
            "isAccessibleForFree": True,
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
            "inLanguage": ["en", "ro"],
        }, ensure_ascii=False) + "</script>\n"
    return f'''<!doctype html>
<html lang="{lang}" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{url_of(me)}">
<link rel="alternate" hreflang="en" href="{url_of(PAGES[key][0])}" data-rel="{rel(me, PAGES[key][0])}">
<link rel="alternate" hreflang="ro" href="{url_of(PAGES[key][1])}" data-rel="{rel(me, PAGES[key][1])}">
<link rel="alternate" hreflang="x-default" href="{url_of(PAGES[key][0])}">
<meta name="theme-color" content="#fbf8f1" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#16202c" media="(prefers-color-scheme: dark)">
<meta name="color-scheme" content="light dark">
<link rel="icon" href="{rel(me, "assets/img/lanruj.svg")}" type="image/svg+xml">
<link rel="apple-touch-icon" href="{rel(me, "assets/img/apple-touch-icon.png")}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Lanruj">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{url_of(me)}">
<meta property="og:image" content="{SITE_URL}/assets/img/og-{lang}.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{"en_US" if lang == "en" else "ro_RO"}">
<meta property="og:locale:alternate" content="{"ro_RO" if lang == "en" else "en_US"}">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="{rel(me, "assets/css/style.css")}?v={version("assets/css/style.css")}">
<script src="{rel(me, "assets/js/main.js")}?v={version("assets/js/main.js")}" defer></script>
{ld}</head>
<body>
<a class="skip" href="#main">{"Skip to content" if lang == "en" else "Sari la conținut"}</a>
'''


def email_html(lang):
    if EMAIL:
        return f'<a class="button primary" href="mailto:{EMAIL}">{EMAIL}</a>'
    return '<span class="button primary soon">' + ("e-mail address coming soon" if lang == "en" else "adresa de e-mail, în curând") + "</span>"


CONTENT = {
    ("about", "en"): ("About Lanruj", "What Lanruj is, why it exists and how it is made.", '''
<section class="page-head"><div class="wrap narrow">
  <p class="eyebrow">About</p>
  <h1>A calm notebook on your computer</h1>
  <p class="lead">Lanruj is a bullet journal app for Linux. It keeps the method as it is on paper: short lines for tasks, events and notes, a page for each day, week and month, and a moment every evening to decide what is still worth doing.</p>
</div></section>
<section><div class="wrap narrow prose">
  <h2>Why Lanruj</h2>
  <p>Many note and to-do apps want an account, a subscription or a place in the cloud. Lanruj wants none of that. It is made for people who like the bullet journal method and want it on their computer too, without giving up their notes to anyone.</p>
  <h2>What it believes in</h2>
  <ul class="checks">
    <li>Your notes are plain Markdown files in a folder on your computer.</li>
    <li>It works offline, always, with no account and no ads.</li>
    <li>Encryption is there when you want it, with a recovery key.</li>
    <li>It is free software: anyone can read, change and share the code.</li>
  </ul>
  <h2>How it is made</h2>
  <p>Lanruj is written in Rust, with GTK 4 and libadwaita, so it fits naturally on the GNOME desktop. It speaks English and Romanian and comes with seven fonts for your pages, including two that look like handwriting.</p>
  <h2>Who makes it</h2>
  <p>Lanruj is built by Claude, the AI made by Anthropic, and tested by ThinkRoot. Ideas, bug reports and kind words are always welcome on the <a href="contact.html">contact page</a>.</p>
</div></section>
'''),
    ("about", "ro"): ("Despre Lanruj", "Ce este Lanruj, de ce există și cum este făcut.", '''
<section class="page-head"><div class="wrap narrow">
  <p class="eyebrow">Despre</p>
  <h1>Un caiet liniștit, pe calculatorul tău</h1>
  <p class="lead">Lanruj este o aplicație de tip „bullet journal” pentru Linux. Păstrează metoda așa cum este pe hârtie: rânduri scurte pentru sarcini, evenimente și notițe, câte o pagină pentru fiecare zi, săptămână și lună și un moment, în fiecare seară, în care hotărăști ce mai merită făcut.</p>
</div></section>
<section><div class="wrap narrow prose">
  <h2>De ce Lanruj</h2>
  <p>Multe aplicații de notițe și de sarcini îți cer un cont, un abonament sau un loc în cloud. Lanruj nu îți cere nimic din toate acestea. Este făcut pentru cei cărora le place metoda „bullet journal” și o vor și pe calculator, fără să-și dea notițele altcuiva.</p>
  <h2>Ce urmărește</h2>
  <ul class="checks">
    <li>Notițele tale sunt fișiere Markdown obișnuite, într-un dosar de pe calculatorul tău.</li>
    <li>Merge fără internet, fără cont și fără reclame.</li>
    <li>Criptarea îți stă la îndemână când ai nevoie de ea, cu o cheie de recuperare.</li>
    <li>Este un program liber: oricine poate citi, schimba și distribui codul.</li>
  </ul>
  <h2>Cum este făcut</h2>
  <p>Lanruj este scris în Rust, cu GTK 4 și libadwaita, așa că se potrivește firesc cu desktopul GNOME. Aplicația este în engleză și în română și vine cu șapte fonturi pentru pagini, dintre care două imită scrisul de mână.</p>
  <h2>Cine îl face</h2>
  <p>Lanruj este construit de Claude, inteligența artificială a companiei Anthropic, și testat de ThinkRoot. Ideile, problemele găsite și vorbele bune sunt binevenite pe <a href="contact.html">pagina de contact</a>.</p>
</div></section>
'''),
    ("contact", "en"): ("Contact - Lanruj", "How to get in touch about Lanruj: questions, ideas and bug reports.", '''
<section class="page-head"><div class="wrap narrow">
  <p class="eyebrow">Contact</p>
  <h1>Get in touch</h1>
  <p class="lead">Questions, ideas, a bug you found, or just a few words about how you use Lanruj: all of them are welcome.</p>
</div></section>
<section><div class="wrap narrow">
  <div class="contact-cards">
    <div class="contact-card">
      <h3>E-mail</h3>
      <p>For questions and anything you would rather not post in public.</p>
      EMAIL
    </div>
    <div class="contact-card">
      <h3>Bugs and ideas</h3>
      <p>Bug reports and feature ideas go to the project's issue tracker, where everyone can follow them.</p>
      <a class="button" href="https://github.com/ThinkRoot99/Lanruj/issues">Issues on GitHub</a>
    </div>
  </div>
  <p class="hint-text">When you report a bug, please mention your Linux distribution, how you installed Lanruj and the steps that lead to the problem. Never send your journal files or your password.</p>
</div></section>
'''),
    ("contact", "ro"): ("Contact - Lanruj", "Cum ne scrii despre Lanruj: întrebări, idei și probleme găsite.", '''
<section class="page-head"><div class="wrap narrow">
  <p class="eyebrow">Contact</p>
  <h1>Scrie-ne</h1>
  <p class="lead">Întrebări, idei, o problemă pe care ai găsit-o sau doar câteva cuvinte despre cum folosești Lanruj: toate sunt binevenite.</p>
</div></section>
<section><div class="wrap narrow">
  <div class="contact-cards">
    <div class="contact-card">
      <h3>E-mail</h3>
      <p>Pentru întrebări și pentru tot ce nu vrei să scrii în public.</p>
      EMAIL
    </div>
    <div class="contact-card">
      <h3>Probleme și idei</h3>
      <p>Problemele găsite și ideile de funcții noi ajung în lista de probleme a proiectului, unde le poate urmări oricine.</p>
      <a class="button" href="https://github.com/ThinkRoot99/Lanruj/issues">Problemele, pe GitHub</a>
    </div>
  </div>
  <p class="hint-text">Când semnalezi o problemă, spune-ne ce distribuție Linux folosești, cum ai instalat Lanruj și ce pași duc la problemă. Nu trimite niciodată fișierele jurnalului sau parola.</p>
</div></section>
'''),
    ("docs", "en"): ("Docs - Lanruj", "How to install, update and uninstall Lanruj, and how to use it.", '''
<section class="page-head"><div class="wrap narrow">
  <p class="eyebrow">Docs</p>
  <h1>Install and use Lanruj</h1>
  <p class="lead">How to install Lanruj, keep it up to date or remove it, and how to find your way around the app.</p>
</div></section>
<section><div class="wrap narrow prose">
  <h2 id="install">Installing</h2>
  <p>Lanruj comes as an AppImage and as a Flatpak. Both run on Debian 13, Ubuntu 24.04 and Linux Mint 22 or newer, Fedora, openSUSE Leap 16, Arch and other distributions at least as recent. You only need one of them.</p>
  <h3>AppImage</h3>
  <p>The AppImage is a single file that carries everything it needs; nothing else has to be installed.</p>
  <ol>
    <li><a href="APPIMAGE_URL">Download the AppImage</a> and put it where you want to keep it, for example in a folder called <code>Applications</code> in your home folder.</li>
    <li>Make it executable: right-click it, open Properties, then Permissions, and allow running it as a program. In a terminal, the same is <code>chmod +x Lanruj-VERSION-x86_64.AppImage</code>.</li>
    <li>Double-click it.</li>
  </ol>
  <p>At every start, Lanruj adds itself to the applications menu, so after the first start you can open it from there. If you move the file, the menu entry follows it at the next start.</p>
  <h3>Flatpak</h3>
  <p>Flatpak must be installed, with Flathub added. Most distributions have both; on Debian, run <code>sudo apt install flatpak</code> and follow the steps on <a href="https://flathub.org/setup">flathub.org/setup</a>. Then <a href="FLATPAK_URL">download the Flatpak</a> and install it from a terminal, in the folder where you saved it:</p>
  <ul>
    <li>for you only, without a password: <code>flatpak install --user lanruj.flatpak</code></li>
    <li>for all users of the computer, with your administrator password: <code>flatpak install lanruj.flatpak</code></li>
  </ul>
  <p>Flatpak downloads the GNOME runtime from Flathub if it is missing. Double-clicking the file works only where GNOME Software is installed. If Lanruj does not appear in the applications menu after your first Flatpak installation for yourself, log out and back in; on Cinnamon (Linux Mint), pressing Ctrl+Alt+Esc is enough.</p>
  <h2 id="update">Updating</h2>
  <p><strong>AppImage:</strong> download the new version, start it once, then delete the old file. <strong>Flatpak:</strong> download the new <code>lanruj.flatpak</code> and install it the same way as the first time. Your journal and your settings stay as they are.</p>
  <h2 id="uninstall">Uninstalling</h2>
  <p>Uninstalling removes the app, not your journal. If you turned them on, first turn off <em>Start with the computer</em> and <em>Remember the password on this computer</em> in Preferences, so nothing is left in your startup programs or in your keyring.</p>
  <p><strong>AppImage:</strong> delete the file, then its menu entry and icons:</p>
  <ul>
    <li><code>rm ~/.local/share/applications/io.github.ThinkRoot99.Lanruj.desktop</code></li>
    <li><code>rm ~/.local/share/icons/hicolor/scalable/apps/io.github.ThinkRoot99.Lanruj.svg</code></li>
    <li><code>rm ~/.local/share/icons/hicolor/symbolic/apps/io.github.ThinkRoot99.Lanruj-symbolic.svg</code></li>
  </ul>
  <p>The settings stay in <code>~/.config/lanruj</code>, <code>~/.local/state/lanruj</code> and <code>~/.cache/lanruj</code>; delete these folders too if you do not want to keep them.</p>
  <p><strong>Flatpak:</strong> run <code>flatpak uninstall --delete-data io.github.ThinkRoot99.Lanruj</code>, then <code>flatpak uninstall --unused</code> to remove the GNOME runtime if no other app needs it. If you installed Lanruj for you only, add <code>--user</code> to both commands.</p>
  <p><strong>Your journal</strong> stays in <code>~/.lanruj</code>, and the backups in <code>Documents/Lanruj - copii</code> or in the folder you chose. Delete them only if you are sure you no longer need what you wrote.</p>
  <h2 id="use">Using Lanruj</h2>
  <p>The first time you open Lanruj, it asks for the language, the paper, the font and whether to encrypt the journal. You can change all of them later in Preferences. The guide in the app (F1) explains everything step by step; here is the short version.</p>
  <h3>Day, week and month pages</h3>
  <p>Each day has its own page, and the week and the month have theirs. You write short lines in the field at the bottom: start a line with <code>.</code> for a task, <code>o</code> for an event or <code>-</code> for a note, then press Enter. Add <code>*</code> after the sign to mark something important, or <code>!</code> for an idea. Ctrl+Enter ticks a task when it is done. The future log holds what is further ahead.</p>
  <h3>Migration</h3>
  <p>In the evening, Ctrl+M takes you through the tasks you did not finish, one by one. For each, you decide: move it to the next day, schedule it for a later date, drop it or leave it where it is.</p>
  <h3>Journal</h3>
  <p>The journal is for writing at length, one page per day. You can use headings, lists, quotes, colours and different fonts, and link a piece of text to a day, a task or Tracking. Ctrl+Shift+O starts a new entry with the current time.</p>
  <h3>Tracking</h3>
  <p>Tracking follows your habits and activities, your sleep and your work days, month by month, with charts and sheets you can print.</p>
  <h3>Index, search and notes</h3>
  <p>The Index keeps the days and pages you want to find again; Ctrl+I adds the day you are looking at. Ctrl+F searches everywhere. Ctrl+N opens a note: a small slip for a quick idea, which stays on every page until you delete it.</p>
  <h3>Backups, lock and encryption</h3>
  <p>Lanruj makes backups of your journal on its own. In Preferences, under Security, you can lock the app with a password or a PIN, lock it when the screen locks, and encrypt the whole journal.</p>
  <h3>Keyboard shortcuts</h3>
  <p>Almost everything can be done from the keyboard. Ctrl+? shows all the shortcuts in the app, and the <a href="https://github.com/ThinkRoot99/Lanruj/wiki/Keyboard-shortcuts">keyboard shortcuts page</a> in the project wiki explains each one.</p>
</div></section>
'''),
    ("docs", "ro"): ("Documentație - Lanruj", "Cum instalezi, actualizezi și dezinstalezi Lanruj și cum îl folosești.", '''
<section class="page-head"><div class="wrap narrow">
  <p class="eyebrow">Documentație</p>
  <h1>Instalarea și folosirea lui Lanruj</h1>
  <p class="lead">Cum instalezi Lanruj, cum îl ții la zi sau îl dezinstalezi și cum te descurci în aplicație.</p>
</div></section>
<section><div class="wrap narrow prose">
  <h2 id="instalare">Instalarea</h2>
  <p>Lanruj vine ca AppImage și ca Flatpak. Amândouă merg pe Debian 13, pe Ubuntu 24.04 și Linux Mint 22 sau mai noi, pe Fedora, openSUSE Leap 16, Arch și alte distribuții cel puțin la fel de noi. Ai nevoie doar de unul dintre ele.</p>
  <h3>AppImage</h3>
  <p>AppImage-ul e un singur fișier care are în el tot ce-i trebuie; nu mai trebuie instalat nimic altceva.</p>
  <ol>
    <li><a href="APPIMAGE_URL">Descarcă AppImage-ul</a> și pune-l unde vrei să-l păstrezi, de exemplu într-un dosar numit <code>Aplicații</code> din dosarul tău personal.</li>
    <li>Dă-i drept de rulare: clic dreapta pe el, Proprietăți, apoi Permisiuni, și bifează că poate fi rulat ca program. Din terminal, același lucru se face cu <code>chmod +x Lanruj-VERSION-x86_64.AppImage</code>.</li>
    <li>Deschide-l cu dublu clic.</li>
  </ol>
  <p>La fiecare pornire, Lanruj se adaugă singur în meniul de aplicații, așa că după prima pornire îl poți deschide de acolo. Dacă muți fișierul, lansatorul din meniu îl urmează la pornirea următoare.</p>
  <h3>Flatpak</h3>
  <p>Flatpak trebuie să fie instalat, iar Flathub adăugat. Cele mai multe distribuții le au pe amândouă; pe Debian, rulează <code>sudo apt install flatpak</code> și urmează pașii de pe <a href="https://flathub.org/setup">flathub.org/setup</a>. Apoi <a href="FLATPAK_URL">descarcă pachetul Flatpak</a> și instalează-l din terminal, din dosarul în care l-ai salvat:</p>
  <ul>
    <li>doar pentru tine, fără parolă: <code>flatpak install --user lanruj.flatpak</code></li>
    <li>pentru toți utilizatorii calculatorului, cu parola de administrator: <code>flatpak install lanruj.flatpak</code></li>
  </ul>
  <p>Dacă mediul GNOME lipsește, Flatpak îl descarcă de pe Flathub. Dublul clic pe fișier merge doar unde e instalat GNOME Software. Dacă Lanruj nu apare în meniul de aplicații după prima ta instalare Flatpak doar pentru tine, ieși din sesiune și intră din nou; pe Cinnamon (Linux Mint) ajunge să apeși Ctrl+Alt+Esc.</p>
  <h2 id="actualizare">Actualizarea</h2>
  <p><strong>AppImage:</strong> descarci versiunea nouă, o pornești o dată, apoi ștergi fișierul vechi. <strong>Flatpak:</strong> descarci noul <code>lanruj.flatpak</code> și îl instalezi la fel ca prima dată. Jurnalul și setările rămân neatinse.</p>
  <h2 id="dezinstalare">Dezinstalarea</h2>
  <p>Dezinstalarea scoate aplicația, nu și jurnalul. Dacă le-ai pornit, oprește întâi din Setări <em>Pornește odată cu calculatorul</em> și <em>Ține minte parola pe acest calculator</em>, ca să nu rămână nimic în programele de pornire sau în portofelul de chei.</p>
  <p><strong>AppImage:</strong> ștergi fișierul, apoi lansatorul din meniu și iconițele:</p>
  <ul>
    <li><code>rm ~/.local/share/applications/io.github.ThinkRoot99.Lanruj.desktop</code></li>
    <li><code>rm ~/.local/share/icons/hicolor/scalable/apps/io.github.ThinkRoot99.Lanruj.svg</code></li>
    <li><code>rm ~/.local/share/icons/hicolor/symbolic/apps/io.github.ThinkRoot99.Lanruj-symbolic.svg</code></li>
  </ul>
  <p>Setările rămân în <code>~/.config/lanruj</code>, <code>~/.local/state/lanruj</code> și <code>~/.cache/lanruj</code>; șterge și aceste dosare dacă nu vrei să le păstrezi.</p>
  <p><strong>Flatpak:</strong> rulează <code>flatpak uninstall --delete-data io.github.ThinkRoot99.Lanruj</code>, apoi <code>flatpak uninstall --unused</code>, care scoate și mediul GNOME dacă nu-l mai folosește altă aplicație. Dacă ai instalat Lanruj doar pentru tine, adaugă <code>--user</code> la amândouă comenzile.</p>
  <p><strong>Jurnalul</strong> rămâne în <code>~/.lanruj</code>, iar copiile de siguranță în <code>Documente/Lanruj - copii</code> sau în dosarul ales de tine. Șterge-le doar dacă ești sigur că nu mai ai nevoie de ce ai scris.</p>
  <h2 id="folosire">Folosirea</h2>
  <p>Prima dată când deschizi Lanruj, te întreabă limba, hârtia, fontul și dacă vrei jurnalul criptat. Le poți schimba pe toate mai târziu, din Setări. Ghidul din aplicație (F1) explică totul pas cu pas; iată pe scurt.</p>
  <h3>Paginile zilei, săptămânii și lunii</h3>
  <p>Fiecare zi are pagina ei, la fel săptămâna și luna. Scrii rânduri scurte în câmpul de jos: începi rândul cu <code>.</code> pentru o sarcină, cu <code>o</code> pentru un eveniment sau cu <code>-</code> pentru o notiță, apoi apeși Enter. Pune <code>*</code> după semn ca să însemni ceva important sau <code>!</code> pentru o idee. Ctrl+Enter bifează o sarcină când e gata. În Planuri ții ce e mai departe în timp.</p>
  <h3>Migrarea</h3>
  <p>Seara, Ctrl+M te trece pe rând prin sarcinile pe care nu le-ai terminat. Pentru fiecare hotărăști: o muți pe ziua următoare, o programezi pe mai târziu, renunți la ea sau o lași unde este.</p>
  <h3>Jurnalul</h3>
  <p>Jurnalul e pentru scris pe larg, câte o pagină pe zi. Poți folosi titluri, liste, citate, culori și fonturi diferite și poți lega o bucată de text de o zi, de o sarcină sau de Monitorizare. Ctrl+Shift+O începe o însemnare nouă cu ora de acum.</p>
  <h3>Monitorizarea</h3>
  <p>Monitorizarea urmărește obiceiurile și activitățile tale, somnul și zilele de serviciu, lună de lună, cu grafice și foi de tipărit.</p>
  <h3>Indexul, căutarea și biletele</h3>
  <p>Indexul păstrează zilele și paginile pe care vrei să le regăsești; Ctrl+I adaugă ziua pe care o vezi. Ctrl+F caută peste tot. Ctrl+N deschide un bilet: o hârtiuță pentru o idee rapidă, care rămâne pe fiecare pagină până o ștergi.</p>
  <h3>Copiile de siguranță, blocarea și criptarea</h3>
  <p>Lanruj face singur copii de siguranță ale jurnalului. Din Setări, la Siguranță, poți bloca aplicația cu o parolă sau un PIN, o poți bloca odată cu ecranul și poți cripta tot jurnalul.</p>
  <h3>Scurtăturile de taste</h3>
  <p>Aproape totul se poate face de la tastatură. Ctrl+? arată în aplicație toate scurtăturile, iar <a href="https://github.com/ThinkRoot99/Lanruj/wiki/Scurtături-de-taste">pagina cu scurtăturile de taste</a> din wiki-ul proiectului le explică pe fiecare.</p>
</div></section>
'''),
    ("privacy", "en"): ("Privacy policy - Lanruj", "Lanruj collects no data: the app works offline and the website uses no cookies or tracking.", '''
<section class="page-head"><div class="wrap narrow">
  <p class="eyebrow">Privacy</p>
  <h1>Privacy policy</h1>
  <p class="lead">In short: Lanruj does not collect anything about you. Your journal stays on your computer, and this website does not track you.</p>
  <p class="updated">Last updated: 27 November 2026</p>
</div></section>
<section><div class="wrap narrow prose">
  <h2>The app</h2>
  <ul>
    <li><b>No data leaves your computer.</b> Lanruj has no account, no cloud, no statistics and no telemetry. It does not connect to the internet on its own; it only opens a link in your browser when you click one.</li>
    <li><b>Your journal is a folder of files</b> (<code>~/.lanruj</code>) on your computer. Backups and exported archives go only where you choose.</li>
    <li><b>Encryption is optional.</b> When it is on, your files are encrypted on your computer with your password. Nobody else, including the author of Lanruj, can read them or recover the password.</li>
    <li><b>The keyring is optional.</b> If you ask Lanruj to remember the password, it is kept in your system's keyring, on your computer.</li>
    <li><b>Syncing is your choice.</b> If you sync the journal between computers, for example with Syncthing, the files travel between your own devices, as you set it up.</li>
  </ul>
  <h2>This website</h2>
  <ul>
    <li><b>No cookies, no analytics, no ads.</b> The site loads no fonts, scripts or images from other websites.</li>
    <li><b>Your language choice</b> is kept in your browser's local storage, on your device, only so the site opens in the language you picked. You can clear it from your browser at any time.</li>
    <li><b>Server logs.</b> Like most websites, the server that hosts this site may keep standard access logs (such as the address of your device and the time of the visit) for security and to keep the site running. They are not used to identify or follow you.</li>
  </ul>
  <h2>Contact</h2>
  <p>For any question about privacy, see the <a href="contact.html">contact page</a>.</p>
</div></section>
'''),
    ("privacy", "ro"): ("Politica de confidențialitate - Lanruj", "Lanruj nu adună niciun fel de date: aplicația funcționează fără internet, iar site-ul nu folosește cookie-uri și nu te urmărește.", '''
<section class="page-head"><div class="wrap narrow">
  <p class="eyebrow">Confidențialitate</p>
  <h1>Politica de confidențialitate</h1>
  <p class="lead">Pe scurt: Lanruj nu adună nimic despre tine. Jurnalul tău rămâne pe calculatorul tău, iar site-ul acesta nu te urmărește.</p>
  <p class="updated">Ultima actualizare: 27 noiembrie 2026</p>
</div></section>
<section><div class="wrap narrow prose">
  <h2>Aplicația</h2>
  <ul>
    <li><b>Nicio informație nu pleacă de pe calculatorul tău.</b> Lanruj nu are cont, cloud, statistici sau telemetrie. Nu se conectează singur la internet; deschide o legătură în browser doar când dai clic pe ea.</li>
    <li><b>Jurnalul tău este un dosar cu fișiere</b> (<code>~/.lanruj</code>) pe calculatorul tău. Copiile de siguranță și arhivele exportate ajung doar unde alegi tu.</li>
    <li><b>Criptarea este opțională.</b> Când este pornită, fișierele sunt criptate pe calculatorul tău, cu parola ta. Nimeni altcineva, nici autorul aplicației, nu le poate citi și nu poate recupera parola.</li>
    <li><b>Portofelul de chei este opțional.</b> Dacă ceri ca parola să fie ținută minte, ea stă în portofelul de chei al sistemului, pe calculatorul tău.</li>
    <li><b>Sincronizarea este alegerea ta.</b> Dacă sincronizezi jurnalul între calculatoare, de exemplu cu Syncthing, fișierele circulă între propriile tale dispozitive, așa cum le-ai legat tu.</li>
  </ul>
  <h2>Site-ul</h2>
  <ul>
    <li><b>Fără cookie-uri, fără statistici, fără reclame.</b> Site-ul nu încarcă fonturi, scripturi sau imagini de pe alte site-uri.</li>
    <li><b>Limba aleasă</b> este ținută în memoria locală a browserului, pe dispozitivul tău, doar ca site-ul să se deschidă în limba pe care ai ales-o. O poți șterge oricând din browser.</li>
    <li><b>Jurnalele serverului.</b> Ca majoritatea site-urilor, serverul care găzduiește site-ul poate păstra jurnale obișnuite de acces (de exemplu adresa dispozitivului tău și ora vizitei), pentru siguranță și ca site-ul să funcționeze. Ele nu sunt folosite ca să te identifice sau să te urmărească.</li>
  </ul>
  <h2>Contact</h2>
  <p>Pentru orice întrebare despre confidențialitate, vezi <a href="contact.html">pagina de contact</a>.</p>
</div></section>
'''),
}


def build():
    for key in ("docs", "about", "contact", "privacy"):
        for lang in ("en", "ro"):
            title, desc, body = CONTENT[(key, lang)]
            body = body.replace("EMAIL", email_html(lang)).replace("APPIMAGE_URL", APPIMAGE_URL).replace("FLATPAK_URL", FLATPAK_URL).replace("VERSION", VERSION)
            out = head(lang, key, title, desc) + header(lang, key) + "\n\n<main id=\"main\">\n" + body + "\n</main>\n\n" + footer(lang, key) + "\n\n</body>\n</html>\n"
            path = os.path.join(SITE, PAGES[key][0 if lang == "en" else 1])
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(out)
    # Paginile de început: doar meniul, subsolul și legăturile din <head>.
    for lang in ("en", "ro"):
        path = os.path.join(SITE, PAGES["home"][0 if lang == "en" else 1])
        with open(path, encoding="utf-8") as f:
            s = f.read()
        s = re.sub(r"<header class=\"top\">.*?</header>", lambda _: header(lang, "home"), s, count=1, flags=re.S)
        s = re.sub(r"<footer>.*?</footer>", lambda _: footer(lang, "home"), s, count=1, flags=re.S)
        # Butoanele de descărcare duc la pachetele versiunii publicate.
        s = re.sub(r"releases/download/v[0-9.]+/Lanruj-[0-9.]+-x86_64\.AppImage", f"releases/download/v{VERSION}/Lanruj-{VERSION}-x86_64.AppImage", s)
        s = re.sub(r"releases/download/v[0-9.]+/lanruj\.flatpak", f"releases/download/v{VERSION}/lanruj.flatpak", s)
        start = s.index("<!doctype html>")
        end = s.index("<body>") + len("<body>\n")
        title = re.search(r"<title>(.*?)</title>", s).group(1)
        desc = re.search(r'<meta name="description" content="(.*?)">', s).group(1)
        s = s[:start] + head(lang, "home", title, desc) + re.sub(r'^<a class="skip"[^\n]*\n', "", s[end:])
        s = s.replace("<main>", '<main id="main">', 1)
        with open(path, "w", encoding="utf-8") as f:
            f.write(s)
    extras()
    print("gata")


def extras():
    """sitemap.xml, robots.txt, pagina 404 și .htaccess (Apache: pagina 404, compresia, memorarea în browser)."""
    from datetime import date
    today = date.today().isoformat()
    urls = []
    for key, (en, ro) in PAGES.items():
        for me in (en, ro):
            alts = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{url_of(p)}"/>' for l, p in (("en", en), ("ro", ro)))
            urls.append(f"  <url>\n    <loc>{url_of(me)}</loc>\n    <lastmod>{today}</lastmod>{alts}\n  </url>")
    with open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
                + "\n".join(urls) + "\n</urlset>\n")
    with open(os.path.join(SITE, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
    # Pagina 404: în amândouă limbile, cu adrese de la rădăcină (merge din orice dosar).
    css, js = version("assets/css/style.css"), version("assets/js/main.js")
    with open(os.path.join(SITE, "404.html"), "w", encoding="utf-8") as f:
        f.write(f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page not found · Lanruj</title>
<meta name="robots" content="noindex">
<link rel="icon" href="/assets/img/lanruj.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/css/style.css?v={css}">
</head>
<body>
<main id="main" class="lost">
  <div class="wrap">
    <img src="/assets/img/lanruj.svg" alt="" width="88" height="88">
    <h1>This page is not in the journal</h1>
    <p>The address may be wrong, or the page has moved.</p>
    <p><a class="button primary" href="/">Go to the home page</a></p>
    <p lang="ro" class="lost-ro">Pagina nu e în jurnal: adresa poate fi greșită sau pagina s-a mutat. <a href="/lang/ro/">Mergi la prima pagină</a>.</p>
  </div>
</main>
</body>
</html>
''')
    with open(os.path.join(SITE, ".htaccess"), "w", encoding="utf-8") as f:
        f.write('''# Lanruj - site. Fișier făcut de tools/pagini.py.
ErrorDocument 404 /404.html
Options -Indexes
AddDefaultCharset utf-8
AddType image/webp .webp
AddType image/svg+xml .svg

# HTTPS și fără „www.”
<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteCond %{HTTPS} off
    RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
    RewriteCond %{HTTP_HOST} ^www\\.(.+)$ [NC]
    RewriteRule ^ https://%1%{REQUEST_URI} [L,R=301]
</IfModule>

# compresie
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/css text/plain application/javascript application/json application/ld+json image/svg+xml application/xml
</IfModule>

# memorarea în browser: stilul și scriptul au amprenta în adresă (?v=…), deci pot sta un an
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresDefault "access plus 1 hour"
    ExpiresByType text/html "access plus 0 seconds"
    ExpiresByType text/css "access plus 1 year"
    ExpiresByType application/javascript "access plus 1 year"
    ExpiresByType image/webp "access plus 1 month"
    ExpiresByType image/jpeg "access plus 1 month"
    ExpiresByType image/png "access plus 1 month"
    ExpiresByType image/svg+xml "access plus 1 month"
</IfModule>

# antete de siguranță
<IfModule mod_headers.c>
    Header always set X-Content-Type-Options "nosniff"
    Header always set Referrer-Policy "strict-origin-when-cross-origin"
    Header always set X-Frame-Options "SAMEORIGIN"
    Header always set Permissions-Policy "camera=(), microphone=(), geolocation=()"
</IfModule>

# notițele și uneltele de lucru nu sunt pentru vizitatori
<FilesMatch "(?i)(\\.(py|md|sh)$|^README|^LICENSE)">
    Require all denied
</FilesMatch>
RedirectMatch 403 ^/tools(/|$)
''')


if __name__ == "__main__":
    build()
