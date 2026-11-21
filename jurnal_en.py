#!/usr/bin/env python3
"""Un jurnal de probă în engleză, pentru capturile de pe site (fără nimic personal).
Folosire: python3 site/jurnal_en.py <dosar>"""
import os
import sys

from PIL import Image, ImageDraw

ROOT = sys.argv[1]


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


write("2026/11/2026-11-19.md", """# Thursday, 19 November 2026

- o 10:00 Project presentation
- [x] * Send the slides to the team
- [x] Book the train tickets to Vienna
- [>] Fix the kitchen shelf ^sh01
- Rain all day, <span style="color:#1c71d8">a good day for reading</span>
- [x] Call grandma

Tags: work, family
Day: 4/5
""")
write("2026/11/2026-11-20.md", """# Friday, 20 November 2026

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
""")
write("2026/11/2026-11-21.md", """# Saturday, 21 November 2026

- o 11:00 Farmers' market with mum
- [ ] Wash the car
- [ ] ! Try grandma's ==apple pie recipe==
- [ ] Fix the kitchen shelf ^sh01
- Trip notes: [opening hours](https://example.org/museum)
- o 16:00 Coffee with Ana
  ![Sunset on the hill|220](2026-11-21/sunset.jpg)
- [ ] Pack for Vienna

Tags: home
""")
picture("2026/11/2026-11-21/sunset.jpg", [(250, 196, 120), (237, 120, 90)], (255, 236, 170), [(120, 90, 110), (70, 55, 80)])
picture("2026/11/2026-11-21/morning.jpg", [(170, 215, 245), (225, 240, 250)], (255, 250, 220), [(110, 170, 110), (70, 130, 80)])

write("2026/11/luna.md", """# November 2026

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
""")
write("2026/12/luna.md", """# December 2026

## Calendar

- 6 St Nicholas
- 24 Christmas Eve with the parents
- 31 18:00 New Year's Eve with friends

## Tasks

- [ ] Buy the Christmas presents
- [ ] * Make next year's budget
""")
write("2026/saptamani/2026-S47.md", """# Week 47, 16-22 November 2026

- [ ] Fix the kitchen shelf ^sh01
- [x] * Finish the project presentation
- [ ] Read two chapters a day
- [ ] Gym three times
  - Monday and Wednesday done, Friday left
""")
write("2026/saptamani/2026-S48.md", """# Week 48, 23-29 November 2026

- [ ] Get the house ready for winter
- [ ] ! Start the present list
""")
write("viitor.md", """# Plans

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
""")
write("pagini/2026-11-23.md", """# Trip to Vienna

- o 23 November 07:40 Train from the central station
- [ ] Book the Belvedere tickets
- [x] Hotel near the Naschmarkt
- Café list: Central, Sperl, Hawelka
""")
write("index.md", """# Index

- [Trip to Vienna](pagini/2026-11-23.md): [23-27 November 2026](2026/11/2026-11-23.md)
- [Project presentation](2026/11/2026-11-19.md): 19 November 2026
""")
print("gata:", ROOT)
