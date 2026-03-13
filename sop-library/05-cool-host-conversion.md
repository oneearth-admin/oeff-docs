# Cool Host Conversion — Stream 5

**Owner:** Kim
**Backup:** Garen
**Tools:** Mailmeteor, Google Forms, Google Sheets (cool host tab), hosts@ Gmail
**Audience:** Practitioner
**Reading context:** Desk-doing — run this pipeline whenever there are uncommitted venues

---

## What this is

"Cool hosts" are venues that expressed interest in hosting a screening but haven't committed or selected a film. This pipeline converts them from interested to committed. Once a cool host selects a film and confirms, they move to the warm host sheet and enter the regular communication streams (Streams 1-4).

---

## The pipeline

```
Cool host list (Google Sheet, separate tab)
  → Conversion email (Mailmeteor — one ask: fill out the form)
  → Film selection form (Google Form)
  → Host responds → move to warm host sheet
  → Host enters regular streams
```

---

## Step by step

### 1. Confirm cool host list exists — before first send

**What to do:**
1. Open V7 Google Sheet
2. Find or create the cool host tab with columns: Name, Email, Venue, Status (Contacted / Form Sent / Responded / Converted), Date Last Contacted, Notes
3. Verify data is current — Garen or Operations may have the latest list

**Decision rights:** You can create the tab. If you're not sure who's on the cool host list, ask Garen.

---

### 2. Build the film selection form — before first conversion email

**What to do:**
1. Create a Google Form:
   - Your name + venue name
   - Link to film list PDF in the form description (view trailers, read synopses)
   - Top 1-2 film choices (text field — they type the title)
   - "Do you need to see the full film before deciding?" (Y / N)
   - Preferred screening date (text field or date picker)
   - Any questions? (open text)
2. Test the form — make sure the film list PDF link works
3. Note: this form exists to reduce friction. One link, one action.

**Decision rights:** You own form design. Film list PDF comes from Executive Director or Operations.

---

### 3. Send conversion email — as soon as form is ready

**Template:** Cool host conversion email (to be drafted)
**Merge fields:** {{First Name}}, {{Venue Name}}

**What to do:**
1. Draft in Mailmeteor. Keep it short and clear:
   - Acknowledge the gap: "We know it's been a few weeks since we last connected"
   - One ask: fill out the film selection form
   - Offer a quick call if they want help choosing
   - Link to host guide for reference
2. Send test, then send to full cool host list
3. Update Status to "Form Sent" in the cool host sheet

**Decision rights:** You own the send.

---

### 4. Monitor responses and convert — ongoing

**What to do:**
1. Check form responses daily after the send
2. When a host selects a film:
   - Update cool host sheet Status to "Responded"
   - Confirm the film choice with Operations (check availability)
   - Once confirmed, add the host to the warm host sheet with their film assignment
   - Update cool host sheet Status to "Converted"
   - The host now receives all regular stream communications
3. If a host selected "Need to see the full film first" — route to Garen for screener access

**Decision rights:** You own conversion tracking. Film availability confirmation routes through Operations. Screener access routes through Garen.

---

### 5. Follow up on non-respondents — 1 week after conversion email

**What to do:**
1. Check who hasn't responded to the conversion email
2. Send one individual follow-up from hosts@ — keep it warm and low-pressure
3. If still no response after the follow-up, mark them as "No response" in the cool host sheet
4. Don't push further. Some venues aren't ready this year.

**Decision rights:** You own follow-ups. After two touches (original email + one follow-up), stop.

---

## Where everything lives

| Thing | Location |
|-------|----------|
| Cool host list | V7 Google Sheet — cool host tab |
| Warm host list | V7 Google Sheet — warm host tab |
| Film selection form | Google Forms — [link when created] |
| Film list PDF | Shared Google Drive folder |
| Conversion email template | Email drafts folder |

---

## Escalation

- **Cool host wants to talk on the phone before committing** → You can take the call, or route to Garen if the questions are technical.
- **Film they want isn't available** → Offer alternatives. If they're set on a specific film, route to Operations.
- **Cool host converts very late (mid-April)** → Flag to Garen. Late conversions may need compressed timelines for deliverables.
- **More cool hosts than expected convert** → Flag to Executive Director — this affects scheduling and film distribution.

---

## Anchor questions

1. What was the conversion rate? How many of the cool hosts ended up committing?
2. What made the difference — was it the email, the phone call offer, the form simplicity?
3. Was there a common reason hosts didn't convert? That's useful for next year's recruitment.
