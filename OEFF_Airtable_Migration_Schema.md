# OEFF Film Festival Database - Airtable Migration Schema

**Document Generated:** February 6, 2026
**Source Files:**
- V7-with-Dashboard.xlsx (33 sheets, ~1,200 data rows)
- Benefits Tracking 2026.xlsx (2 sheets)

---

## EXECUTIVE SUMMARY

### Current State
- **Core Data Tables:** 5 base tables (Hosts, Films_2026, Events_2025/2026/2024, Film_Contacts, Event_Media, Packet_QA, Host_Intake, Participants, Recordings)
- **Archive Data:** 12 historical sheets from 2024-2025 seasons (should migrate to separate archive base or views)
- **Reference Data:** Partners (150), Metrics (110), Gap Analysis, Matching worksheets
- **Dashboards:** 2 dashboard sheets + Schema Guide + Color Legend (documentation)

### Recommended Airtable Structure
**Primary Base:** OEFF Festival Database 2026 (11 Tables)
**Secondary Bases (Optional):**
- Archive Base (2024-2025 historical data)
- Sponsor/Partner Base (integrated from Benefits Tracking 2026.xlsx)

---

## TABLE 1: VENUES
**Status:** Core table | **Source:** Hosts sheet
**Row Count:** 100 venues
**Primary Field:** Venue_ID

### Fields

| Field Name | Airtable Type | Source Column | Required | Notes |
|---|---|---|---|---|
| **Venue_ID** | Single line text | Venue_ID | Yes | Format: V-XXX (e.g., V-001) |
| **Venue Name** | Single line text | Venue_Name | Yes | Official venue name |
| **Region** | Single select | Region | No | Chicago Central, Northern Suburbs, Southern Suburbs, Western Suburbs, etc. (52/100 populated) |
| **Capacity** | Number | Capacity | No | Seating capacity. Note: Some entries show "TBD" or mixed formats (14/100 populated) |
| **Tech Tier** | Single select | Tech_Tier | No | Options: T1, T2, T3 (19/100 populated) |
| **Contact Information** | Long text | Contact_Info | No | Concatenated contact details (2/100 populated) |
| **First OEFF Year** | Number | First_OEFF_Year | No | Year venue joined festival (73/100 populated) |
| **Accessibility Features** | Long text | Accessibility | No | Accessibility accommodations (0/100 - to be populated) |
| **Notes** | Long text | Notes | No | Historical notes about venue (77/100 populated) |
| **Active Status** | Single select | [DERIVED] | No | Options: Active, Inactive, TBD (auto-populate based on presence in 2026 events) |
| **Previous Contacts** | Long text | Previous_Contacts | No | Historical venue contact names/info for reference (from prior seasons) |

### Linked Records
- Linked to **Events** (one venue → many events)
- Linked to **Host Intake** (one venue → one intake form)

### Suggested Views
1. **Active 2026 Venues** - Filtered to venues with 2026 events
2. **By Region** - Grouped by Region field
3. **By Tech Tier** - Grouped by Tech_Tier
4. **Capacity Range** - Sorted by capacity
5. **Data Gaps** - Filter to TBD/empty fields for completion

---

## TABLE 2: FILMS
**Status:** Core table | **Source:** Films_2026 sheet
**Row Count:** 12 films
**Primary Field:** Film_ID

### Fields

| Field Name | Airtable Type | Source Column | Required | Notes |
|---|---|---|---|---|
| **Film_ID** | Single line text | Film_ID | Yes | Format: F26-XXX (e.g., F26-001) |
| **Film Title** | Single line text | Film_Title | Yes | Official film title |
| **Runtime (minutes)** | Number | Runtime_Min | No | Duration in minutes (11/12 populated) |
| **Release Year** | Number | Release_Year | No | Original film release year (11/12 populated) |
| **Primary Topic** | Single select | Primary_Topic | Yes | e.g., Wildlife, Waste & Recycling, Built Environment (all 12 populated) |
| **Secondary Topic** | Single select | Secondary_Topic | Yes | Related topic (12/12 populated) |
| **Tertiary Topic** | Single select | Tertiary_Topic | No | Additional theme (12/12 populated) |
| **Marginalized Voices** | Checkbox | Marginalized_Voices | No | Boolean indicator (12/12 populated) |
| **Filmmakers** | Long text | Filmmaker_Names | Yes | Names of directors/producers (12/12 populated) |
| **Film Website** | URL | Film_Website | No | Link to film info (12/12 populated; currently placeholder) |
| **Trailer Link** | URL | Trailer_Link | No | Link to trailer (0/12 - to be populated) |
| **Caption Status** | Single select | Caption_Status | No | Options: Burned In, SRT File Available, Needs Help, N/A (0/12 - to be populated) |
| **Audio Description** | Checkbox | Audio_Description | No | Has AD track (0/12 - to be populated) |
| **Spanish Version** | Checkbox | Spanish_Available | No | Spanish language version available (0/12 - to be populated) |
| **Intake Form Received** | Checkbox | Intake_Received | Yes | From film contact (12/12 populated) |
| **Notes** | Long text | Notes | No | Additional film information (0/12 - to be populated) |

### Linked Records
- Linked to **Film Contacts** (one film → many contacts)
- Linked to **Events** (one film → many screenings)

### Suggested Views
1. **2026 Lineup** - All confirmed films
2. **By Topic** - Grouped by Primary Topic
3. **Missing Assets** - Filter to films with empty Trailer/Caption Status
4. **Intake Status** - Filter by Intake_Received checkbox
5. **Accessibility Ready** - Filter to films with captions/AD/Spanish

---

## TABLE 3: EVENTS
**Status:** Core table | **Source:** Events_2026, Events_2025, Events_2024 combined
**Row Count:** 219 events (31 from 2026, 180 from 2025, 8 from 2024)
**Primary Field:** Event_ID

