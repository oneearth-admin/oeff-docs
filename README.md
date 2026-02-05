# OEFF 2026 Documentation

Internal team documentation for the One Earth Film Festival.

## Structure

```
oeff-docs/
├── index.html              # Multi-gate landing
├── styles.css              # Shared design system (v4.1)
├── setup-guide.html        # Shared inbox setup
├── team-guide.html         # Communication norms
└── team/                   # Unlisted support & admin docs
    ├── admin-guide.html        # Google Groups admin setup
    ├── auto-reply.html         # Domain email auto-reply config
    ├── design-dna.html         # Visual patterns reference
    ├── escalation.html         # 🟢🟡🔴 escalation triggers
    ├── support-onboarding.html # Day 1 checklist for support person
    ├── support-system.html     # 4-layer support system overview
    └── templates.html          # Copy-paste email templates (H1-H6, F1-F4, V1-V4, I1-I3)
```

## Gate Flow (v4.1)

```
Gate 1: New vs Returning
         │
         ▼
Gate 2: Relationship Type
         ├── Seasonal Support ──────┐
         ├── Project Contractor ────┤
         ├── Area Coordinator ──────┼──► Coordinator Onboarding
         └── Leadership ────────────┼──► Admin Docs
                                    │
                                    ▼
Gate 3a: Area Selection (Seasonal + Contractor)
         ├── Hosts / Venues
         ├── Films / Content
         ├── Programs
         └── Tech / AV
                │
                ▼ (Seasonal only)
Gate 3b: Role Selection
         ├── Email Support
         ├── Event Support
         └── General Support
                │
                ▼
    Area-specific Resources + Role Onboarding
```

**New team member:**
1. Land on index → "I'm new"
2. Select relationship (Seasonal / Contractor / Coordinator / Leadership)
3. Select area (Hosts, Films, Programs, Tech)
4. Select role if seasonal (Email / Event / General support)
5. See role-specific onboarding + area resources

**Returning visitor:**
1. Land on index → "I know what I need"
2. Quick reference with pill navigation (Guides / Cheat Sheet / FAQ)
3. LocalStorage remembers returning visitors

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
