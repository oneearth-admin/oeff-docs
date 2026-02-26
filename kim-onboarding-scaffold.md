# Kim Onboarding Scaffold

Status: UPDATED — Feb 24, 2026
Purpose: What Garen needs to prepare, and what Kim's first two weeks look like.

---

## Before tomorrow's call (Garen prep)

### Access checklist
- [ ] hosts@oneearthfilmfest.org — shared inbox access
- [ ] V7 Google Sheet — viewer or editor
- [ ] Google Drive folder (curated onboarding docs)
- [ ] Mailmeteor — installed on hosts@ account
- [ ] Host guide link: hosts.oneearthfilmfest.org

### Docs to share (three, not twelve)
1. **Host Comms Plan** — the 5-stream operations plan (this is her map)
2. **Starter Project Brief** — what she's actually doing and how it's scoped
3. **Host Guide** — what hosts see, so she knows the other side of every email

Everything else (dependency map, onboarding overview, runbook) is reference. She finds it when she needs it, not before.

### First task, named
**"Send the next webinar reminder via Mailmeteor."**
Concrete. Completable. Low-stakes. Garen shadows the first one, Kim runs the second solo.

---

## Tomorrow's call (9:00-9:30, Kim joins)

### Frame for the 30 minutes
This is a get-to-know-you, not a briefing. Kim should leave with:

1. **What OEFF is** — one paragraph, plain language
2. **Where we're at** — 57 days out, 16 screenings, hosts confirmed, comms infrastructure built
3. **What her role is** — operate the host communications system and document what doesn't work
4. **What happens this week** — three docs to read, one shadow session, first sync Thursday or Friday

### What NOT to do
- Don't walk through all 5 streams
- Don't explain the full tech stack
- Don't over-brief. She's a change management professional. She'll figure out the system faster by touching it than by hearing about it.

---

## Communication contract

| Channel | Use for |
|---------|---------|
| Email | Async updates, sharing drafts, non-urgent questions |
| SMS | Quick coordination, "are you available?" |
| Google Chat | Day-to-day back-and-forth, links, quick questions |
| Phone | When something's complex or nuanced, or when text isn't working |

**Sync cadence:** 2x/week, 30 min each
- Suggest: Monday (plan the week) + Thursday (check progress, unblock)
- Format: Loose — no formal agenda. "What are you working on, what's stuck, what's next."

**Escalation rule:** If a host asks something Kim doesn't know, she doesn't guess. She flags it in Google Chat and Garen responds within a few hours. No host should wait more than a business day.

---

## Tool + identity model

### Mail merge: Mailmeteor
Replacing YAMM. Gmail-native interface (looks like composing a regular email), shared template support (up to 10 collaborators), works with Send As aliases.

- **Cost:** $12.99/user/month (Premium) for 2-3 users
- **Why not YAMM:** YAMM cannot use Gmail delegated access — each user must log into the sending account directly. No shared template infrastructure. Workarounds only.
- **Migration risk:** 4 of 5 comms streams are zero-risk. Stream 2 (deliverables shipping) has a moderate question around open tracking for 48-hour no-open follow-ups — assess whether this workflow is active in practice.

### Sending identity: Gmail "Send As" delegation
No shared account. No admin@ or comms@ user needed.

1. Google Workspace admin grants "Send mail as hosts@" to Kim's account
2. Kim adds hosts@oneearthfilmfest.org as a Send As alias in her Gmail settings
3. Kim verifies via confirmation email
4. Mailmeteor automatically sees hosts@ as an available sender

**Result:** Kim sends from her own login. Emails come from hosts@. Replies go to hosts@ group inbox. Audit trail shows who actually sent each message.

### Shared workflow model
- **Templates** live in Mailmeteor — Garen builds, shares with Kim's account. Updates propagate.
- **Merge data** lives in shared Google Sheets (already collaborative by nature).
- **Email drafts** live in shared Google Drive folder owned by the org (role-portable, survives operator turnover).

When Kim leaves: revoke Send As permission, revoke Mailmeteor template sharing. Templates and merge data stay with the org.

