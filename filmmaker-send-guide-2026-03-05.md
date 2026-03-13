# OEFF 2026 — Filmmaker Send Guide

March 5, 2026 · 12 films, 4 campaigns

**Merge sheet:** [OEFF 2026 Filmmaker Merge Sheet](https://docs.google.com/spreadsheets/d/1eFyEiENnjiOdy5eYAVwZUpWKvtfxhdZ2L-_YlWSSxFQ/edit)

**Outreach doc:** [OEFF 2026 — Filmmaker Outreach](https://docs.google.com/document/d/1CfXegKRMa73rbG1Kyv_kwBVK5HgmvLkRSd6DbA0VQBk/edit)

**HTML templates:** `/tmp/oeff-mailmeteor-templates/` (4 files, one per campaign)

---

## Setup

1. Open the merge sheet (link above)
2. Apply a filter: **Data → Create a filter** (if not already active)
3. For each campaign below:
   - Click the filter dropdown on the **Send Group** column (column I)
   - Uncheck all, then check only the group for that campaign
   - Open Mailmeteor: **Extensions → Mailmeteor → Mail merge**
   - Switch to **HTML mode** in the template editor (click the `<>` icon)
   - Paste the HTML template for that campaign
   - Set the subject line
   - Preview all emails, then send
   - Clear the filter before moving to the next campaign

**Important:** Mailmeteor sends only to visible rows. The filter controls who gets each template.

---

## Campaign 1 — Feature Single (4 films)

**Filter Send Group to:** `Feature-Single`

**HTML template:** `campaign-1-feature-single.html`

**Recipients:**

| Film | Email |
|------|-------|
| Jane Goodall: Reasons for Hope | john@cosmicpicture.com |
| Plastic People | ruth@whitepinepictures.com |
| Drowned Land | colleenthurston8@gmail.com |
| In Our Nature | james@synchronous.tv |

**Subject:**

    One Earth Film Festival 2026 — {{Film Title}} — screening confirmation + licensing

**Body preview:**

> Hi {{First Name}},
>
> Your film **{{Film Title}}** is confirmed for one screening at OEFF 2026:
>
> **{{Venue List}}**
>
> Could you let us know your **nonprofit screening license rate**? One Earth Film Festival is a 501(c)(3). Once licensing is set, we'll follow up with file delivery specs, AV details, and day-of logistics.
>
> Really looking forward to sharing this film with our audiences. Thank you for being part of the festival!

---

## Campaign 2 — Feature Multi (5 films)

**Filter Send Group to:** `Feature-Multi`

**HTML template:** `campaign-2-feature-multi.html`

**Recipients:**

| Film                | Email                         | Screenings |
| ------------------- | ----------------------------- | ---------- |
| Beyond Zero         | nathan@haveypro.com           | 2          |
| Rooted              | LWaring.Douglas@gmail.com     | 2          |
| How to Power a City | melanie.larosa@gmail.com      | 3          |
| Rails to Trails     | dan@protesscommunications.com | 2          |
| 40 Acres            | dmccarthy@magpictures.com     | 2          |

**Subject:**

    One Earth Film Festival 2026 — {{Film Title}} — screening confirmation + licensing

**Body preview:**

> Hi {{First Name}},
>
> Your film **{{Film Title}}** is confirmed for **{{Screening Count}} screenings** at OEFF 2026:
>
> **{{Venue List}}**
>
> Could you let us know your **nonprofit screening license rate for {{Screening Count}} screenings**? One Earth Film Festival is a 501(c)(3). If you're able to offer a multi-screening or festival rate, that would be amazing. Once licensing is set, we'll follow up with file delivery specs, AV details, and day-of logistics.
>
> Really looking forward to sharing this film with our audiences. Thank you for being part of the festival!

---

## Campaign 3 — Short Licensing (2 films)

**Filter Send Group to:** `Short-Licensing`

**HTML template:** `campaign-3-short-licensing.html`

**Recipients:**

| Film | Email | Screenings |
|------|-------|------------|
| Planetwalker | dominic@encompassfilms.com | 4 |
| That Which Once Was | kimi.newdaybiz@gmail.com | 1 |

**Subject:**

    One Earth Film Festival 2026 — {{Film Title}} — screening confirmation + licensing

**Body preview:**

> Hi {{First Name}},
>
> Your short film **{{Film Title}}** is confirmed for **{{Screening Count}} screening(s)** at OEFF 2026:
>
> **{{Venue List}}**
>
> Could you let us know your **nonprofit screening license rate**? One Earth Film Festival is a 501(c)(3). Once licensing is set, we'll follow up with file delivery specs and day-of logistics.
>
> Really looking forward to sharing this film with our audiences. Thank you for being part of the festival!

---

## Campaign 4 — Chasing Time (1 email, manual)

**Send manually from Gmail.** No Mailmeteor needed.

**HTML template:** `campaign-4-chasing-time.html` (paste into Gmail compose, or type manually)

**To:** sarah@exposurelabs.com

**Subject:**

    One Earth Film Festival 2026 — Chasing Time — screening confirmation + thank you

**Body preview:**

> Hi Sarah,
>
> Chasing Time is confirmed for **3 screenings** at OEFF 2026:
>
> **Park Ridge Community Church — April 24**
> **Chicago Climate Action Museum — April 24**
> **Euclid Ave UMC — April 24**
>
> Thank you so much for your team's generous offer to waive the screening fee — we really appreciate it. We'll follow up separately with file delivery specs, AV details, and day-of logistics.
>
> Really looking forward to sharing this film with our audiences. Thank you for being part of the festival!

---

## After sending

1. Go back to the merge sheet
2. Clear the filter (click the filter icon on Send Group → Select All)
3. Fill in today's date (2026-03-05) in the **Sent Date** column for all 12 films sent
4. Whose Water? stays blank — not sent (Hold)

## Follow-up tracking

- **Mailmeteor dashboard:** Check open rates and reply status for Campaigns 1-3
- **Automated follow-up:** Consider setting a follow-up in Mailmeteor for ~5 days if no reply
- **Merge sheet:** Track responses in the **Response Status** and **License Fee** columns as they come in

## Watch for

- **HTML mode:** Make sure you're in Mailmeteor's HTML editor (click `<>`) before pasting templates. If you paste into the rich text editor, the HTML tags will show as literal text.
- **{{Venue List}} line breaks:** If venues show as one long line, the newlines aren't rendering as `<br>` in the merge field. Let Garen (Claude) know to fix in the sheet data.
- **Replies:** Some filmmakers may reply to the thread, others may email separately. Check both.

---

*Not sent: Whose Water? (F26-010) — Hold, Ana + Josh rewatching for Epiphany fit.*
