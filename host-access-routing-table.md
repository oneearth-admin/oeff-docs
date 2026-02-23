# OEFF Host Access Routing Table

**Prepared:** 2026-02-23
**Companion to:** `host-portal-security-recommendation.md`
**Status:** Reference document — nothing built

---

## What Lives Where

Every piece of host-facing information falls into one of three access tiers. The tier determines how a host reaches it and how it gets delivered.

### Tier 1: Public (no gate)

Anyone can see this. Indexed by search engines. Linked from the OEFF website.

| Content | Where it lives | How hosts find it |
|---------|---------------|-------------------|
| Venue name, film title, date | `hosts/index.html` (venue sections) | Link from OEFF website, shared in emails |
| Event description and region | `hosts/index.html` | Same |
| RSVP/event page link | `hosts/index.html` | Same |
| Marketing assets (poster, social kit) | `hosts/index.html` (mar state) | Same |
| "Your Focus" callout per venue | `hosts/index.html` (all states) | Same |
| General orientation info | `hosts/index.html` | Same |

**Privacy enforcement:** The automated build-time check (privacy lint) blocks phone numbers, Dropbox URLs, and screening packet links from appearing in any public page. If any slip through, the build fails.

### Tier 2: Token-gated (unguessable link)

Only accessible via a unique URL like `hosts/a3f9x7k2/`. Not indexed by search engines (`noindex` meta tag + `robots.txt` exclusion). A host needs the link to see the page — there's no way to browse to it.

| Content | Where it lives | How hosts find it |
|---------|---------------|-------------------|
| Host helper one-pager | `hosts/[token]/index.html` | YAMM email with personalized link |
| Contact emails (co-host, AV, facility) | Host helper page | Same |
| Day-of timeline (computed) | Host helper page | Same |
| RSVP count snapshot | Host helper page | Same |
| Screening packet link (Apr only) | Host helper page | Same |
| "Update your info" form link | Host helper page | Same |
| "Something wrong?" mailto | Host helper page | Same |

**Who can see it:** Anyone with the link. If a host forwards it, the recipient can view the page. This is acceptable for contact info — it's not public, but it's not locked.

### Tier 3: Password-gated (token + password)

Requires both the unique URL and a separate password. The password is delivered in a different email than the token link, so compromising one doesn't compromise both.

| Content | Where it lives | How hosts find it |
|---------|---------------|-------------------|
| Scholarship status | Password-gated section of host helper | Token link (YAMM) + password (separate YAMM) |
| Scholarship amount | Same | Same |
| Any future financial info | Same | Same |

**Who can see it:** Only someone who has both the link and the password. This is the strongest protection tier in our static stack.

---

## How Hosts Get Access

The delivery mechanism is YAMM (Yet Another Mail Merge) — the bulk personalized email tool OEFF already uses. Each host receives their access credentials through the existing email cadence, not through a separate channel.

### Delivery Timeline

| Email wave | When | What's included | YAMM merge fields |
|-----------|------|-----------------|-------------------|
| **Confirmation email** | When host is confirmed (Phase 3) | Welcome, expectations, general host guide link | `{{venue_name}}`, `{{film_title}}`, `{{event_date}}` |
| **"Your host page is ready"** | March prep wave (~Mar 10) | Token link to their host helper page | `{{host_helper_url}}` (the full token URL) |
| **Screening packet delivery** | ~3 weeks before event (Phase 4) | Packet download link + password | `{{packet_password}}` |
| **Scholarship notification** | If applicable, separate from packet | Password for financial section | `{{financial_password}}` (different from packet password) |
| **Day-before reminder** | Day before screening | Reminder with host helper link again | `{{host_helper_url}}` (repeat for convenience) |

### Key Design Choice: Two Emails, Not One

The token link and any passwords are delivered in **separate emails**. This is intentional:

- If a host forwards their "your host page is ready" email to a co-host, the co-host can see the helper page (Tier 2) but not the financial section (Tier 3) because they don't have the password.
- If someone somehow gets the password email alone, they can't use it without the token URL.
- This mirrors how the old Host Helper worked — the spreadsheet link came in one email, and confidential file passwords came in another.

### What Hosts Actually Experience

A host named Maria at Pilsen Community Center:

1. **March 10:** Maria gets an email: "Your host page for OEFF 2026 is ready." She clicks the link → sees her helper page with tonight's timeline, contacts, event page link.
2. **March 20:** Maria's AV contact changes. She clicks "Update your info" on her helper page → pre-filled Google Form opens → she edits the AV contact field → submits. OEFF team reviews and merges.
3. **April 5:** Maria gets a separate email: "Your screening packet is ready." Includes a password. She goes to her helper page (bookmarked or re-clicks from the March email), enters the password → sees the packet download link.
4. **April 23, 6:45 PM:** Maria pulls up her helper page on her phone while setting up chairs. Timeline, contacts, packet link — all one tap away.

