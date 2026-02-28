# Filmmaker Comms: State of Play

**Date:** 2026-02-28
**Author:** Garen
**Audience:** Garen, Ana, Josh
**Next action deadline:** Monday 3/2 (filmmaker outreach send)

---

## The Big Picture

We have 12 films in the 2026 lineup. Filmmakers need to hear from us with one clear, consolidated ask. Right now there are multiple threads — survey completion, licensing negotiation, AV tech specs, marketing assets — and they're spread across different tools and conversations. This document maps the current state and proposes a path to a single unified outreach.

---

## Per-Film Status Matrix

| Film | Contact | Intake Done? | Screenings | Licensing Need | Status |
|------|---------|:---:|:---:|------|--------|
| **Jane Goodall: Reasons for Hope** | John Wickstrom (Cosmic Picture) | Yes | 1 | Single license | Confirmed |
| **Plastic People** | Ruth Pindilli (White Pine) | Yes | 1 | Single license | Confirmed |
| **Beyond Zero** | **NO CONTACT** | **No** | 1 | Single license | Confirmed — but no contact on file |
| **Drowned Land** | Colleen Thurston | Yes | 1 | Single license | Pending |
| **Rooted** | Lauren Waring Douglas | Yes | 2 | **Multi-license (nonprofit rate)** | Confirmed |
| **How to Power a City** | Melanie La Rosa | Yes | 3 | **Multi-license (nonprofit rate)** | Mixed (1 confirmed, 2 pending) |
| **Oscar Shorts** | Darwin Shaw | Yes | 0 | TBD — no venue assigned yet | — |
| **40 Acres** | **NO CONTACT** | **No** | 2 | **Multi-license (nonprofit rate)** | Pending — and no contact on file |
| **CAM Awards** | **NO CONTACT** | **No** | 0 | Partnership (non-standard) | — |
| **Whose Water?** | Kate Levy | Yes | 0 | TBD — no venue assigned yet | — |
| **Rails to Trails** | Dan Protess | Yes | 1 | Single license | Confirmed |
| **In Our Nature** | James Parker (Synchronous) | Yes | 0 | TBD — no venue assigned yet | — |

### Key Takeaways

- **9/12 films** have submitted the Film Intake Survey. The 3 missing: Beyond Zero, 40 Acres, CAM Awards.
- **3 films** need multi-screening license negotiations (Rooted ×2, How to Power a City ×3, 40 Acres ×2).
- **3 films** have NO CONTACT on file — Beyond Zero, 40 Acres, CAM Awards. These need to be sourced before outreach.
- **4 films** have 0 screenings assigned — Oscar Shorts, CAM Awards, Whose Water?, In Our Nature. Venue assignments may be pending or these may have a different pipeline (e.g., CAM is a partnership, not a traditional screening).

---

## The Two Surveys Problem

### What exists

**Film Intake Survey (new, 2026)**
- ~25 questions, streamlined from the 2025 version (37 questions)
- Sections: Contact, Marketing/Promo, Attendance, Licensing, Accessibility, Delivery
- 9 of 12 filmmakers have submitted (Jan 26–Feb 5 window)
- Google Form ID: `1FAIpQLSflchFav...` (live URL exists but not wired into any local tooling)

**Original Film Survey (legacy)**
- 37 questions, used in prior years
- Included marketing commitments, Q&A availability, social handles
- Ana's concern: the new survey may have dropped some of these fields

### What's actually missing from the new survey

The new 2026 design spec (documented in `OEFF-2026-Form-Designs-Industry-Aligned.html`) actually **does include** marketing, attendance, and licensing sections. The streamlining was about reducing redundancy and simplifying accessibility questions — not removing categories.

