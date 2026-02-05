# OEFF Knowledge Base: What This Is & How It Works

## ELI5

You have a folder of HTML files on your computer. When you push them to GitHub, Cloudflare automatically publishes them as a website. Edit locally → push → live in 30 seconds.

---

## What We Built

A static documentation site for OEFF team resources:

| URL | Content | Audience |
|-----|---------|----------|
| `docs.oneearthfilmfest.org/` | Landing page with navigation | Team |
| `.../setup-guide.html` | How to use shared inboxes | Team |
| `.../team-guide.html` | Communication norms | Team |
| `.../team/admin-guide.html` | Google Groups admin setup | Unlisted (admin only) |
| `.../team/design-dna.html` | Design system reference | Unlisted (internal) |

**Unlisted = not linked in navigation, but accessible if you have the URL.** Not security, just information architecture.

---

## Architecture

```
Your computer          GitHub              Cloudflare Pages
┌─────────────┐       ┌─────────────┐      ┌─────────────┐
│ oeff-docs/  │ push  │ oeff-docs   │ auto │ docs.oeff...│
│ (HTML+CSS)  │ ───►  │ repo        │ ───► │ (live site) │
└─────────────┘       └─────────────┘      └─────────────┘
```

- **GitHub** = version control, stores your files
- **Cloudflare Pages** = free hosting, watches GitHub, auto-deploys on push
- **No build step** = pure HTML/CSS, no frameworks, no complexity

---

## File Structure

```
oeff-docs/
├── index.html          ← Landing page
├── styles.css          ← Shared design system (edit once, applies everywhere)
├── setup-guide.html    ← Public doc
├── team-guide.html     ← Public doc
├── README.md           ← Deployment instructions
└── team/               ← Unlisted section
    ├── admin-guide.html
    └── design-dna.html
```

---

## How to Update Content

```bash
cd /Users/garen/Downloads/oeff-docs   # or wherever you moved it
# edit any .html file
git add .
git commit -m "Describe what you changed"
git push
```

Live in ~30 seconds. Check Cloudflare dashboard → Deployments to confirm.

---

## How to Add a New Page

1. Create `new-page.html` in the appropriate folder
2. Start with this template:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page Title — OEFF 2026</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>

<header>
  <h1>Page Title</h1>
  <p class="subtitle">Brief description</p>
</header>

<!-- Your content here -->

<footer>
  OEFF 2026 · <a href="index.html">Back to docs</a>
</footer>

</body>
</html>
```

3. If it should be linked publicly, add it to `index.html` navigation
4. If it should be unlisted, put it in `team/` and share URL directly
5. Push to GitHub

---

## Design System Basics

The `styles.css` file handles all visual styling. Key elements:

- **Headers:** `<h1>`, `<h2>`, `<h3>` — automatically styled
- **Body text:** Just write `<p>` tags
- **Lists:** Standard `<ul>`, `<ol>`, `<li>`
- **Tables:** Standard `<table>` with `<th>` for headers
- **Callouts:** Use `<blockquote>` for highlighted quotes/tips
- **Code:** Use `<code>` for inline technical terms

Colors are sage-tinted (OEFF brand), typography is Avenir/Georgia. You don't need to think about it—just write semantic HTML and it looks right.

---

## Custom Domain Setup

1. Cloudflare Pages dashboard → your project → **Custom domains**
2. Click **Set up a custom domain**
3. Enter: `docs.oneearthfilmfest.org`
4. Cloudflare auto-configures DNS + SSL

Requires OEFF's domain to be managed in Cloudflare (which it likely is if you're using Cloudflare Pages).

---

## Troubleshooting

**Deploy failed?**
- Check Cloudflare dashboard → Deployments → click failed deploy → read error
- Usually a syntax error in HTML

**Changes not showing?**
- Did you `git push`? Check with `git status`
- Check Cloudflare dashboard to confirm deployment completed
- Hard refresh browser (Cmd+Shift+R)

**Need to undo a change?**
```bash
git log --oneline          # find the commit hash you want
git revert <hash>          # creates a new commit that undoes it
git push
```

---

## For Future Claude Sessions

**Context to provide:**
> OEFF has a static docs site deployed via GitHub → Cloudflare Pages. Repo is `oeff-docs`, live at `docs.oneearthfilmfest.org`. Design system in `styles.css` uses OEFF brand (sage-tinted, Avenir/Georgia). To add content: create HTML file, link stylesheet, push to GitHub.

**Files Claude should know about:**
- `styles.css` — design tokens, don't recreate
- `team/` folder — unlisted internal docs
- This summary doc — architecture and workflow

---

## Why This Approach?

| Alternative | Tradeoff |
|-------------|----------|
| Google Docs | Can't control design, copy-paste drift, not a "real" website |
| WordPress | Overkill, requires maintenance, hosting costs |
| Notion | Limited design control, Notion branding |
| Static site generators (11ty, Hugo) | Adds build complexity for ~10 pages |

Plain HTML + Cloudflare Pages = maximum control, zero maintenance, free hosting, version history, professional URLs.

---

*Created Feb 4, 2026 · OEFF 2026 Technical Coordination*
