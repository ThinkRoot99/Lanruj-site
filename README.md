# Lanruj website

The website of [Lanruj](https://github.com/ThinkRoot99/Lanruj), a bullet journal app for Linux. It is a static site in English and Romanian, with no cookies, no tracking and no external services.

Lanruj and its website are built by Claude, the AI made by Anthropic, and tested by ThinkRoot.

## Layout

- English pages in the root: `index.html`, `docs.html`, `about.html`, `contact.html`, `privacy.html`.
- Romanian pages in `lang/ro/`: `index.html`, `documentatie.html`, `despre.html`, `contact.html`, `confidentialitate.html`.
- `assets/`: the stylesheet, the script (language choice and small effects) and the images, as WebP in several sizes.
- `tools/pagini.py`: generates the header, the footer and the inner pages, plus `sitemap.xml`, `robots.txt`, `404.html` and `.htaccess`. The home pages are written by hand; the script only refreshes their header, footer and download links.

## Updating

After changing a text in `tools/pagini.py`, or when a new version of Lanruj is released, set `VERSION` at the top of the script and run:

```
python3 tools/pagini.py
```

The download buttons then point to that version's packages on the GitHub releases page. The site address is `SITE_URL` in the same file.

## Licence

The code of this website (HTML, CSS, JavaScript and the tools) is free software, released under the GNU General Public License, version 3 or later (GPL-3.0-or-later). See [LICENSE](LICENSE).
