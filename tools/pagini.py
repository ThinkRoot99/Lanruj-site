#!/usr/bin/env python3
"""Paginile site-ului Lanruj: meniul de sus și subsolul comune, plus paginile Despre, Contact
și Politica de confidențialitate, în engleză (rădăcina) și română (lang/ro/).
Paginile de început (index.html, lang/ro/index.html) își păstrează conținutul; li se refac
doar meniul și subsolul. Folosire: python3 site/tools/pagini.py"""
import os
import re

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Adresa de contact: de completat de autor (până atunci apare un loc marcat).
EMAIL = ""

PAGES = {
    # cheie: (fișier EN, fișier RO)
    "home": ("index.html", "lang/ro/index.html"),
    "about": ("about.html", "lang/ro/despre.html"),
    "contact": ("contact.html", "lang/ro/contact.html"),
    "privacy": ("privacy.html", "lang/ro/confidentialitate.html"),
}
NAV = {
    "en": [("home", "Home"), ("about", "About"), ("contact", "Contact"), ("privacy", "Privacy")],
    "ro": [("home", "Acasă"), ("about", "Despre"), ("contact", "Contact"), ("privacy", "Confidențialitate")],
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
        <p class="sign">made by ThinkRoot</p>
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
        <p>Jurnal de tip „bullet journal”, pe Linux.</p>
        <p class="sign">creat de ThinkRoot</p>
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
          <li><a href="{a("about")}">Despre</a></li>
          <li><a href="{a("contact")}">Contact</a></li>
          <li><a href="{a("privacy")}">Politica de confidențialitate</a></li>
        </ul>
      </div>
    </div>
    <p class="legal copy"><span class="copyleft" role="img" aria-label="Copyleft">©</span> 2026 Lanruj</p>
    <p class="legal">Lanruj este un program liber, sub licența GPL-3.0-or-later. Bullet Journal este o metodă creată de Ryder Carroll; Lanruj este o aplicație independentă și nu este afiliată metodei sau autorului ei.</p>
  </div>
</footer>'''


def head(lang, key, title, description):
    me = PAGES[key][0 if lang == "en" else 1]
    return f'''<!doctype html>
<html lang="{lang}" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="icon" href="{rel(me, "assets/img/lanruj.svg")}" type="image/svg+xml">
<link rel="alternate" hreflang="en" href="{rel(me, PAGES[key][0])}">
<link rel="alternate" hreflang="ro" href="{rel(me, PAGES[key][1])}">
<link rel="stylesheet" href="{rel(me, "assets/css/style.css")}">
<script src="{rel(me, "assets/js/main.js")}" defer></script>
</head>
<body>
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
  <p>Lanruj is made by ThinkRoot, an independent developer. Ideas, bug reports and kind words are always welcome on the <a href="contact.html">contact page</a>.</p>
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
    <li>Funcționează și fără internet, mereu, fără cont și fără reclame.</li>
    <li>Criptarea este acolo când ai nevoie de ea, cu o cheie de recuperare.</li>
    <li>Este un program liber: oricine poate citi, schimba și împărți codul.</li>
  </ul>
  <h2>Cum este făcut</h2>
  <p>Lanruj este scris în Rust, cu GTK 4 și libadwaita, așa că se potrivește firesc cu desktopul GNOME. Vorbește română și engleză și vine cu șapte fonturi pentru pagini, dintre care două arată ca scrisul de mână.</p>
  <h2>Cine îl face</h2>
  <p>Lanruj este făcut de ThinkRoot, un dezvoltator independent. Ideile, problemele găsite și vorbele bune sunt binevenite pe <a href="contact.html">pagina de contact</a>.</p>
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
      <span class="button soon">Forgejo and GitHub, coming soon</span>
    </div>
  </div>
  <p class="hint-text">When you report a bug, please mention your Linux distribution, how you installed Lanruj and the steps that lead to the problem. Never send your journal files or your password.</p>
</div></section>
'''),
    ("contact", "ro"): ("Contact - Lanruj", "Cum iei legătura în legătură cu Lanruj: întrebări, idei și probleme găsite.", '''
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
      <p>Problemele găsite și ideile de funcții noi merg în lista proiectului, unde le poate urmări oricine.</p>
      <span class="button soon">Forgejo și GitHub, în curând</span>
    </div>
  </div>
  <p class="hint-text">Când semnalezi o problemă, spune-ne ce distribuție Linux folosești, cum ai instalat Lanruj și ce pași duc la problemă. Nu trimite niciodată fișierele jurnalului sau parola.</p>
</div></section>
'''),
    ("privacy", "en"): ("Privacy policy - Lanruj", "Lanruj collects no data: the app works offline and the website uses no cookies or tracking.", '''
<section class="page-head"><div class="wrap narrow">
  <p class="eyebrow">Privacy</p>
  <h1>Privacy policy</h1>
  <p class="lead">In short: Lanruj does not collect anything about you. Your journal stays on your computer, and this website does not track you.</p>
  <p class="updated">Last updated: 21 November 2026</p>
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
    ("privacy", "ro"): ("Politica de confidențialitate - Lanruj", "Lanruj nu adună nicio dată: aplicația funcționează fără internet, iar site-ul nu folosește cookie-uri sau urmărire.", '''
<section class="page-head"><div class="wrap narrow">
  <p class="eyebrow">Confidențialitate</p>
  <h1>Politica de confidențialitate</h1>
  <p class="lead">Pe scurt: Lanruj nu adună nimic despre tine. Jurnalul tău rămâne pe calculatorul tău, iar site-ul acesta nu te urmărește.</p>
  <p class="updated">Ultima actualizare: 21 noiembrie 2026</p>
</div></section>
<section><div class="wrap narrow prose">
  <h2>Aplicația</h2>
  <ul>
    <li><b>Nicio dată nu pleacă de pe calculatorul tău.</b> Lanruj nu are cont, cloud, statistici sau telemetrie. Nu se conectează singur la internet; deschide o legătură în browser doar când dai clic pe ea.</li>
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
    for key in ("about", "contact", "privacy"):
        for lang in ("en", "ro"):
            title, desc, body = CONTENT[(key, lang)]
            body = body.replace("EMAIL", email_html(lang))
            out = head(lang, key, title, desc) + header(lang, key) + "\n\n<main>\n" + body + "\n</main>\n\n" + footer(lang, key) + "\n\n</body>\n</html>\n"
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
        start = s.index("<!doctype html>")
        end = s.index("<body>") + len("<body>\n")
        title = re.search(r"<title>(.*?)</title>", s).group(1)
        desc = re.search(r'<meta name="description" content="(.*?)">', s).group(1)
        s = s[:start] + head(lang, "home", title, desc) + s[end:]
        with open(path, "w", encoding="utf-8") as f:
            f.write(s)
    print("gata")


if __name__ == "__main__":
    build()
