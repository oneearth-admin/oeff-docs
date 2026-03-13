# Email Template Quick Reference

**Owner:** Kim (sends) / Garen (template design)
**Tools:** Mailmeteor, hosts@ Gmail
**Audience:** Practitioner
**Reading context:** Desk-doing — look up a template before each send

---

## Active templates

### Stream 1: Webinar Cycle

| ID | Template | When | Subject line | Merge fields |
|----|----------|------|-------------|-------------|
| 03 | Webinar Preview | 7 days before webinar | Next Monday: {{Webinar Topic}} — OEFF Host Webinar Series | {{First Name}}, {{Webinar Topic}}, {{Webinar Date}}, {{Prep Notes}}, {{Agenda Bullets}} |
| 04 | Webinar Reminder | 1 day before webinar | Tomorrow at noon: {{Webinar Topic}} | {{First Name}}, {{Webinar Topic}}, {{Webinar Date}} |
| 05 | Webinar Recap | Day after webinar | Recording + recap: {{Webinar Topic}} | {{First Name}}, {{Webinar Topic}}, {{Webinar Date}}, {{Recording Link}}, {{Recap Bullets}}, {{Action Items}}, {{Next Webinar Topic}}, {{Next Webinar Date}} |

### Stream 2 & 3: Deliverables + Milestones

| ID | Template | When | Key merge fields |
|----|----------|------|-----------------|
| — | Film confirmation | ~Mar 9, as matching completes | {{Film Title}}, {{Screening Date}}, {{Film Synopsis}}, {{Trailer Link}} |
| — | Marketing kit ready | ~Mar 23 | {{Film Title}}, {{Venue Name}} |
| — | Screening packet | ~Apr 1 | {{Film Title}}, {{Download Link}}, {{Financial Password}} |
| — | Slides + trailers | ~Apr 15 | {{Film Title}}, {{Slides Link}}, {{Screening Date}} |
| — | One week out | ~Apr 15 | {{Film Title}}, {{Screening Date}}, {{Venue Name}} |
| — | Eve of festival | ~Apr 21 | {{First Name}} |
| — | Thank you + debrief | ~Apr 29 | {{First Name}}, {{Venue Name}}, {{Survey Link}} |

### Other

| ID | Template | When | Key merge fields |
|----|----------|------|-----------------|
| 01 | Host Helper URL | When sharing host-specific page links | {{Venue Name}}, {{Host Helper URL}} |
| 02 | Financial/Password | Companion to template 01 | {{Venue Name}}, {{Financial Password}}, {{Host Helper URL}} |
| 06 | Calendar invite description | One-time, recurring series | N/A (manual) |
| — | Cool host conversion | When converting uncommitted venues | {{First Name}}, {{Venue Name}} |

---

## How to use a template

1. Open Mailmeteor in hosts@ Gmail
2. Select the template by name
3. Swap in the per-webinar or per-event content block (templates 03 and 05 have these — look under "Per-Webinar Content Blocks" in the template file)
4. Verify merge fields populated from the connected Google Sheet
5. **Always send a test to yourself first** — check links, merge fields, formatting
6. Schedule or send to the appropriate list

---

## Template files location

All markdown source files live in: `email-drafts/` (shared Google Drive)

```
email-drafts/
├── 01-host-helper-url.md
├── 02-financial-password.md
├── 03-webinar-preview.md      ← has per-webinar content blocks
├── 04-webinar-reminder.md
├── 05-webinar-recap.md        ← has per-webinar recap blocks
└── 06-calendar-invite-description.md
```

Stream 2/3 templates (film confirmation, screening packet, one week out, eve of festival, thank you) are to be drafted as the timeline approaches. Use Claude to generate first drafts, then refine.

---

## Merge field source

All merge fields pull from the V7 Google Sheet. Mailmeteor reads directly from the sheet connected to your campaign.

| Field | Column in V7 Sheet |
|-------|-------------------|
| {{First Name}} | First Name |
| {{Email}} | Email |
| {{Venue Name}} | Venue |
| {{Film Title}} | Film Title |
| {{Screening Date}} | Screening Date |
| {{Host Helper URL}} | Host Helper URL |
| {{Financial Password}} | Financial Password |
| {{Download Link}} | Download Link |

Other fields ({{Webinar Topic}}, {{Recap Bullets}}, etc.) are swapped manually per-send — they're not column-driven.

---

## Send checklist (every time)

1. Correct template selected
2. Content block swapped for this specific send
3. Merge fields verified in preview
4. Test email sent to yourself
5. Links tested (especially download links and Zoom registration)
6. Sent to the correct list (warm hosts? cool hosts? all?)
7. V7 Sheet tracking columns updated after send

---

## Tone notes

- Sign off as "The One Earth Film Festival Team" — not individual names
- Send from hosts@oneearthcollective.org
- Partnership frame: hosts are doing something for their community, not attending our event
- No "just checking in" — every email has a purpose
- "No worries" when a host can't attend something — reduce guilt, keep them in the loop
