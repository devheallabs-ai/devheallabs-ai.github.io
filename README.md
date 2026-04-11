# DevHeal Labs AI Website

Public company website for DevHeal Labs AI.

Live site: https://devheallabs.in

## What is here

- `index.html` — homepage
- `404.html` — custom not-found page
- `CNAME` — domain config
- `start.bat` / `start.sh` — local preview helpers
- `website/` — deployable mirror of the public assets

## Preview locally

Windows:

```bat
start.bat
```

macOS / Linux:

```bash
./start.sh
```

Then open http://localhost:9000

## Update content

- Edit text directly in `index.html`
- Update product cards in the products section
- Adjust colors in the `:root` CSS variables
- Keep `website/` in sync with the public files when needed