---

## Garen's timeline

### Today (Monday Feb 24)
- [ ] Prep access checklist — confirm Kim has hosts@ inbox, V7 sheet, Drive folder
- [ ] Pick three docs to share tomorrow

### Tomorrow (Tuesday Feb 25)
- [ ] 8:30–9:00 — Priorities + prep with Erin and Ana
- [ ] 9:00–9:30 — Kim intro. Hand over three docs.
- [ ] 9:30–10:00 — Debrief with Erin and Ana
- [ ] 10:00–11:00 — Erin scope: contract, on-site, milestones
- [ ] 11:45 — Squad call

### Wednesday Feb 26
- [ ] Install Mailmeteor on hosts@ account (5 min)
- [ ] Send one test merge — 3-5 warm hosts, low-stakes email. Validate merge fields, Send As, scheduling, rendering.
- [ ] Answer Stream 2 question: is the 48-hour no-open follow-up real or theoretical?

### Thursday Feb 27
- [ ] First sync with Kim — review her questions, walk through one Mailmeteor send cycle together
- [ ] Set up Send As — admin grants Kim permission, Kim adds and verifies in Gmail
- [ ] Share Mailmeteor templates with Kim's account

### Friday Feb 28 — Decision point
- [ ] Commit or revert. If test send went clean: Mailmeteor is the tool.
- [ ] Rename yamm-drafts/ → email-drafts/
- [ ] Update comms plan tool stack section

---

## Week 1: Shadow and orient

### Monday (Feb 25)
- 9:00-9:30: Intro call (Ana + Garen + Kim)
- Kim receives: Host Comms Plan, Starter Project Brief, Host Guide link
- Kim reads the three docs at her own pace

### Tuesday-Wednesday
- Kim reviews V7 sheet structure (just the Hosts tab and Events_2026 tab)
- Kim watches a recorded webinar or reviews a past send (Garen provides example)
- Kim drafts the next webinar reminder (doesn't send — Garen reviews)

### Thursday or Friday — First sync
- Review Kim's draft reminder
- Walk through one full Mailmeteor send cycle together (compose, merge fields, test send, schedule)
- Answer questions from her first few days of reading
- Confirm she has all access she needs

### What Kim is tracking (three anchor questions)
1. What tripped me up? Where did docs assume context I didn't have?
2. What's missing for the next person who does this job?
3. Where are repeated patterns that could be templates or checklists?

---

## Week 2: First solo cycle

### Kim owns Stream 1 (webinar reminders + recording follow-ups)
- Monday: Schedule reminder for next webinar (2 days before)
- Day after webinar: Send follow-up with recording link + key takeaways
- Update host guide with recording link
- Garen reviews output but doesn't co-pilot

### Mid-week sync
- What worked, what didn't
- Any host responses that need escalation
- Start identifying which Stream 2-4 tasks she's ready to pick up

### End of week
- Kim shares running notes (anchor questions)
- Garen and Kim decide together which stream to add next

---

## Weeks 3-7: Expand

Kim picks up additional streams based on confidence and calendar:
- **Stream 2** (deliverables shipping) — starts ~3 weeks before first screening
- **Stream 3** (milestone communications) — Ana approves messaging, Kim sends
- **Stream 4** (data collection forms) — pre-event readiness forms go out 3 weeks before each screening

Each new stream: Kim reads the relevant section of the comms plan, does one supervised cycle, then owns it.

---

## Week 8: Wrap and debrief

- Kim delivers operator notes (compiled from her running anchor-question doc)
- 30-min debrief: What worked? What should change for next year?
- Improved templates handed off
- Decision point: festival week on-site role (separate scope, separate conversation)

---

## Success signals

**Week 1:** Kim can explain what the 5 streams are and has sent one test email.
**Week 2:** Kim has independently sent a webinar reminder and follow-up. Garen didn't need to intervene.
**Week 3:** Kim is operating 2+ streams. Host response time hasn't degraded.
**Week 8:** Someone new could pick up Kim's operator notes and run the system next year.