### Fields

| Field Name | Airtable Type | Source Column | Required | Notes |
|---|---|---|---|---|
| **Event_ID** | Single line text | Event_ID | Yes | Format: Exx-XXX (e.g., E26-001, E25-001, E24-001) |
| **Year** | Number | [DERIVED] | Yes | Extract from Event_ID: 26, 25, or 24 |
| **Event Tier** | Single select | Venue_Status | No | Options: Flagship, Community, Community/Hybrid Stream. Extracted from column A of 2026HostVenues |
| **Venue** | Link to Venues | Venue_ID | Yes | Foreign key to Venues table |
| **Venue Name** | Single line text | Venue_Name | Yes | Denormalized for readability; sync from Venue |
| **Date** | Date | Date | No | Event date (14/31 for 2026, 56/180 for 2025, 7/8 for 2024 populated) |
| **Time** | Single line text | Time | No | Start time, e.g., "6-9P", "6:30P" |
| **Ticket Price** | Single line text | Tix_Price | No | e.g., "Free", "$75 ea or two for $150". Free text to accommodate varied pricing structures |
| **Event Type** | Single select | Event_Type | No | Public, Public but ticketed, Invite only, Internal (29/31 for 2026 populated) |
| **Film** | Link to Films | Film_ID | No | Foreign key to Films table (for 2026 events with Film_ID) |
| **Film Title** | Single line text | Film_Title | No | Film screening title/description |
| **Film Status** | Single select | Film_Status | No | Options: Confirmed, Not Confirmed, TBD, Cancelled (parse from column K, e.g., "Rooted (CONFIRMED)") |
| **Film Survey Complete** | Date | Film_Survey_Date | No | Date host completed film preference survey |
| **Pipeline Status** | Single select | Pipeline_Status | No | Scheduled, In Progress, Completed, Cancelled (29/31 for 2026 populated) |
| **OEFF Rep** | Single line text | OEFF_Rep | No | OEFF staff representative (0/31 - to be populated) |
| **Team Contact** | Single line text | Team_Contact | No | Internal contact person (16/31 for 2026 populated) |
| **Host Fee Ask** | Currency | Host_Fee_Ask | No | Requested honorarium (0/31 - to be populated) |
| **Host Fee Committed** | Currency | Host_Fee_Committed | No | Confirmed payment (0/31 - to be populated) |
| **Host Fee Invoice Amount** | Currency | Host_Fee_Invoice_Amt | No | Actual invoiced amount |
| **Host Fee Invoice Info** | Long text | Host_Fee_Invoice_Info | No | Invoice details, PO numbers, billing notes |
| **Host Fee Invoice Sent** | Date | Host_Fee_Invoice_Sent | No | Date invoice was sent (and by whom — append name in Notes) |
| **Host Fee Reminder Sent** | Date | Host_Fee_Reminder_Sent | No | Date payment reminder was sent |
| **Host Fee Payment Received** | Date | Host_Fee_Payment_Received | No | Date payment was received |
| **Host Fee Status** | Single select | Host_Fee_Status | No | Pending, Invoiced, Reminded, Paid (expanded from original 3-option list) |
| **Licensing Request Status** | Single select | Licensing_Request_Status | No | Options: Not Started, Single License Requested, Multi-License Requested, Approved, Denied. More granular than License_Status |
| **License Status** | Single select | License_Status | No | License agreement status (0/31 - to be populated) |
| **Film License Amount** | Currency | Film_License_Amt | No | License fee amount approved by Ana |
| **Film Licensing Contact** | Single line text | Film_License_Contact | No | Contact info for licensing (may overlap with Film_Contacts table) |
| **License Invoice Received** | Date | License_Invoice_Received | No | Date OEC received the film license invoice |
| **License Invoice Paid** | Date | License_Invoice_Paid | No | Date OEC paid the film license invoice |
| **Volunteer Needs** | Long text | Volunteer_Needs | No | Volunteer requirements and notes for this event |
| **Notes** | Long text | Notes | No | Event details, special notes, early program notes (21/31 for 2026 populated) |

### Linked Records
- **Venue** → Venues table (required)
- **Film** → Films table (optional, mainly for 2026)
- **Host Intake** → Host Intake table (optional, link via Venue_ID)
- **Event Media** → Event_Media table (optional)
- **Packet QA** → Packet_QA table (optional)
- **Recordings** → Recordings table (optional)
- **Participants** → Participants table (optional)
- **Festival Metrics** → Festival_Metrics table (optional)

### Suggested Views
1. **2026 Events - Calendar** - Filter Year=26, sorted by Date
2. **2025 Events - Archive** - Filter Year=25
3. **2024 Events - Archive** - Filter Year=24
4. **Status Board** - Grouped by Pipeline Status
5. **By Event Tier** - Grouped by Event Tier (Flagship, Community, Hybrid)
6. **Host Fees Due** - Filter Host_Fee_Status ≠ "Paid"
7. **Host Fee Invoice Tracker** - Show Ask, Committed, Invoice Amt, Sent, Reminder, Payment Received
8. **Licensing Pipeline** - Show Licensing_Request_Status, License_Status, Film_License_Amt, Invoice Received/Paid dates
9. **Licensing Needed** - Filter License_Status = "Pending"
10. **Missing Films** - Filter Film empty, Year=26
11. **By Venue** - Grouped by Venue
12. **Upcoming Events** - Filter Date >= today, sorted by Date
13. **Volunteer Planning** - Filter Volunteer_Needs not empty, sorted by Date

---

## TABLE 4: FILM CONTACTS
**Status:** Child/Related table | **Source:** Film_Contacts sheet
**Row Count:** 9 contacts
**Primary Field:** Contact_ID

### Fields

