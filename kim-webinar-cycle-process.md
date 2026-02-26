# Webinar Cycle Process — Stream 1

**Owner:** Kim (Week 1 shadowed, Week 2+ solo)
**Backup:** Garen
**Tools:** Mailmeteor, Google Drive, hosts@ Gmail, git (host guide updates — Garen handles until comfortable)

---

## What this is

Every Monday from now through April 13, OEFF runs a host webinar at noon CT. Each webinar has a three-email cycle around it, plus a host guide update after the recording is available. This doc walks through the full cycle for one webinar — repeat it each week.

---

## The cycle

```
Sun/Mon prior week     →  Preview email (template 03)
Sunday evening         →  Reminder email (template 04)
Monday noon            →  Webinar happens (Zoom)
Monday afternoon       →  Download recording from Zoom
Tuesday morning        →  Upload recording to Google Drive
                       →  Update host guide with recording link
                       →  Send recap email (template 05)
```

---

## Step by step

### 1. Preview email — 7 days before (Sunday or Monday)

**Template:** `03-webinar-preview.md` in the email drafts folder

**What to do:**
1. Open Mailmeteor in hosts@ Gmail
2. Select the preview template
3. Swap in this week's content block (each webinar has its own agenda bullets and prep notes — they're in the template file under "Per-Webinar Content Blocks")
4. Merge fields to check: `{{First Name}}`, `{{Webinar Topic}}`, `{{Webinar Date}}`
5. Send a test to yourself first — check that links work, merge fields populated, formatting looks right
6. Schedule or send to the full host list

**Decision rights:** You own this send. No approval needed unless you've changed the wording beyond what's in the template.

---

### 2. Reminder email — 1 day before (Sunday evening or Monday morning)

**Template:** `04-webinar-reminder.md`

**What to do:**
1. Open Mailmeteor, select the reminder template
2. Swap in the topic and date — that's it, this one is short by design
3. Send test, then send to full list
4. Best timing: Sunday 6-7pm CT, or Monday 7-9am CT

**Decision rights:** Same — you own it. This is a nudge, not new content.

---

### 3. Webinar happens — Monday noon CT

**What to do:**
- Attend the webinar (or watch the recording afterward)
- Take quick notes on what was actually covered — the recap email should reflect what happened, not just what was planned
- Note any action items Josh or Ana called out — these go into the recap

**Not your job:** Running the webinar, managing Zoom settings, presenting. That's Josh and the OEFF team. You're tracking content for the follow-up.

---

### 4. Download the recording — Monday afternoon

**What to do:**
1. Log into Zoom (credentials in hosts@ account or ask Garen)
2. Go to Recordings → Cloud Recordings
3. Find the webinar by date
4. Download the MP4 file

**If the recording isn't ready yet:** Zoom cloud recordings can take 1-3 hours to process. Check back later Monday or early Tuesday. Don't hold up the rest of your day for it.

---

### 5. Upload recording to Google Drive — Tuesday morning

**What to do:**
1. Upload the MP4 to the shared OEFF Google Drive folder (Garen will show you the exact folder during shadow session)
2. Set sharing to "Anyone with the link can view"
3. Copy the sharing link — you'll need it for the next two steps

**Naming convention:** `OEFF 2026 Host Webinar — [Topic] — [Date].mp4`
Example: `OEFF 2026 Host Webinar — Marketing Promotion — 2026-03-16.mp4`

---

### 6. Update the host guide — Tuesday morning

**What it is:** The host guide at hosts.oneearthfilmfest.org is a single HTML file that auto-deploys when changes are pushed to git. It has a section listing past webinar recordings.

**For now (Weeks 1-2):** Send Garen the recording link and he'll update the host guide. This takes him ~5 minutes.

**Later (when comfortable):** You can make this update yourself. The process is:
1. Open `~/Desktop/OEFF Clean Data/hosts/index.html`
2. Find the webinar recordings section (search for "recording" — it's in a collapsible details element)
3. Add a new link following the existing pattern
4. Save the file
5. In terminal: `cd ~/Desktop/OEFF\ Clean\ Data/hosts && git add index.html && git commit -m "Add [Topic] webinar recording" && git push`
6. The site updates automatically within a minute

**No pressure on the git part.** It's a nice-to-have, not a requirement. Garen can keep doing this if you'd rather focus on the comms side.

---

### 7. Send the recap email — Tuesday morning

**Template:** `05-webinar-recap.md`

**What to do:**
1. Open Mailmeteor, select the recap template
2. Swap in this week's content block (recap bullets, action items, next webinar info)
3. **Adjust the recap bullets based on your notes from the actual webinar** — the template has suggested bullets, but what was covered may have shifted. Use your judgment.
4. Drop the Google Drive recording link into `{{Recording Link}}`
5. Send test, check links (especially the recording link), then send to full list

**Decision rights:** You own the send. If you need to adjust the recap bullets from what's in the template — because the webinar covered different ground — go for it. That's your judgment call. If you're unsure about tone, send a draft to Garen in Google Chat first.

---

## Where everything lives

| Thing | Location |
|-------|----------|
| Email templates | Email drafts folder (shared Google Drive) — also in `yamm-drafts/` as markdown reference |
| Host list for merges | `oeff-warm-hosts-cleaned.csv` in Google Sheets |
| Host guide (live site) | [hosts.oneearthfilmfest.org](https://hosts.oneearthfilmfest.org) |
| Host guide (source file) | `~/Desktop/OEFF Clean Data/hosts/index.html` |
| Zoom recordings | Zoom cloud → Google Drive shared folder |
| Webinar schedule | Host guide + calendar invite description |

---

## Remaining webinar dates + topics

| Date | Topic | Status |
|------|-------|--------|
| Feb 23 | Background, Logistics, Program Preview | Done — recording available |
| **Mar 2** | **Programming + Per-Film Discussions** | **Next up** |
| Mar 16 | Marketing & Promotion | |
| Mar 23 | Volunteer Recruitment & Training | |
| Mar 30 | AV/Tech Verification & Day-of Support | |
| Apr 6 | Office Hours (optional) | |
| Apr 13 | Office Hours (optional) | |

---

## Escalation

- **Host replies with a question you can answer** → answer it from hosts@, your judgment
- **Host replies with something you're not sure about** → flag in Google Chat to Garen, respond within a business day
- **Host says they can't make a webinar** → reassure them the recording will be sent (it will — that's step 7)
- **Zoom recording doesn't appear** → check back in 3 hours. If still missing after 6 hours, ask Garen to check the Zoom account
- **Mailmeteor merge looks wrong in test** → don't send. Screenshot the issue and send to Garen in Google Chat

---

## The shadow plan

**Mar 2 cycle (your first):** Garen runs the sends, you watch. Your job is to follow along with this doc and note anything that's confusing or missing.

**Mar 16 cycle (your second):** You run the sends, Garen reviews before you hit send. Ask questions as you go — that's the point.

**Mar 23 onward:** You own it. Garen is available but not watching.

---

## Three things to track as you do this

These are the same anchor questions from your starter project. Keep a running doc:

1. **What tripped you up?** Where did this process assume context you didn't have?
2. **What's missing?** If someone else needed to do this next year, what would you add?
3. **What could be tighter?** Patterns you see that could become templates or checklists.

Your notes on these questions are genuinely valuable — they make the system better for next time.
