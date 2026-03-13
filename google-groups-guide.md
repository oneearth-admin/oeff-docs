# OEFF Google Groups Guide

Last updated: 2026-03-05

## Overview

Google Groups on `oneearthcollective.org` serve three functions:
1. **Distribution lists** — email everyone in a group at once
2. **Shared inboxes** — collaborative inbox where multiple people can assign, reply to, and resolve threads (when enabled)
3. **Access control** — grant Drive/Calendar permissions to a group instead of individuals

The source of truth for group membership is the **[Squad Roster](https://docs.google.com/spreadsheets/d/1LAV7DB7g11qSAg0cQXKHJOUlIycCBD6x4gAW50dQDvk/edit?gid=0#gid=0)** spreadsheet, column I ("Groups").

---

## Active Groups

### squad@oneearthcollective.org

**Purpose:** Full OEFF planning team. Announcements, all-hands updates, anything the whole squad should see.

**Type:** Internal distribution list

**Members (14):**

| Name | Email | Role in Group |
|------|-------|---------------|
| Ana Garcia Doyle | ana@ | Owner |
| Garen Hudson | garen@ | Manager |
| Ahmad Garib | ahmad@ | Member |
| Andy Nunez | andy@ | Member |
| Cesar Almeida | cesar@ | Member |
| Erin Turney | tech@ | Member |
| Jani Wodi | jani@ | Member |
| Joanna Drew | joanna@ | Member |
| Joshua Bynum | joshua@ | Member |
| Kim Pham | kim@ | Member |
| Maria Iman | maria@ | Member |
| Michael Alexander | michael@ | Member |
| Peter Akai | peter@ | Member |
| Sanaa Davis | sanaa@ | Member |

**Notes:**
- OEC domain members only — YFC collaborators (Lisa, Sandy, Sue) removed 2026-03-06 to simplify delivery
- `helen@` was previously a member — removed during 2026-03-05 sync (not on current roster)

---

### core@oneearthcollective.org

**Purpose:** Leadership and key coordinators. Decision-making threads, budget discussions, strategic planning — things that don't need 19 inboxes.

**Type:** Internal distribution list (NEW — created 2026-03-05)

**Members (7):**

| Name | Email | Role |
|------|-------|------|
| Ana Garcia Doyle | ana@ | Executive Director |
| Cesar Almeida | cesar@ | Marketing Manager |
| Erin Turney | tech@ | Creative Assets Lead |
| Garen Hudson | garen@ | AV/Tech Coordinator |
| Joshua Bynum | joshua@ | Digital Comms Coordinator |
| Kim Pham | kim@ | Host Comms Support |
| Michael Alexander | michael@ | Development Manager |

**Notes:**
- Sue (YFC) removed 2026-03-06 — external members were causing delivery issues
- Joanna Drew (Grants Manager) is on squad@ only — she's OEC-wide, not OEFF-specific

---

### interns@oneearthcollective.org

**Purpose:** OEFF intern cohort. Scheduling, onboarding, intern-specific coordination.

**Type:** Internal distribution list (NEW — created 2026-03-05)

**Members (4):**

| Name | Email |
|------|-------|
| Jani Wodi | jani@ |
| Maria Iman | maria@ |
| Peter Akai | peter@ |
| Sanaa Davis | sanaa@ |

**Notes:**
- All interns are also on squad@
- Use this for availability surveys, festival week assignments, and onboarding materials

---

### hosts@oneearthcollective.org

**Purpose:** External-facing support group for screening hosts. Hosts email this address for logistics help, tech questions, and general inquiries.

**Type:** Shared inbox (collaborative inbox enabled)

**Members (5):**

| Name | Email | Role in Group |
|------|-------|---------------|
| Ana Garcia Doyle | ana@ | Owner |
| Joshua Bynum | joshua@ | Owner |
| Erin Turney | tech@ | Owner |
| Garen Hudson | garen@ | Member |
| Kim Pham | kim@ | Member |

**Notes:**
- This is the primary contact point for hosts — linked from the host guide at hosts.oneearthfilmfest.org
- Owners can manage group settings; Members can view and respond
- External senders (hosts) can email this address and reach the team

---

### films@oneearthcollective.org

**Purpose:** Filmmaker communications — format availability, file delivery, QC status, licensing.

**Type:** Shared inbox

**Members (6):**

| Name | Email | Role in Group |
|------|-------|---------------|
| Garen Hudson | garen@ | Owner |
| Joshua Bynum | joshua@ | Owner |
| Ana Garcia Doyle | ana@ | Member |
| Erin Turney | tech@ | Member |
| Peter Akai | peter@ | Member |
| Sanaa Davis | sanaa@ | Member |

**Notes:**
- External filmmakers and distributors email this address
- Peter and Sanaa (interns) handle initial triage

---

### classroom_teachers@oneearthcollective.org

**Purpose:** System-generated group for Google Classroom. Not actively used for OEFF.

**Members:** 0

**Notes:** Do not delete — Google Workspace requires this group.

---

## Group Types Explained

### Distribution list (squad@, core@, interns@)
- Email the group address, everyone gets it
- No shared inbox — replies go to the sender, not the group
- Good for: announcements, meeting notes, all-hands updates

### Shared inbox (hosts@, films@)
- Email arrives in a shared inbox visible to all members
- Members can assign conversations, mark as resolved, add labels
- Replies come FROM the group address (e.g., hosts@), not individual accounts
- Good for: external-facing support, intake workflows
- Enable in admin.google.com > Groups > [group] > Settings > Enable collaborative inbox

### Access control
- Any group can be used as a permission target in Drive, Calendar, etc.
- Example: share a Drive folder with core@ instead of 8 individual emails
- When someone leaves core@, they lose access automatically

---

## Internal vs. External

| Group | Who can email it | Who receives |
|-------|-----------------|--------------|
| squad@ | Domain members only | All squad members |
| core@ | Domain members only | Core team only |
| interns@ | Domain members only | Intern cohort |
| hosts@ | Anyone (external) | Host support team |
| films@ | Anyone (external) | Film & media team |

**To change external posting:** admin.google.com > Groups > [group] > Access settings > Who can post

---

## How to Update Groups

### Option 1: Sync from the Squad Roster (recommended)

1. Edit column I ("Groups") in the [Squad Roster sheet](https://docs.google.com/spreadsheets/d/1LAV7DB7g11qSAg0cQXKHJOUlIycCBD6x4gAW50dQDvk/edit?gid=0#gid=0)
2. Run the sync script:

```bash
# Preview changes (dry run)
python3 ~/tools/group-sync.py

# Apply changes
python3 ~/tools/group-sync.py --apply

# Just list current members
python3 ~/tools/group-sync.py --list
```

The script reads the sheet, compares against current Google Group memberships, and shows what needs to change. It only modifies squad@, core@, and interns@ — it does NOT touch hosts@ or films@ (those have different membership logic).

### Option 2: Manual (admin console)

1. Go to [admin.google.com/ac/groups](https://admin.google.com/ac/groups)
2. Click the group
3. Members > Add members / Remove members

Use this for hosts@ and films@ since those aren't managed by the sync script.

---

## Google Spaces (Chat)

Google Spaces are separate from Groups. A Space is a persistent chat room; a Group is an email list. They can overlap in membership but are managed independently.

Current OEFF-related Spaces should be documented separately if they exist. Groups and Spaces do not automatically sync members.

---

## Credentials & API Access

The sync script uses OAuth2 via `~/tools/google-auth.py`:

- **Account:** garen@oneearthcollective.org
- **GCP project:** oeff-tools
- **Token:** ~/tools/.google-token.json
- **Scopes:** Sheets (read roster) + Admin Directory Groups (manage memberships)
- **API enabled:** Admin SDK API on oeff-tools project (Google Cloud Console)

To re-authorize:
```bash
python3 ~/tools/google-auth.py --account oec --scopes "sheets,admin_groups"
```

---

## Decision Log

| Date | Decision |
|------|----------|
| 2026-03-05 | Created Groups column (I) in Squad Roster sheet as source of truth |
| 2026-03-05 | Enabled Admin SDK API on oeff-tools GCP project |
| 2026-03-05 | Built group-sync.py for sheet-to-groups sync |
| 2026-03-05 | Three-tier model: squad@ (all), core@ (leadership), interns@ (cohort) |
| 2026-03-05 | YFC split: Sue on core@ + squad@, Lisa/Sandy on squad@ only |
| 2026-03-05 | hosts@ and films@ managed manually (external-facing, different logic) |
| 2026-03-06 | Removed all YFC members (Lisa, Sandy, Sue) from squad@ and core@ — external members caused delivery issues |
| 2026-03-06 | Fixed squad@ whoCanPostMessage: ALL_IN_DOMAIN → ALL_MEMBERS |
| 2026-03-06 | Set explicit ALL_MAIL delivery for all members |
| 2026-03-06 | Fixed core@ allowExternalMembers: false → true (then removed external members anyway) |

---

## Open Questions

- [ ] Should hosts@ and films@ be added to the sync script, or stay manual?
- [ ] Group posting settings need verification in admin console (who can post externally?)
- [ ] Are there Google Spaces that should be documented here?
- [ ] Helen removed from squad@ — confirm she's no longer on the team