| Field Name | Airtable Type | Source Column | Required | Notes |
|---|---|---|---|---|
| **Contact_ID** | Single line text | Contact_ID | Yes | Format: FC26-XXX (e.g., FC26-001) |
| **Film** | Link to Films | Film_ID | Yes | Foreign key to Films table |
| **Film Title** | Single line text | Film_Title | Yes | Denormalized; sync from Film |
| **Contact Name** | Single line text | Contact_Name | Yes | Primary contact person (9/9 populated) |
| **Email** | Email | Email | Yes | Contact email address (9/9 populated) |
| **Phone** | Phone | Phone | Yes | Contact phone number (9/9 populated; mixed formats) |
| **Role** | Single select | Role | Yes | Producer, Filmmaker, Director, Distributor, Agent (9/9 populated) |
| **Is Primary** | Checkbox | Is_Primary | Yes | Primary contact indicator (9/9 = Yes) |
| **Secondary Contact Name** | Single line text | Secondary_Name | No | Secondary contact person name (6/9 populated) |
| **Secondary Email** | Email | Secondary_Email | No | Secondary contact email (6/9 populated) |
| **Formats Available** | Long text | Formats_Available | No | Video formats provided (e.g., H.264 MP4, ProRes, DCP; 9/9 populated) |
| **Caption Status** | Single select | Caption_Status | No | Burned In, SRT File, Needs Help, N/A (9/9 populated) |
| **Audio Description Available** | Checkbox | Audio_Description | No | Has AD track (9/9 populated) |
| **Spanish Version Available** | Checkbox | Spanish_Available | No | Spanish language available (9/9 populated) |
| **Submission Timestamp** | Date | Timestamp | No | Form submission date (9/9 populated: Jan 26, 2026) |

### Linked Records
- **Film** → Films table (required)

### Suggested Views
1. **All 2026 Contacts** - All records with contact info
2. **By Role** - Grouped by Role
3. **Format Ready** - Grouped by Formats Available
4. **Caption Status** - Grouped by Caption_Status
5. **Recently Submitted** - Sorted by Timestamp (newest first)
6. **Contact Directory** - Show Contact Name, Email, Phone

---

## TABLE 5: EVENT MEDIA
**Status:** Child/Related table | **Source:** Event_Media sheet
**Row Count:** 25 media assets
**Primary Field:** Media_ID

### Fields

| Field Name | Airtable Type | Source Column | Required | Notes |
|---|---|---|---|---|
| **Media_ID** | Single line text | Media_ID | Yes | Format: M26-XXX (e.g., M26-001) |
| **Event** | Link to Events | [DERIVED] | No | Link to associated event (match by date/venue) |
| **Event Name** | Single line text | Event_Name | Yes | Event identifier (25/25 populated) |
| **Venue** | Single line text | Venue | No | Venue address/name (24/25 populated) |
| **Date** | Date | Date | No | Event date (24/25 populated) |
| **Time** | Single line text | Time | No | Event time range (24/25 populated) |
| **Film Title** | Single line text | Film_Title | Yes | Featured film/content (24/25 populated) |
| **Feature Link** | URL | Feature_Link | No | Link to feature film video (0/25 - to be populated) |
| **English Subtitles** | Checkbox | English_Subs | No | English subtitle availability (0/25 - to be populated) |
| **Spanish Subtitles** | Checkbox | Spanish_Subs | No | Spanish subtitle availability (0/25 - to be populated) |
| **Dropbox Link** | URL | Dropbox_Link | No | Link to media file storage (0/25 - to be populated) |
| **Intro Link** | URL | Intro_Link | Yes | Intro reel video link (25/25 populated; vimeo/example.com) |
| **Trailer Link** | URL | Trailer_Link | Yes | Trailer video link (25/25 populated) |
| **YFC Promo Link** | URL | YFC_Promo_Link | Yes | Young Filmmaker Choice promo (25/25 populated) |
| **PreShow Reel Link** | URL | PreShow_Reel_Link | Yes | Pre-show reel link (25/25 populated) |
| **Has Captions** | Checkbox | Has_Captions | No | Captions included in media (1/25 populated) |
| **Needs Merge** | Checkbox | Needs_Merge | No | Media files need merging (1/25 populated) |
| **Merge Status** | Single select | Merge_Status | No | Pending, In Progress, Complete (0/25 - to be populated) |
| **Verified By** | Single line text | Verified_By | No | Person who verified media (1/25 = "System Prep") |
| **Notes** | Long text | Notes | No | Technical/QA notes (0/25 - to be populated) |

### Linked Records
- **Event** → Events table (optional, link by Date/Venue match)

### Suggested Views
1. **2025 Event Media** - All records (25 from 2025)
2. **Missing Feature Links** - Filter Feature_Link empty
3. **Needs Merge** - Filter Needs_Merge = Yes
4. **Ready for Distribution** - Filter Has_Captions = Yes, Merge_Status = Complete
5. **By Event** - Grouped by Event Name

---

## TABLE 6: PACKET QA
**Status:** Child/Related table | **Source:** Packet_QA sheet
**Row Count:** 23 QA records
**Primary Field:** Packet_ID

### Fields

