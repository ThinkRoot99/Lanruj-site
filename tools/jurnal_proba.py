#!/usr/bin/env python3
"""Un jurnal de probă, în engleză sau în română, pentru capturile de pe site (fără nimic personal).
Are zilele 19-21 noiembrie 2026, luna, săptămânile, Planurile, Indexul, o zi de Jurnal,
Monitorizarea lunii și două bilete. Capturile se fac cu LANRUJ_AZI=2026-11-21.
Folosire: python3 tools/jurnal_proba.py <en|ro> <dosar>"""
import os
import random
import sys

from PIL import Image, ImageDraw

LANG, ROOT = sys.argv[1], sys.argv[2]
RO = LANG == "ro"


def write(path, text):
    p = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)


def picture(path, sky, sun, hills):
    """O poză simplă: cer, soare, dealuri."""
    p = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    w, h = 900, 600
    img = Image.new("RGB", (w, h), sky[0])
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        c = tuple(int(sky[0][i] * (1 - t) + sky[1][i] * t) for i in range(3))
        d.line([(0, y), (w, y)], fill=c)
    d.ellipse([560, 120, 720, 280], fill=sun)
    d.polygon([(0, 420), (220, 300), (480, 430), (700, 330), (900, 420), (900, 600), (0, 600)], fill=hills[0])
    d.polygon([(0, 500), (300, 420), (620, 520), (900, 460), (900, 600), (0, 600)], fill=hills[1])
    img.save(p, quality=88)


