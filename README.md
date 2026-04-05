# DevHeal Labs AI - Company Homepage

Official website for **DevHeal Labs AI** — Intelligent Developer Tools & AI-Native Infrastructure.

**Live:** [https://devheallabs.in](https://devheallabs.in)
**Repo:** [DevHealLabs/devheallabs.github.io](https://github.com/devheallabs-ai/devheallabs.github.io)

---

## What This Is

Single-page company homepage for DevHeal Labs AI, showcasing:

- **NC Language** — The AI programming language
- **HiveANT** — Autonomous incident response
- **SwarmOps** — Intelligent operations platform
- **NeuralEdge** — Financial intelligence engine

Built as a zero-dependency static site (pure HTML/CSS/JS, no frameworks).

## Project Structure

```
devheallabs-website/
  index.html        # Main homepage (served by GitHub Pages)
  404.html          # Custom 404 page
  CNAME             # Custom domain config (devheallabs.in)
  start.sh          # Local dev & deploy helper script
  favicon-note.txt  # Favicon requirements
  README.md         # This file
  website/          # Mirror copy of deployable assets
    index.html
    CNAME
```

## Preview Locally

```bash
# Quick start
./start.sh

# Or manually
python3 -m http.server 9000
```

Then open [http://localhost:9000](http://localhost:9000) in your browser.

## Deploy to GitHub Pages

This site is deployed via GitHub Pages from the `DevHealLabs/devheallabs.github.io` repository.

### Steps

1. Clone the deployment repo:
   ```bash
   git clone git@github.com:DevHealLabs/devheallabs.github.io.git
   ```

2. Copy the updated files:
   ```bash
   cp index.html 404.html CNAME ../devheallabs.github.io/
   ```

3. Commit and push:
   ```bash
   cd ../devheallabs.github.io
   git add -A
   git commit -m "Update website"
   git push origin main
   ```

4. GitHub Pages will automatically deploy within a few minutes.

### Custom Domain

The `CNAME` file contains `devheallabs.in`. DNS must have:
- An `A` record pointing to GitHub Pages IPs (185.199.108-111.153)
- Or a `CNAME` record pointing to `devheallabs.github.io`

## Update Content

All content lives in `index.html` as a self-contained single file:

- **Text/copy** — Edit the HTML directly
- **Colors** — Modify CSS variables in the `:root` block
- **Products** — Add/edit cards in the `#products` section
- **Links** — Update `href` attributes in nav, footer, and product cards

No build step required. Edit, save, deploy.

---

Built in Hyderabad, India.