| Field Name | Airtable Type | Source Column | Required | Notes |
|---|---|---|---|---|
| **Packet_ID** | Single line text | Packet_ID | Yes | Format: PKT-XXX (e.g., PKT-001) |
| **Event Number** | Number | Event_Num | Yes | Sequential event number (23/23 populated) |
| **Event Time** | Single line text | Event_Time | Yes | Time range for event (23/23 populated) |
| **Film Title** | Single line text | Film | Yes | Film name/content description (23/23 populated) |
| **Location** | Single line text | Location | Yes | Full venue address (23/23 populated) |
| **Sponsor Loop Status** | Single select | Sponsor_Loop | Yes | Done, In Progress, Needs Work (23/23 populated) |
| **Opening Remarks** | Checkbox | Opening_Remarks | No | Opening remarks prepared (0/23 - to be populated) |
| **YFC Promo Status** | Single select | YFC_Promo | No | Done, In Progress, Needed (1/23 populated) |
| **OEFF Promo Status** | Single select | OEFF_Promo | No | Done, In Progress, Needed (1/23 populated) |
| **Sponsor Slide Status** | Single select | Sponsor_Slide | No | Done, In Progress, Needed (1/23 populated) |
| **Laurel Status** | Single select | Laurel | No | Done, In Progress, Needed (1/23 populated) |
| **YFC Short Films** | Long text | YFC_Short | Yes | Young Filmmaker Choice shorts list (23/23 populated) |
| **Feature Film** | Long text | Feature | Yes | Feature film details (23/23 populated) |
| **QR Loop Status** | Single select | QR_Loop | No | Done, In Progress, Needed (1/23 populated) |
| **Concatenation Created** | Single select | Concat_Created | Yes | Open, In Progress, Complete (23/23 = "open") |
| **Overall Status** | Single select | Status | No | Done, In Progress, Pending (1/23 populated) |
| **Notes** | Long text | Notes | No | QA notes and issues (0/23 - to be populated) |

### Linked Records
- **Event** → Events table (optional, link by Event_Num or film title match)

### Suggested Views
1. **QA Status Board** - Grouped by Overall Status
2. **To Do** - Filter Overall_Status ≠ "Done"
3. **Sponsor Loop Tracking** - Filter by Sponsor_Loop_Status
4. **Concat Status** - Filter Concat_Created = "open" (incomplete)
5. **Event Sequence** - Sorted by Event_Number

---

## TABLE 7: HOST INTAKE
**Status:** Child/Related table | **Source:** Host_Intake sheet
**Row Count:** 28 intake forms
**Primary Field:** Intake_ID

### Fields

| Field Name | Airtable Type | Source Column | Required | Notes |
|---|---|---|---|---|
| **Intake_ID** | Single line text | Intake_ID | Yes | Format: HIF-XXX (e.g., HIF-001) |
| **Venue** | Link to Venues | Venue_ID | No | Foreign key to Venues table (19/28 populated; note: 9 unmatched) |
| **Organization Name** | Single line text | Org_Name | Yes | Official organization name (28/28 populated) |
| **Submission Timestamp** | Date | Timestamp | No | Form submission datetime (16/28 populated) |
| **Contact Name** | Single line text | Contact_Name | Yes | Primary contact person (18/28 populated) |
| **Contact Email** | Email | Contact_Email | No | Contact email address (19/28 populated) |
| **Region** | Single select | Region | No | Geographic region (20/28 populated) |
| **Frontline Community** | Checkbox | Frontline_Community | No | Serves frontline/environmental justice communities (18/28 populated) |
| **Film Topic Preference 1** | Single line text | Film_Topic_1 | No | Primary film topic interest (16/28 populated) |
| **Film Topic Preference 2** | Single line text | Film_Topic_2 | No | Secondary film topic interest (16/28 populated) |
| **Film Selection Notes** | Long text | Film_Notes | No | Specific requests/preferences (6/28 populated) |
| **Venue Address** | Single line text | Venue_Address | No | Full venue/facility address (16/28 populated) |
| **Has Projector** | Checkbox | Has_Projector | No | Equipment: Projector (11/28 populated) |
| **Has Sound System** | Checkbox | Has_Sound | No | Equipment: Sound system (14/28 populated) |
| **Has Screen** | Checkbox | Has_Screen | No | Equipment: Projection screen (13/28 populated) |
| **Has Computer** | Checkbox | Has_Computer | No | Equipment: Computer/laptop (13/28 populated) |
| **Has WiFi** | Checkbox | Has_WiFi | No | Equipment: WiFi internet (14/28 populated) |
| **Has AV Technical Lead** | Checkbox | Has_AV_Lead | No | Equipment: Technical support person (12/28 populated) |
| **Has Wheelchair Access** | Checkbox | Has_Wheelchair | No | Accessibility: Wheelchair accessible (15/28 populated) |
| **Capacity 60+ Seating** | Checkbox | Cap_60plus | No | Capacity: 60+ person capacity (14/28 populated) |
| **Space & Logistics Notes** | Long text | Space_Notes | No | Venue setup, hybrid capability notes (8/28 populated) |
| **Promotion Channels** | Long text | Promo_Channels | No | Comma-separated list of marketing channels (16/28 populated) |
| **Promotion Strategy Notes** | Long text | Promo_Notes | No | Custom promotion approach (13/28 populated) |
| **Host Meeting Attended** | Checkbox | Host_Meeting | No | Attended pre-event meeting (16/28 populated) |
| **Motivation/Why OEFF** | Long text | Motivation | No | Organization's interest in festival (16/28 populated) |
| **Additional Comments** | Long text | Additional | No | Any other notes (13/28 populated) |

### Linked Records
- **Venue** → Venues table (optional; 9 unmatched intakes need manual linking)

### Suggested Views
1. **2026 Intakes** - All 28 current intake forms
2. **Unmatched Venues** - Filter Venue empty (9 records)
3. **Equipment Ready** - Filter Has_Projector, Has_Sound, Has_Screen all checked
4. **Accessibility Compliant** - Filter Has_Wheelchair = Yes, Cap_60plus = Yes
5. **Frontline Communities** - Filter Frontline_Community = Yes
6. **By Region** - Grouped by Region
7. **Incomplete Forms** - Filter for multiple empty fields
8. **Action Items** - Unmatched venues need Venue_ID assignment

---

## TABLE 8: PARTICIPANTS
**Status:** Child/Related table | **Source:** Participants sheet
**Row Count:** 132 participants
**Primary Field:** Participant_ID

### Fields