T = {
    "2026/11/2026-11-19.md": ("""# Thursday, 19 November 2026

- o 10:00 Project presentation
- [x] * Send the slides to the team
- [x] Book the train tickets to Vienna
- [>] Fix the kitchen shelf ^sh01
- Rain all day, <span style="color:#1c71d8">a good day for reading</span>
- [x] Call grandma

Tags: work, family
Day: 4/5
""", """# Joi, 19 noiembrie 2026

- o 10:00 Prezentarea proiectului
- [x] * Trimite slide-urile echipei
- [x] Cumpără biletele de tren spre Viena
- [>] Repară raftul din bucătărie ^sh01
- Ploaie toată ziua, <span style="color:#1c71d8">o zi bună de citit</span>
- [x] Sună-o pe bunica

Etichete: serviciu, familie
Ziua: 4/5
"""),
    "2026/11/2026-11-20.md": ("""# Friday, 20 November 2026

- o 18:30 Dinner with the family
- [ ] Buy light bulbs for the hallway ^bl02
- [ ] <span style="color:#c01c28">Car service</span> for the winter tyres ^cs03
- [ ] * Send the ==monthly report==
- [x] Walk in the park, 30 minutes
  - cold, but sunny
- <span style="color:#26a269">Finished the book I started last month</span>
- [ ] Look for a desk lamp

Tags: books, health
Day: 4/5
""", """# Vineri, 20 noiembrie 2026

- o 18:30 Cină cu familia
- [ ] Cumpără becuri pentru hol ^bl02
- [ ] <span style="color:#c01c28">Service</span> pentru anvelopele de iarnă ^cs03
- [ ] * Trimite ==raportul lunar==
- [x] Plimbare în parc, 30 de minute
  - frig, dar senin
- <span style="color:#26a269">Am terminat cartea începută luna trecută</span>
- [ ] Caută o lampă de birou

Etichete: cărți, sănătate
Ziua: 4/5
"""),
    "2026/11/2026-11-21.md": ("""# Saturday, 21 November 2026

- o 11:00 Farmers' market with mum ^pi04
- [ ] Wash the car
- [ ] ! Try grandma's ==apple pie recipe==
- [ ] Fix the kitchen shelf ^sh01
- Trip notes: [opening hours](https://example.org/museum)
- o 16:00 Coffee with Ana
  ![Sunset on the hill|220](2026-11-21/sunset.jpg)
- [ ] Pack for Vienna

Tags: home
""", """# Sâmbătă, 21 noiembrie 2026

- o 11:00 Piața cu mama ^pi04
- [ ] Spală mașina
- [ ] ! Încearcă ==rețeta de plăcintă== a bunicii
- [ ] Repară raftul din bucătărie ^sh01
- Pentru excursie: [programul muzeului](https://example.org/museum)
- o 16:00 Cafea cu Ana
  ![Apus pe deal|220](2026-11-21/apus.jpg)
- [ ] Fă bagajul pentru Viena

Etichete: acasă
"""),
    "2026/11/luna.md": ("""# November 2026

## Calendar

- 9 Dentist, check-up
- 11 Residents' association meeting
- 25 Eye doctor
- 30 Andrei's birthday

## Tasks

- [x] * Book the family doctor ^fd01
- [ ] Car service
  - the garage on Factory Street
- [ ] Renew the internet subscription
- [x] Pay the property tax
- [ ] ! Plan the winter holiday
- Idea: home-made presents this year
""", """# Noiembrie 2026

## Calendar

- 9 Dentist, control
- 11 Ședința asociației de proprietari
- 25 Oftalmolog
- 30 Ziua lui Andrei

## Sarcini

- [x] * Programare la medicul de familie ^fd01
- [ ] Service pentru mașină
  - atelierul de pe strada Fabricii
- [ ] Reînnoiește abonamentul la internet
- [x] Plătește impozitul pe casă
- [ ] ! Plănuiește vacanța de iarnă
- Idee: cadouri făcute în casă anul acesta
"""),
    "2026/12/luna.md": ("""# December 2026

## Calendar

- 6 St Nicholas
- 24 Christmas Eve with the parents
- 31 18:00 New Year's Eve with friends

## Tasks

- [ ] Buy the Christmas presents
- [ ] * Make next year's budget
""", """# Decembrie 2026

## Calendar

- 6 Moș Nicolae
- 24 Ajunul Crăciunului cu părinții
- 31 18:00 Revelionul cu prietenii

## Sarcini

- [ ] Cumpără cadourile de Crăciun
- [ ] * Fă bugetul pe anul viitor
"""),
    "2026/saptamani/2026-S47.md": ("""# Week 47, 16-22 November 2026

- [ ] Fix the kitchen shelf ^sh01
- [x] * Finish the project presentation
- [ ] Read two chapters a day
- [ ] Gym three times
  - Monday and Wednesday done, Friday left
""", """# Săptămâna 47, 16-22 noiembrie 2026

- [ ] Repară raftul din bucătărie ^sh01
- [x] * Termină prezentarea proiectului
- [ ] Citește două capitole pe zi
- [ ] Sală de trei ori
  - luni și miercuri gata, a rămas vineri
"""),
    "2026/saptamani/2026-S48.md": ("""# Week 48, 23-29 November 2026

- [ ] Get the house ready for winter
- [ ] ! Start the present list
""", """# Săptămâna 48, 23-29 noiembrie 2026

- [ ] Pregătește casa pentru iarnă
- [ ] ! Începe lista de cadouri
"""),
    "viitor.md": ("""# Plans

## December 2026

- [ ] 15 Car service at 60,000 km
- o 20 Christmas market with friends
- [ ] Renew the gym membership

## January 2027

- [ ] * 20 Tax return
- [ ] Yearly check-up at the family doctor

## February 2027

- o 14 Dinner out
- [ ] Change the car oil

## March 2027

- [ ] Spring cleaning
""", """# Planuri

## Decembrie 2026

- [ ] 15 Revizia mașinii la 60.000 km
- o 20 Târgul de Crăciun cu prietenii
- [ ] Reînnoiește abonamentul la sală

## Ianuarie 2027

- [ ] * 20 Declarația de impozit
- [ ] Controlul anual la medicul de familie

## Februarie 2027

- o 14 Cină în oraș
- [ ] Schimbă uleiul la mașină

## Martie 2027

- [ ] Curățenia de primăvară
"""),
    "pagini/2026-11-23.md": ("""# Trip to Vienna

- o 23 November 07:40 Train from the central station
- [ ] Book the Belvedere tickets
- [x] Hotel near the Naschmarkt
- Café list: Central, Sperl, Hawelka
""", """# Excursie la Viena

- o 23 noiembrie 07:40 Trenul din Gara de Nord
- [ ] Cumpără biletele la Belvedere
- [x] Hotel lângă Naschmarkt
- Cafenele: Central, Sperl, Hawelka
"""),
    "index.md": ("""# Index

- [Trip to Vienna](pagini/2026-11-23.md): [23-27 November 2026](2026/11/2026-11-23.md)
- [Project presentation](2026/11/2026-11-19.md): 19 November 2026
""", """# Index

- [Excursie la Viena](pagini/2026-11-23.md): [23-27 noiembrie 2026](2026/11/2026-11-23.md)
- [Prezentarea proiectului](2026/11/2026-11-19.md): 19 noiembrie 2026
"""),
    # Jurnalul zilei: scris pe larg, cu titlu, subtitlu, ora, formatare, o listă și o legătură spre un rând.
    "jurnal/2026/2026-11-21.md": ("""# Journal · 21 November 2026

## <span style="font-family:Caveat"><span style="font-size:125%">A slow Saturday</span></span>

### 09:10
I woke up before the alarm and stayed in bed a little longer, listening to the rain. Coffee, a few pages of the new book and **no screens** until ten.

### Morning
The [market with mum](lanruj:intrare/zi/2026-11-21/pi04) was full of apples and pumpkins. She told me again how grandma made her *apple pie*: thin pastry, a lot of cinnamon and ==patience==.

- apples, walnuts and honey
- a pumpkin for the soup
- flowers for the kitchen table

### 16:40
Coffee with Ana. We talked about the trip to Vienna and about how fast this year went.

> Write it down, or it didn't happen.

Tonight: pack the bag, then read until I fall asleep.
""", """# Jurnal · 21 noiembrie 2026

## <span style="font-family:Caveat"><span style="font-size:125%">O sâmbătă fără grabă</span></span>

### 09:10
M-am trezit înainte de alarmă și am mai stat puțin în pat, ascultând ploaia. Cafea, câteva pagini din cartea nouă și **fără ecrane** până la zece.

### Dimineața
[Piața cu mama](lanruj:intrare/zi/2026-11-21/pi04) era plină de mere și dovleci. Mi-a povestit iar cum făcea bunica *plăcinta cu mere*: foi subțiri, multă scorțișoară și ==răbdare==.

- mere, nuci și miere
- un dovleac pentru supă
- flori pentru masa din bucătărie

### 16:40
Cafea cu Ana. Am vorbit despre excursia la Viena și despre cât de repede a trecut anul.

> Scrie-o, altfel n-a fost.

Diseară: bagajul, apoi citit până adorm.
"""),
    "bilete.md": ("""# Bilete

- Present idea for Andrei: a good chess set
- Ask mum for the pie recipe, on paper
""", """# Bilete

- Idee de cadou pentru Andrei: un șah bun
- Cere-i mamei rețeta de plăcintă, pe hârtie
"""),
}