**However**, the data that came back from the 9 submissions only populated contact + AV fields in Airtable. The richer fields (licensing terms, attendance, social handles, premiere status) are either:
- Still in the raw Google Sheets response data (not synced to local files)
- In Notes columns
- Not captured at all (if those sections weren't active when the form went out in January)

### Recommendation

**Don't create a third survey.** Instead:
1. Confirm what sections are live on the current form (check the actual Google Form)
2. If marketing/attendance/licensing sections are already there → the 9 respondents may have already answered them (check the Google Sheet)
3. If those sections were added after the January send → the 3 non-respondents will get the full version, but the 9 who already responded will need a targeted follow-up for just the missing sections

---

## The Monday Outreach: What It Needs to Accomplish

One email per filmmaker. Each is custom because screening counts/venues vary. The email needs to:

1. **Confirm screenings** — "Your film [title] is scheduled for [N] screenings at [venues] on [dates]"
2. **Request licensing terms** — "Please reply with your per-screening nonprofit rate for [N] screenings to audiences of up to 100"
3. **Survey completion** — For the 3 who haven't submitted: link to the Film Intake Survey
4. **Survey supplement** — For the 9 who already submitted: if marketing/attendance fields weren't captured, a targeted ask for just those fields
5. **Deadline** — "Please respond by 03/07/2026" (one week, gives buffer before early-access tickets)

### Sending logistics

- **From:** `films@oneearthcollective.org`
- **Method:** Mail merge (Garen building, will show Josh the process)
- **CC/BCC:** Ana + Garen on all threads
- **Template:** One master template with merge fields for: filmmaker name, film title, screening count, venue names, dates, licensing tier (single vs. multi)

---

## Airtable Integration: What Needs Linking

The screenshots show Airtable records that need connecting. The pipeline:

```
Film Survey (Google Form)
    |
    v
Google Sheets: Film_Survey_Responses
    |
    v (manual export or Apps Script)
Airtable:
    Films table ← film metadata
    Film Contacts table ← filmmaker identity + AV specs
    Events table ← licensing fields (currently 0/31 populated)
```

### Fields that exist in schema but are empty for 2026

| Table | Field | Status |
|-------|-------|--------|
| Events | Licensing Request Status | 0/31 populated |
| Events | License Status | 0/31 populated |
| Events | Film License Amount | 0/31 populated |
| Events | Film Licensing Contact | 0/31 populated |
| Events | License Invoice Received | 0/31 populated |
| Events | License Invoice Paid | 0/31 populated |
| Films | Trailer Link | 0/12 populated |
| Films | Runtime (in schema, not exported) | Unknown |
| Films | Filmmaker Names (in schema, not exported) | Unknown |

### What needs to happen

1. **After Monday's outreach gets responses** → populate Events licensing fields per screening
2. **Survey response sync** → pull the rich fields from Google Sheets into Airtable (marketing, attendance, social handles)
3. **Missing contacts** → source contacts for Beyond Zero, 40 Acres, CAM Awards before send

---

## Open Questions

1. **Which survey link goes in the Monday email?** Need to verify the live form has all sections active.
2. **Beyond Zero, 40 Acres, CAM contacts** — who has these? Josh? Ana? Need to source before Monday.
3. **CAM Awards** — is this a standard film or a partnership? Different outreach tone?
4. **Oscar Shorts, Whose Water?, In Our Nature** — are venue assignments coming, or are these in a different pipeline?
5. **Dominican University film swap** — squad meeting mentioned possible swap from Rooted to Food 2050. Is that decided? Changes the licensing ask.

---

## Timeline

| Date | Action | Owner |
|------|--------|-------|
| **Fri 2/28** | Finalize this status doc, resolve open questions | Garen |
| **Sat 3/1** | Build mail merge template + test send | Garen |
| **Mon 3/2** | Send filmmaker outreach from films@ | Garen |
| **Mon 3/2** | Show Josh the mail merge process | Garen + Josh |
| **Fri 3/7** | Response deadline for filmmakers | Filmmakers |
| **Week of 3/2** | Early-access tickets go live (once licensing handshakes in) | Ana |
| **Thu 3/13** | Hard deadline for Film Survey completion | Filmmakers |