| Field Name | Airtable Type | Source Column | Required | Notes |
|---|---|---|---|---|
| **Participant_ID** | Single line text | Participant_ID | Yes | Format: Pxx-XXX (e.g., P25-001; all from 2025) |
| **Name** | Single line text | Name | Yes | Full name (132/132 populated) |
| **Role** | Single select | Role | No | Filmmaker-virt, Staff, Volunteer, Speaker, Judge, etc. (40/132 populated) |
| **Email** | Email | Email | Yes | Email address (115/132 populated) |
| **Event/Film** | Single line text | Event_Film | Yes | Event or film name (132/132 populated, mostly "Launch Party") |
| **Year** | Number | Year | Yes | Festival year (132/132 = 2025) |
| **Honorarium** | Currency | Honorarium | No | Payment amount (0/132 - to be populated) |

### Linked Records
- **Event** → Events table (optional, link via Event_Film name + Year)

### Suggested Views
1. **2025 Participants** - All records filtered to Year=2025
2. **By Role** - Grouped by Role
3. **Filmmakers** - Filter Role contains "Filmmaker"
4. **Missing Email** - Filter Email empty
5. **Pending Honorarium** - Filter Honorarium empty
6. **Contact Directory** - Show Name, Email, Role

---

## TABLE 9: RECORDINGS
**Status:** Child/Related table | **Source:** Recordings sheet
**Row Count:** 62 recording links
**Primary Field:** Recording_ID

### Fields

| Field Name | Airtable Type | Source Column | Required | Notes |
|---|---|---|---|---|
| **Recording_ID** | Single line text | Recording_ID | Yes | Format: Rxx-XXX (e.g., R25-001; all from 2025) |
| **Event** | Single line text | Event | Yes | Event name/description (62/62 populated) |
| **Year** | Number | Year | Yes | Festival year (62/62 = 2025) |
| **Recap URL** | URL | Recap_URL | No | Short highlight reel link (17/62 populated; vimeo.com) |
| **Full Event URL** | URL | Full_URL | No | Full event recording link (8/62 populated; vimeo review links) |

### Linked Records
- **Event** → Events table (optional, link via Event name + Year)

### Suggested Views
1. **2025 Recordings** - All records
2. **With Recap** - Filter Recap_URL not empty (17 records)
3. **Full Recording Available** - Filter Full_URL not empty (8 records)
4. **Missing Links** - Filter both URLs empty (35+ records)
5. **By Event** - Grouped by Event

---

## TABLE 10: SPONSORS & BENEFITS
**Status:** Reference/Tracking table | **Source:** Benefits Tracking 2026.xlsx - FY26 Sponsors & Benefits sheets
**Row Count:** 23 sponsors
**Primary Field:** Sponsor_ID (to be created)

### Fields

| Field Name | Airtable Type | Source Column | Required | Notes |
|---|---|---|---|---|
| **Sponsor_ID** | Single line text | [AUTO] | Yes | Format: SPN-XXX (auto-generated) |
| **Sponsor Name** | Single line text | Sponsor Name | Yes | Legal organization name (23/23 populated) |
| **Sponsor Level** | Single select | Sponsor Level | Yes | Presenting, Growing, Supporting, Tabling/Nonprofit (23/23 populated) |
| **Commitment Date** | Date | Committed Date | Yes | Date committed (23/23 populated; format: MM.DD.YY) |
| **Tagline/Featurette Status** | Single select | Tagline or Featurette | No | Opted Out, Requested, Submitted (15/23 populated) |
| **Website** | URL | Website | Yes | Organization website (23/23 populated) |
| **Contact Email** | Email | [DERIVED] | No | Primary contact (to extract from notes if needed) |

### Benefits Matrix (Nested/Rollup fields or separate junction table)

Benefits are offered based on Sponsor Level. Create lookup/rollup fields OR separate Benefits Tracking table:

#### Major Benefits (Most commonly fulfilled)
- **Logo on OEFF Website** - Checkbox (23/23 populated)
- **Recognition on Social Media** - Single select (23/23 populated: "1 Individual Branded Post", "1 Branded Post")
- **Logo & Link on OEFF Sponsor Page** - Checkbox (21/23 filled)
- **Social Recognition Post (Nov 2025)** - Checkbox (8/23)
- **E-Newsletter Feature (Month Selection)** - Single line text (20/23: "Requested" or Month)
- **Donor Preview Party Tickets** - Number (23/23: 2-5 tickets)
- **Launch Party Tickets** - Number (23/23: 2-4 tickets)

#### Media & Promotional Benefits
- **Full Page Program Guide Ad** - Checkbox (0/23)
- **Logo on Printed Bookmark** - Checkbox (1/23)
- **Branded Sponsor Spotlight on Website** - Checkbox (0/23)
- **Recognition in Pre-Fest Promo Video** - Checkbox (0/23)
- **Recognition in Fest Week Video** - Checkbox (1/23)

#### Event Presence
- **Presented By Slot + Tabling** - Checkbox (4/23)
- **Tabling at Launch Party** - Checkbox (1/23)
- **Action Fair Screening Remarks** - Checkbox (0/23)
- **Launch Party Verbal Recognition by MC** - Checkbox (2/23)

#### Premium/Partnership Benefits
- **Sponsors-Only Group Tour (OEC)** - Checkbox (4/23)
- **Educational Program (Speaker or Screening)** - Checkbox (0/23)
- **Team Building Volunteer Opportunity** - Checkbox (0/23)
- **Early OEFF Ticket Presale** - Checkbox (23/23: all False)

### Linked Records
- **Events** → Events table (optional, for sponsor-related events)

### Suggested Views
1. **By Sponsorship Level** - Grouped by Sponsor Level
2. **Fulfilled Benefits** - Show benefit completion status
3. **Commitment Timeline** - Sorted by Commitment Date
4. **Website Links** - Show Name & Website URLs
5. **Activation Checklist** - Filter by missing benefits

---