for path, (en, ro) in T.items():
    write(path, ro if RO else en)
picture("2026/11/2026-11-21/" + ("apus.jpg" if RO else "sunset.jpg"), [(250, 196, 120), (237, 120, 90)], (255, 236, 170), [(120, 90, 110), (70, 55, 80)])

# Monitorizarea lunii: activități (bifate, numărate, cu timp), somn și serviciu, zilele 1-21.
rnd = random.Random(7)
if RO:
    acts = ["cafea", "citit", "flotări", "apă", "plank"]
    head, lst = "# Noiembrie 2026\n\n## Serviciu\n\n", "Listă: cafea, citit, flotări (număr), apă (pahare), plank (timp)"
    work = ["- 2 serviciu: predare la ora 8", "- 3 ore suplimentare 08:00-12:00: inventarul lunii", "- 6 rezervă", "- 10 serviciu",
            "- 14 serviciu", "- 15 ore suplimentare 18:00-21:00", "- 18 serviciu: tura de noapte la poartă", "- 23-27 concediu"]
    sleep_h, act_h, night, day = "## Somn", "## Activități", "noapte", "zi"
else:
    acts = ["coffee", "reading", "push-ups", "water", "plank"]
    head, lst = "# November 2026\n\n## Work\n\n", "List: coffee, reading, push-ups (number), water (glasses), plank (time)"
    work = ["- 2 duty: handover at 8", "- 3 overtime 08:00-12:00: monthly inventory", "- 6 standby", "- 10 duty",
            "- 14 duty", "- 15 overtime 18:00-21:00", "- 18 duty: night shift at the gate", "- 23-27 leave"]
    sleep_h, act_h, night, day = "## Sleep", "## Activities", "night", "day"
lines = [head + "\n".join(work) + "\n", sleep_h + "\n"]
for d in range(1, 22):
    n = rnd.choice([6, 6.5, 7, 7, 7.5, 8, 8.5])
    lines.append(f"- {d} {night} {int(n)}:{'30' if n % 1 else '00'}")
    if rnd.random() < 0.3:
        lines.append(f"- {d} {day} 0:{rnd.choice(['30', '45'])}")
lines.append("\n" + act_h + "\n\n" + lst + "\n")
for d in range(1, 22):
    parts = []
    if rnd.random() < 0.9:
        parts.append(acts[0])
    if rnd.random() < 0.7:
        parts.append(acts[1])
    if rnd.random() < 0.6:
        parts.append(f"{acts[2]} {rnd.choice([20, 25, 30, 40])}")
    parts.append(f"{acts[3]} {rnd.choice([4, 5, 6, 7, 8])}")
    if rnd.random() < 0.5:
        parts.append(f"{acts[4]} {rnd.choice(['1:00', '1:30', '2:00'])}")
    lines.append(f"- {d} " + ", ".join(parts))
write("monitorizare/2026-11.md", "\n".join(lines) + "\n")

# Setările: limba, hârtia cu puncte, fără migrarea de seară (capturile sunt făcute la orice oră).
write(".setari.ini", f"[lanruj]\nlimba={LANG}\nhartie=puncte\nmigrare-automata=false\n")
print("gata:", ROOT)
