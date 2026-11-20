# Swift Recovery Service — website

Static, mobile-first site for Swift Recovery Service (Liverpool). No framework, no build tooling beyond one Python script.

- `index.html` — the whole site (CSS and JS inline for speed)
- `assets/img/` — web-sized JPEG + WebP copies of the real job photos, plus `og.jpg` (social share image)
- `swift-recovery-demo-photos/` — original photos (source for the build)
- `tools/build.py` — regenerates `assets/img/` and checks links/files
- `design-preview.html` — the approved Stage 1 design mockup

## Build

```bash
pip install pillow
python3 tools/build.py
```

## Deploy

Upload `index.html`, `favicon.svg`, `robots.txt` and `assets/` to any static host (Netlify, Vercel, GitHub Pages, cPanel).

Once the domain is known, make the `og:image` / `twitter:image` URLs absolute (e.g. `https://yourdomain.co.uk/assets/img/og.jpg`) and add `<link rel="canonical">` and `og:url`, so link previews work on WhatsApp and Facebook.