## TABLE 11: PARTNERS
**Status:** Reference/Organization table | **Source:** Partners sheet
**Row Count:** 150 organizations
**Primary Field:** Partner_ID

### Fields

| Field Name | Airtable Type | Source Column | Required | Notes |
|---|---|---|---|---|
| **Partner_ID** | Single line text | Partner_ID | Yes | Format: ORG-XXX (e.g., ORG-001) |
| **Organization Name** | Single line text | Org_Name | Yes | Name of partner organization (150/150 populated) |
| **Contact Person** | Single line text | Contact | No | Primary contact name (29/150 populated) |
| **Email** | Email | Email | No | Contact email (6/150 populated; note: many stored in Contact field) |
| **Topic Focus** | Long text | Topics | No | Environmental topics or mission (4/150 populated) |
| **Notes** | Long text | Notes | No | Relationship, collaboration details (0/150 - mostly empty) |
| **Relationship Status** | Single select | [DERIVED] | No | Active, Inactive, Prospect (auto-assign) |

### Linked Records
- **Events** → Events table (optional, for co-hosted events)
- **Sponsors** → Sponsors table (optional, some partners are also sponsors)

### Suggested Views
1. **All Partners** - Complete organization list
2. **With Contact Info** - Filter Contact or Email not empty
3. **By Topic** - Grouped by Topic Focus
4. **Data Gaps** - Filter Contact or Email empty (many records)
5. **Contact Directory** - Show Org Name, Contact, Email

---

## OPTIONAL TABLE 12: FESTIVAL METRICS & REPORTING
**Status:** Reporting/Analysis table | **Source:** Festival_Metrics sheet
**Row Count:** 110 event metrics
**Primary Field:** Metric_ID (to be created)

### Fields

| Field Name | Airtable Type | Source Column | Required | Notes |
|---|---|---|---|---|
| **Metric_ID** | Single line text | [AUTO] | Yes | Format: MET-XXX |
| **Year** | Number | Year | Yes | Festival year (110/110 = 2025) |
| **Event Name** | Single line text | Event | Yes | Event description (110/110 populated) |
| **Date** | Date | Date | No | Event date (89/110 populated) |
| **Registrations** | Number | Registrations | No | Registered attendees (93/110 populated) |
| **Walk-In Attendees** | Number | Walk_Ins | No | Walk-in attendance (14/110 populated) |
| **Total Attendance** | Formula | [DERIVED] | No | Registrations + Walk_Ins |
| **Notes** | Long text | Notes | No | Event-specific notes (0/110 - to be populated) |

### Linked Records
- **Event** → Events table (optional, link by Year + Event name)

### Suggested Views
1. **2025 Metrics** - All 110 records
2. **Attendance Dashboard** - Show Event, Registrations, Walk_Ins, Total
3. **High Attendance** - Filter Total_Attendance > median
4. **Incomplete Data** - Filter Registrations or Walk_Ins empty
5. **By Month** - Grouped by Date month

---

## REFERENCE/ARCHIVE TABLES (Separate Archive Base - Optional)

These sheets from 2024-2025 should be migrated to a separate "OEFF Archive 2024-2025" base OR maintained as views in the primary base:

### Archive Tables (Low Priority for Active Base)

1. **2025_Schedule** (133 rows) - View of 2025 events
2. **2025_Host_Venues** (333 rows) - Venue-Event junction data
3. **2026_Host_Venues** (369 rows) - 2026 Venue-Event planning data
4. **2025_Programs** (105 rows) - Program guide data
5. **2024_Programs** (63 rows) - 2024 Program archive
6. **2025_Honoraria** (93 rows) - 2025 Payment records
7. **2024_Honoraria** (47 rows) - 2024 Payment archive
8. **2025_Final_Data** (41 rows) - 2025 Season summary
9. **2024_Final_Data** (279 rows) - 2024 Season summary
10. **2025_Festival_Recordings** (57 rows) - 2025 Recording archive
11. **2024_Festival_Recordings** (70 rows) - 2024 Recording archive
12. **2025_License_Invoice** (15 rows) - License/invoice reference

### Documentation Tables (Reference Base)

1. **Schema_Guide** (137 rows) - Data dictionary
2. **Color_Legend** (24 rows) - Status/field legend
3. **Film_Gap_Analysis** (24 rows) - Analysis document
4. **Matching_Worksheet** (20 rows) - Unmatched intake forms

### Brainstorm/Planning (Optional)

1. **Programming_Ideas** (228 rows) - From Progr+PartnerIdeas
2. **Partner_Ideas** (42 rows) - From ProgPartners

---

## DATA MIGRATION STRATEGY

### Phase 1: Core Tables (Foundation)
1. Import **Venues** (100 rows)
2. Import **Films_2026** (12 rows)
3. Create **Events** table (combine Events_2026 + Events_2025 + Events_2024 with Year field)
4. Create links between Events → Venues → Films

### Phase 2: Related Records
5. Import **Film Contacts** (9 rows)
6. Import **Event Media** (25 rows)
7. Import **Packet QA** (23 rows)
8. Import **Host Intake** (28 rows)
9. Import **Participants** (132 rows)
10. Import **Recordings** (62 rows)
11. Create linkages to Events table

### Phase 3: Reference/Master Data
12. Import **Sponsors** (23 rows) from Benefits Tracking
13. Import **Partners** (150 rows)
14. Import **Festival Metrics** (110 rows)

### Phase 4: Optional/Archive
15. Create separate Archive Base for 2024-2025 historical data
16. Maintain dashboards and documentation

---

## CRITICAL MIGRATION NOTES

### Data Quality Issues to Address

1. **Events with Missing Film_ID (2026):** 19 of 31 events missing film linkage
   - Action: Manual review and assignment needed
   - Cross-reference Film_Title with Films_2026 lineup

