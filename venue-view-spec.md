# Venue View Spec: `2026_Venue_Sections`

Airtable view contract for `generate-venue-sections.py`.

## View Configuration

| Setting | Value |
|---------|-------|
| **Base** | OEFF 2026 (`app9DymWrbAQaHH0K`) |
| **Table** | Events |
| **View name** | `2026_Venue_Sections` |
| **Filter** | `Year = 2026` AND `Pipeline_Status` in (`Confirmed`, `Pending`) |
| **Sort** | Venue Name (A-Z) |

## Required Fields

### From Events table (direct)

| Field | Type | Used in state | Notes |
|-------|------|---------------|-------|
| `Pipeline_Status` | Single select | all | Filter criteria |
| `Event_Date` | Date | mar, apr | ISO format preferred |
| `Event_Time` | Single line text | mar, apr | e.g. "7:00 PM" |
| `Doors_Time` | Single line text | apr | e.g. "6:15 PM" |
| `RSVP_URL` | URL | mar, apr | Luma, Eventbrite, or any platform |
| `RSVP_Count` | Number | apr | Current registration count |
| `Volunteer_Needs` | Long text | mar | Free text describing needs |
| `Screening_Packet_URL` | URL | apr | Secure download link (not rendered in feb/mar) |
| `Venue` | Link to Venues | all | Single linked record |
| `Film` | Link to Films_2026 | all | Single linked record |

### From Venues table (via Events.Venue link)

| Field | Type | Used in state | Notes |
|-------|------|---------------|-------|
| `Name` | Single line text | all | Primary display name |
| `City` | Single line text | all | Location display |
| `Region` | Single line text | all | e.g. "South Side", "Suburban North" |
| `Capacity` | Number | apr | Seat count |
| `Contact_Name` | Single line text | mar, apr | Primary venue contact |
| `Contact_Email` | Email | mar, apr | Primary venue contact email |
| `Facility_Contact` | Email | apr | Building/facility manager email |
| `AV_Contact` | Single line text | (reserved) | AV coordinator name |
| `Equipment_Notes` | Long text | (reserved) | AV setup details |

### From Films_2026 table (via Events.Film link)

| Field | Type | Used in state | Notes |
|-------|------|---------------|-------|
| `Title` | Single line text | all | Film title for display |
| `Runtime_Min` | Number | apr | Minutes, used for day-of timeline |
| `Film_Contact` | Link to Film_Contacts | (reserved) | Filmmaker contact |

### From Film_Contacts table (via Films_2026.Film_Contact link)

| Field | Type | Used in state | Notes |
|-------|------|---------------|-------|
| `Name` | Single line text | (reserved) | Filmmaker name |
| `Email` | Email | (reserved) | Filmmaker email |

## Linked Record Resolution Chain

```
Events.Venue  --> Venues (name, city, region, capacity, contact, facility)
Events.Film   --> Films_2026 (title, runtime)
Films_2026.Film_Contact --> Film_Contacts (name, email)
```

The `2026_Venue_Sections` view pre-joins these relationships, avoiding the 19/31 missing Film_ID problem that occurs in flat CSV exports where linked records lose their join context.

## Privacy Constraints

Fields that must NEVER appear in generated HTML:

- Phone numbers (any format)
- Dropbox URLs or passwords
- Screening packet URLs in feb or mar states (only apr)
- Personal mobile numbers (emergency contact uses email + hotline hours only)

The generator enforces these via regex checks that fail the build.

## Event Registration: Platform-Agnostic

The `RSVP_URL` field is a plain URL. It can point to Eventbrite, Luma, or any registration platform. The generator renders it as "Your event page" — switching platforms per-venue requires only an Airtable update, no script changes.

## State Transitions

| State | Active when | Badge | Key additions |
|-------|------------|-------|---------------|
| `feb` | Before March 10 | "Confirmed Host" | Date/time pending |
| `mar` | March 10 - April 4 | "On Track" | All details confirmed, event page, marketing |
| `apr` | April 5 onward | "Ready" | Doors, capacity, RSVPs, packet, timeline |

---

Last updated: 2026-02-22
