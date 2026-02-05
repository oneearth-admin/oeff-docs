# OEFF 2026 Documentation

Internal team documentation for the One Earth Film Festival.

## Structure

```
oeff-docs/
├── index.html          # Landing page with nav
├── styles.css          # Shared design system
├── setup-guide.html    # Shared inbox setup (public)
├── team-guide.html     # How we work together (public)
└── team/               # Unlisted admin docs
    ├── admin-guide.html
    └── design-dna.html
```

## Deployment to Cloudflare Pages

### Initial setup (~10 min)

1. Create a GitHub repo named `oeff-docs`
2. Push this folder to the repo
3. Go to [Cloudflare Pages](https://dash.cloudflare.com/) → Create application → Pages
4. Connect to Git → Select the repo
5. Build settings: Leave blank (static HTML needs no build)
6. Deploy

### Custom domain (optional)

1. In Cloudflare DNS, add your domain
2. In Pages project → Custom domains → Add `docs.oneearthfilmfest.org`
3. Cloudflare handles SSL automatically

### Updating content

1. Edit HTML files locally
2. Commit and push to GitHub
3. Cloudflare auto-deploys (usually <1 min)

## Design System

The `styles.css` file contains OEFF's design tokens extracted from hosts.oneearthfilmfest.org:

- **Colors:** Sage-tinted neutrals, OEFF brand palette
- **Typography:** Avenir Next (display), Georgia (body)
- **Spacing:** 8px-based scale
- **Components:** Tables, blockquotes, navigation cards

## Unlisted vs Public

Files in `/team/` are not linked from the public navigation. Share URLs directly with team members who need them. This is information architecture, not security—anyone with the URL can access.

---

One Earth Film Festival · April 22–26, 2026