2. **Host Intake Unmatched Venues (9 unmatched):** 
   - See "Matching" worksheet for unmatched intake forms
   - Need to either assign Venue_ID or create new venues
   - Status: Documented in Matching sheet

3. **Dates Missing:**
   - 2026 Events: 17 of 31 missing dates (TBD)
   - 2025 Events: 124 of 180 missing dates
   - 2024 Events: 1 of 8 missing dates
   - Strategy: Keep dates optional; filter "scheduled" vs "planned"

4. **Capacity Field Issues:**
   - Mixed data types: numbers (260, 120) vs text ("TBD")
   - Strategy: Normalize to Number field, use NULL for TBD

5. **Contact Fields:** 
   - Host_Intake Contact_Email: 9 missing (32%)
   - Participants Email: 17 missing (13%)
   - Strategy: Flag for outreach/completion

6. **Phone Formats in Film Contacts:**
   - Mixed formats: "+447753571921", "7736201921", "803-414-8335"
   - Strategy: Use Airtable Phone field (auto-formats)

7. **Empty Columns to Be Populated:**
   - Films_2026: Trailer_Link, Caption_Status, Audio_Description, Spanish_Available (all 0/12)
   - Events_2026: OEFF_Rep, Host_Fee fields, License_Status (all 0/31)
   - Event_Media: Feature_Link, English_Subs, Spanish_Subs, Dropbox_Link (all 0/25)
   - Strategy: Mark as "to be populated" in setup, create views for incomplete data

8. **Column K Film Title + Status Combined (2026HostVenues):**
   - Current format: `"Film Name (CONFIRMED)"` or `"Film Name (NOT CONFIRMED)"`
   - Action: Parse into separate Film_Title and Film_Status fields during import
   - Regex pattern: `(.+?)\s*\(([^)]+)\)\s*$` → group 1 = title, group 2 = status
   - Map: "CONFIRMED" → Confirmed, "NOT CONFIRMED" → Not Confirmed

9. **Column A Event Tier + Inline Notes Combined (2026HostVenues):**
   - Current format: `"FLAGSHIP"`, `"COMMUNITY"`, or `"FLAGSHIP\n*Need OEC laptop..."`
   - Action: Extract tier keyword to Event_Tier field, move inline notes to Events.Notes
   - Standardize to: Flagship, Community, Community/Hybrid Stream

10. **Host Fee Column Labels Say "2025" on 2026 Sheet:**
    - Columns V–AB in 2026HostVenues are labeled "Host Fee 2025 Ask", etc.
    - Likely a header carryover — verify with Ana whether these are 2025 actuals or 2026 planning figures
    - Action: Confirm year intent before importing values

11. **Capacity Field Continues to Have Mixed Types (2026HostVenues):**
    - New non-numeric values found: `"Check last yr HH"`, `"Check email thread"`, `"120?"`
    - Action: Resolve to numbers or NULL before import. Move uncertainty notes to Venues.Notes

### Field Normalization Recommendations

| Issue | Current | Recommended Airtable Type |
|---|---|---|
| Capacity (mixed) | "260", "TBD", "120" | Number (nullable) |
| Timestamp | "2026-01-26 18:01:49" | Date field |
| Time (various) | "6-9P", "6:30P", "6-9P\n*Doors open 5:30P" | Single line text |
| Topics (comma-separated) | "Wildlife, Conservation" | Multiple select OR rollup from Films |
| Promotion Channels | "eNewsletter, Social Media, ..." | Multiple select |
| Region | "Chicago Central (Downtown, Loop)" | Single select (standardize) |
| Tech Tier | "T1", "T2" | Single select |
| Equipment checkmarks | "✓" | Checkbox (convert ✓ to TRUE) |
| URLs (mixed) | "https://example.com", "Film website" | URL field |
| Email (concatenated) | "John Doe <john@example.com>, Org" | Separate Email field |
| Film+Status combined | "Rooted (CONFIRMED)" | Split to Film_Title + Film_Status |
| Event tier + notes | "FLAGSHIP\n*Need laptop..." | Split to Event_Tier (single select) + Notes |
| Ticket pricing (varied) | "Free", "$75 ea or two for $150" | Single line text (too varied for number) |
| Host fee year labels | "Host Fee 2025 Ask" on 2026 sheet | Verify year, rename to current season |

### Linking Strategy

**Primary Keys to Maintain:**
- Venue_ID (V-001 to V-100)
- Film_ID (F26-001 to F26-012)
- Event_ID (E26-001, E25-001, E24-001)
- Contact_ID (FC26-001 to FC26-009)
- Participant_ID (P25-001 to P25-132)
- Intake_ID (HIF-001 to HIF-028)
- Media_ID (M26-001 to M26-025)
- Packet_ID (PKT-001 to PKT-023)
- Recording_ID (R25-001 to R25-062)
- Partner_ID (ORG-001 to ORG-150)

**Linking Priority (Required):**
1. Events → Venues (Event.Venue_ID → Venue.Venue_ID)
2. Events → Films (Event.Film_ID → Film.Film_ID) [2026 only; some TBD]
3. Film_Contacts → Films (Contact.Film_ID → Film.Film_ID)
4. Host_Intake → Venues (Intake.Venue_ID → Venue.Venue_ID) [19/28 populated; 9 need matching]

**Linking Optional (Recommended for Reports):**
- Participants → Events (via Event_Film name + Year)
- Recordings → Events (via Event name + Year)
- Event_Media → Events (via Event Name + Date)
- Packet_QA → Events (via Event_Num or film name)
- Festival_Metrics → Events (via Event name + Year)

---

## VIEWS STRATEGY

### Primary Base Views (11 Tables)

**Venues Table Views:**
- Active 2026 Venues
- By Region (grouped)
- By Tech Tier (grouped)
- Data Gaps (incomplete records)