---

## How It Connects to Existing Systems

### Data Flow: Source to Screen

```
V7 Google Sheets (master)
    |
    v
Airtable (2026_Venue_Sections view, pre-joined)
    |
    v
Token mapping file (venue_name → token, generated once)
    |
    v
generate-venue-sections.py
    |
    +--→ hosts/index.html (public venue sections, Tier 1)
    |
    +--→ hosts/[token]/index.html (per-venue helper, Tier 2)
    |         |
    |         +--→ [password-gated section] (financial, Tier 3)
    |
    v
Cloudflare Pages (deployed)
```

### Data Flow: Host Updates Back to Source

```
Host clicks "Update your info" on helper page
    |
    v
Pre-filled Google Form (one per venue, URL generated by script)
    |
    v
"Host Updates" tab in V7 Google Sheets
    |
    v
OEFF team reviews weekly (March-April)
    |
    v
Team merges approved changes into canonical Hosts/Events tabs
    |
    v
Next Airtable sync picks up changes
    |
    v
Next generator run updates the helper page
```

### YAMM Integration

YAMM reads from a Google Sheet where each row = one host. The new merge fields slot into the existing YAMM workflow:

| Merge field | Source | Generated by |
|-------------|--------|-------------|
| `{{venue_name}}` | V7 Hosts tab | Already exists |
| `{{film_title}}` | V7 Events_2026 tab | Already exists |
| `{{event_date}}` | V7 Events_2026 tab | Already exists |
| `{{host_helper_url}}` | Token mapping file | New: token generation script |
| `{{update_form_url}}` | Form URL mapping file | New: form URL generation script |
| `{{packet_password}}` | Password mapping file | New: password generation script |
| `{{financial_password}}` | Password mapping file | New: password generation script (separate from packet) |

**New YAMM columns needed:** 4 new columns in the YAMM source sheet. Each is populated by a one-time script run, not manual entry.

### What's Already Built vs. What's New

| Component | Status | Effort |
|-----------|--------|--------|
| Public venue sections (`hosts/index.html`) | Built, deployed | -- |
| Privacy lint (build-time check) | Built, enforced | -- |
| YAMM email templates | Exist, need new merge fields | Small: add 4 columns |
| Token generation script | **New** | Small: ~30 lines Python stdlib |
| Host helper HTML template | **New** | Medium: one new template in generator |
| Generator `--helper` flag | **New** | Small: extension of existing script |
| Password gate JS | **New** | Small: ~20 lines vanilla JS |
| Password generation script | **New** | Small: ~20 lines Python stdlib |
| Pre-filled form URL generator | **New** | Small: ~40 lines Python stdlib |
| Google Form for host updates | **New** | Small: one form, manual creation |
| "Host Updates" sheet in V7 | **New** | Small: one new tab |
| `robots.txt` + `noindex` for token paths | **New** | Small: 2 lines |

---

## Search Engine Protection

Token-gated pages should not appear in search results. Two layers enforce this:

1. **`robots.txt`** on Cloudflare Pages: `Disallow: /hosts/*/` blocks crawlers from token paths
2. **`<meta name="robots" content="noindex, nofollow">`** in every token-gated page as a backup

The public `hosts/index.html` remains indexable — that's the point. Only the per-venue helpers are hidden.

---

## Edge Cases

| Situation | What happens |
|-----------|-------------|
| Host loses their link | They reply to any OEFF email asking for it. Team re-sends the YAMM email or forwards the link manually. |
| Host loses their password | Team re-sends the password email. Password doesn't change — it's stable per venue. |
| Host forwards their link to a volunteer | Volunteer can see the helper page (Tier 2). Cannot see financial info (Tier 3) without the password. This is by design. |
| Host contact changes mid-season | New contact emails OEFF or uses the update form. Team updates V7, re-runs generator, re-sends token link to new contact. |
| Co-host needs access | Primary host forwards the token link. Co-host sees Tier 2 content. If co-host needs Tier 3, team sends them the password directly. |
| Token URL is guessed | Tokens are 11 characters from a 64-character alphabet. That's ~70 bits of entropy. Brute-forcing is not realistic. |
| Someone views page source to bypass password gate | They see the hashed password, not the plaintext. They could extract the hidden HTML, but this requires technical knowledge well beyond the threat model. |

---

*Reference document -- Session sw-20260223-e61f -- February 23, 2026*
