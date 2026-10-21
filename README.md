# erayulusoy.com

Source of [erayulusoy.com](https://erayulusoy.com): the website of Eray Ulusoy, web designer and software engineer offering corporate websites, business applications and cloud services.

The site is a fast static site in English (`/`) and Turkish (`/tr/`). Visitors whose browser language is Turkish are sent to the Turkish page automatically; everyone can switch with the EN / TR toggle.

## Structure

| Path | What it is |
| --- | --- |
| `src/template.html` | Page template shared by both languages |
| `src/build.py` | All page text (English and Turkish), SEO data and the build script |
| `src/assets/` | Styles, scripts, self-hosted fonts and the portrait |
| `src/_headers` | Security headers (CSP, HSTS and others) applied by Cloudflare |
| `src/robots.txt`, `src/sitemap.xml` | Search engine files |
| `src/security.txt` | Published at `/.well-known/security.txt` |
| `dist/` | The built site, ready to deploy. Do not edit by hand. |

## Editing text

1. Change the wording in `src/build.py` (the `EN.update(...)` and `TR.update(...)` blocks hold the current copy).
2. Rebuild:

   ```bash
   python3 src/build.py
   ```

3. Deploy the `dist/` folder.

## Deploying

The site runs on Cloudflare Workers static assets (project `ancient-silence-129c`, domains `erayulusoy.com` and `www.erayulusoy.com`).

Dashboard: **Workers & Pages → ancient-silence-129c → New deployment**, then drag the `dist/` folder.

## Contact form

The form is ready for [Formspree](https://formspree.io). Put the form ID in `FORMSPREE_ID` in `src/assets/main.js`, rebuild and deploy. Until then the form asks visitors to email contact@erayulusoy.com.