**Films Table Views:**
- 2026 Lineup (all)
- By Topic (grouped)
- Missing Assets (incomplete)
- Intake Status Dashboard

**Events Table Views:**
- 2026 Calendar (by date)
- 2025 Archive
- 2024 Archive
- Status Board (by Pipeline Status)
- By Venue (grouped)
- Upcoming Events
- Host Fees Due
- Licensing Needed

**Film_Contacts Table Views:**
- All 2026 Contacts
- By Role (grouped)
- Format Ready Status
- Contact Directory

**Event_Media Table Views:**
- By Event (grouped)
- Missing Links (empty URLs)
- Ready for Distribution

**Packet_QA Table Views:**
- QA Status Board
- To Do Items
- Concat Status
- Event Sequence

**Host_Intake Table Views:**
- Unmatched Venues (action items)
- Equipment Ready
- Accessibility Compliant
- By Region (grouped)
- Frontline Communities

**Participants Table Views:**
- By Role (grouped)
- Filmmakers Only
- Contact Directory
- Pending Honorarium

**Recordings Table Views:**
- With Recap Available
- Full Recording Available
- Missing Links
- By Event (grouped)

**Sponsors Table Views:**
- By Sponsorship Level (grouped)
- Benefits Fulfilled (checklist)
- Commitment Timeline
- Activation Checklist

**Partners Table Views:**
- Contact Directory
- By Topic (grouped)
- Data Gaps (missing contact)

---

## AUTOMATION & FORMULAS

### Recommended Automations

1. **Event Year** (Formula on Events table):
   ```
   VALUE(LEFT({Event_ID}, 2)) + 2000
   ```

2. **Event Status Auto-Update** (Automation):
   - IF Linked to Film AND Date is today → Status = "Happening Now"
   - IF Date is past → Status = "Completed"
   - IF Date is future → Status = "Scheduled"

3. **Host Intake Venue Matching** (Manual but flagged):
   - Create view showing Intake_ID, Org_Name, Suggested Venue
   - Flag records with empty Venue_ID for manual assignment

4. **Total Attendance** (Formula on Festival_Metrics):
   ```
   {Registrations} + {Walk_Ins}
   ```

5. **Capacity Utilization** (Formula on Events, if available):
   ```
   IF({Venue},[Total_Attendance], {Capacity}), 0)
   ```

---

## IMPLEMENTATION CHECKLIST

**Pre-Migration:**
- [ ] Audit all 100 venues for duplicates
- [ ] Verify 23 sponsors in Benefits Tracking match Partners list
- [ ] Identify which Participants are staff vs. external
- [ ] Confirm 9 unmatched Host_Intake forms assignment strategy
- [ ] Standardize Region field values (6 unique regions)
- [ ] Standardize Event_Type field values

**Migration Phase 1 (Core):**
- [ ] Create Venues table, import 100 rows
- [ ] Create Films table, import 12 rows
- [ ] Create Events table, combine 3 event sheets + Year field
- [ ] Set up Venue-Event links
- [ ] Set up Film-Event links

**Migration Phase 2 (Related):**
- [ ] Create Film_Contacts table, import 9 rows
- [ ] Create Event_Media table, import 25 rows
- [ ] Create Packet_QA table, import 23 rows
- [ ] Create Host_Intake table, import 28 rows
- [ ] Create Participants table, import 132 rows
- [ ] Create Recordings table, import 62 rows
- [ ] Link all tables to Events

**Migration Phase 3 (Reference):**
- [ ] Create Sponsors table, import 23 rows
- [ ] Create Partners table, import 150 rows
- [ ] Create Festival_Metrics table, import 110 rows

**Post-Migration:**
- [ ] Test all linkages
- [ ] Create all recommended views
- [ ] Set up field-level permissions
- [ ] Configure automations
- [ ] Train team on base structure
- [ ] Document field assumptions
- [ ] Plan archival strategy for 2024-2025 data

---

## ESTIMATED RECORD COUNTS BY TABLE

| Table | Records | Status |
|---|---|---|
| Venues | 100 | Stable |
| Films | 12 | Growing (2026 season) |
| Events | 219 | Historical archive (31 2026, 180 2025, 8 2024) |
| Film_Contacts | 9 | Stable |
| Event_Media | 25 | Archive (2025) |
| Packet_QA | 23 | Archive (2025) |
| Host_Intake | 28 | Current (2026 recruitment) |
| Participants | 132 | Historical (2025) |
| Recordings | 62 | Archive (2025) |
| Sponsors | 23 | Current (FY26) |
| Partners | 150 | Reference (needs cleanup) |
| Festival_Metrics | 110 | Archive (2025) |
| **TOTAL** | **893** | Core + Reference |

---

## SCHEMA VERSION

**Version:** 1.1 (2026HostVenues Compliance Update)
**Date:** February 11, 2026
**Based on:** V7-with-Dashboard.xlsx (33 sheets) + Benefits Tracking 2026.xlsx + ACTIVE_Roadmap OEFF2026Films-Schedule-Programs.xlsx (2026HostVenues sheet)
**Changes in 1.1:**
- Added 14 fields to Events table: Event Tier, Ticket Price, Film Survey Complete, Host Fee Invoice Amount/Info/Sent/Reminder/Payment Received, Licensing Request Status, Film License Amount/Contact, License Invoice Received/Paid, Volunteer Needs
- Added Previous Contacts field to Venues table
- Expanded Host Fee Status options (Pending → Invoiced → Reminded → Paid)
- Added Film Status option "Not Confirmed" (parsed from spreadsheet notation)
- Added 4 new suggested views: By Event Tier, Host Fee Invoice Tracker, Licensing Pipeline, Volunteer Planning
- Added 4 new data quality issues (#8–11): column K parsing, column A splitting, host fee year labels, capacity mixed types
- Added 4 new field normalization entries
**Next Review:** After Phase 1 migration complete

