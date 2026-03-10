# Audit Results: Urgent Host Helper Data Gaps

**Run date:** 2026-03-09
**Sources checked:** Airtable CSV exports (Feb 6), roadmap JSON (Feb 24), roadmap venue contacts CSV, host intake form responses, eventbrite-state.json, **2025 Host Helper sheets (14 returning venues via Sheets API)**. Not checked: Airtable live tables (no API call).

---

## 1. Host Contact Info (name, email, cell) for all 22 scheduled venues

**Bottom line: 21 of 22 venues have a name + email somewhere. 7 venues have cell numbers (recovered from 2025 sheets). Only CAM has zero contact info. Several venues have DIFFERENT contacts between 2025 and 2026 — all 2025 data is flagged NEEDS VERIFICATION.**

| # | Venue | 2026 Contact (intake/roadmap) | 2025 Contact (Host Helper) | Cell (2025) | AV Contact (2025) | Flags |
|---|-------|-------------------------------|---------------------------|-------------|-------------------|-------|
| 1 | Columbia College | Michelle Yates, myates@colum.edu | *No 2025 sheet* | — | — | New host for 2025+ cycle |
| 2 | Trinity Lutheran | John Stoffregen, Jstoff304@gmail.com | *No 2025 sheet* | — | — | May have older helpers |
| 3 | Uncommon Ground | Michael Cameron (intake email field = street address) | Michael Cameron, Helen Cameron, Tara Honeywell, Isaac Rodriguez | — | Isaac Rodriguez, Bookings@uncommonground.com | (NEEDS VERIFICATION) 4 contacts in 2025 — confirm who's primary for 2026 |
| 4 | Climate Action Evanston | Jack Jordan, jjordan@climateactionevanston.org | *No 2025 sheet found* | — | — | Hosted in 2025 but no helper sheet found by name |
| 5 | Village of Oak Park | Lindsey Nieratka, LNieratka@oak-park.us | **Nalini Johnson**, nalini.johnson@oak-park.us | **(224) 598-4728** | **Joe Kreml**, jkreml@oak-park.us | (NEEDS VERIFICATION) **Different primary contact in 2025 vs 2026.** Lindsey is CSO, Nalini was event lead. Confirm who's primary. |
| 6 | ICA | Rory Gilchrist (name only in intake) | **Rory Gilchrist, rgilchrist@ica-usa.org** | **505-577-2055** | Rory (same person) | (NEEDS VERIFICATION) **2025 sheet fills the gap** — email + cell recovered. Rory handles everything there. |
| 7 | Triton College | Benjamin Kadlec, benjaminkadlec@triton.edu | Benjamin Kadlec, same email | **708-714-1116** (office: 708-456-0300 x3189) | **Maria Correa**, mariacorrea@triton.edu | (NEEDS VERIFICATION) Same primary, cell recovered. Verify Maria still AV. |
| 8 | Bethel New Life | Sharif Walker, aniki@bethelnewlife.org | **Tyanna Powell**, tyanna@bethelnewlife.org; **Marcia Kay**, mkay@bethelnewlife.org | **312-218-3320** (Tyanna); work 773-473-7884 | *None* — "OEFF Tech Team onsite" was plan | (NEEDS VERIFICATION) **Different people in 2024 vs 2026.** Sharif/Aniki/Trenton are 2026 contacts. Tyanna/Marcia were 2024. Confirm who's current. |
| 9 | IIT Bronzeville | *None in 2026 sources* | **Syda Taylor**, syda@organiconeness.org; **Alicia Bunton**, abunton1@iit.edu | **312-371-7036** (Syda) | **Alicia Bunton**, abunton1@iit.edu | (NEEDS VERIFICATION) **2025 sheet fills the gap entirely.** Organic Oneness + IIT partnership. Confirm both still involved. |
| 10 | Go Green Park Ridge | Johnny Patney + others from intake | **Mark Kleinschmit**, markkleiny@gmail.com | — | Mark Kleinschmit (same person) | (NEEDS VERIFICATION) Intake has Johnny Patney as submitter, 2025 sheet has Mark Kleinschmit for all roles. Confirm primary. |
| 11 | CAM | **—** | **—** | **—** | **—** | **ONLY venue with zero contact in any source. New partnership for 2026.** |
| 12 | Euclid Ave UMC | Joshua White, whitey1600@gmail.com | *No 2025 sheet* | — | — | New venue |
| 13 | Cultivate/AGC | Kris De la Torre, kris@cultivate-collective.org | Kris de la Torre, kdelatorre@agcchicago.org | **9159291061** or **205-578-9027** | **Farzad Farrokhnia**, farz@cultivate-collective.org | (NEEDS VERIFICATION) **Two different emails for Kris** — 2026 intake uses cultivate-collective.org, 2025 sheet uses agcchicago.org. Both likely work. Cell + AV contact recovered. |
| 14 | BUILD Chicago | Kesiah Bascom, kesiahbascom@buildchicago.org | Kesiah Bascom + Kenyana Walker, kenyanawalker@buildchicago.org | — | *Empty* — never filled in | (NEEDS VERIFICATION) Medical leave noted in intake. 2025 marketing contact: Daniel Perez, danielperez@buildchicago.org |
| 15 | Broadway UMC | Richard Alton, richard.alton@gmail.com | Richard Alton, same | — | **Woo Evans**, woodolla2004@gmail.com | (NEEDS VERIFICATION) Same primary. Marketing: Alexia Riveria, bumclakeview@gmail.com, ph: 773-348-2679 |
| 16 | Calumet College | Monica Puente, mpuente1@ccsj.edu | Monica Puente + **Brian Lowry**, blowry@ccsj.edu | — | Monica Puente (same as main) | (NEEDS VERIFICATION) Same primary. Brian Lowry is additional contact from 2025. |
| 17 | Kehrein Center | *Intake placeholder only* | **janelle@kcachicago.org, reesheda@kcachicago.org** | — | *Empty* | (NEEDS VERIFICATION) **2025 sheet fills the gap.** Janelle and Reesheda were 2025 contacts. Confirm still active for 2026. |
| 18 | BGE/Patagonia | Frances Crable, BGE.chicago773@gmail.com | *No 2025 sheet* | — | — | New venue |
| 19 | Epiphany Center | *Intake placeholder only* | **Drew Jensen**, drew@epiphanychi.com; **Jordyn**, jordyn@epiphanychi.com; **Tatianna Santiago**, tatianna@epiphanychi.com | — | Drew/Jordyn/Tatianna (same team) | (NEEDS VERIFICATION) **2025 sheet fills the gap.** Three contacts at Epiphany. Confirm still the right people. |
| 20 | Chicago Cultural Center | *None in 2026 sources* | **Alex Vazquez**, Jose.Vazquez2@cityofchicago.org; **Natalia Salazar**, Natalia.Salazar@cityofchicago.org | **970.214.8222** (Alex); **773.485.1086** (Natalia) | Alex Vazquez (same) | (NEEDS VERIFICATION) **2025 sheet fills the gap entirely.** City of Chicago staff — confirm still assigned to CCC events. |
| 21 | Dominican University | Maria Pascarella, mpascarella@dom.edu | **Christine Wilson**, cwilson2@dom.edu | — | **Hannah Wald**, hwald@dom.edu | (NEEDS VERIFICATION) **Different primary contact.** 2026 intake = Maria Pascarella. 2025 helper = Christine Wilson. Both may be valid (different roles). |

### Summary after 2025 sheet recovery

- **Complete (name + email):** 21 of 22 venues (up from 16)
- **Cell phones recovered:** 7 venues (up from 0): Oak Park, ICA, Triton, Bethel, IIT Bronzeville, CCC, Cultivate/AGC
- **Zero contact:** 1 (CAM — truly new, needs outreach)
- **Venues where 2025 and 2026 contacts are DIFFERENT PEOPLE:** 4 (Oak Park, Bethel, Dominican, Go Green) — these need explicit verification
- **Venues where 2025 data is the ONLY source:** 4 (IIT Bronzeville, Kehrein Center, Epiphany, CCC) — these especially need verification

### Action needed

1. **CAM:** Only true gap. Need outreach to establish contact.
2. **Verify the 4 venues with contact changes:** Oak Park (Lindsey vs Nalini), Bethel (Sharif vs Tyanna), Dominican (Maria vs Christine), Go Green (Johnny vs Mark). Which person is the 2026 point of contact?
3. **Verify the 4 venues where 2025 data is the only source:** IIT Bronzeville (Syda/Alicia), Kehrein (Janelle/Reesheda), Epiphany (Drew/Jordyn/Tatianna), CCC (Alex/Natalia). Confirm they're still involved.
4. **Cell numbers still missing for 15 venues.** Add cell to a future touchpoint (host confirmation form or direct ask).

---

## 2. Film Runtimes

**Bottom line: ZERO runtimes exist in any local data source.**

| Film | Runtime | Source |
|------|---------|--------|
| Reasons for Hope: Dr. Jane Goodall | — | Not in Films CSV, not in roadmap |
| Beyond Zero | — | Not in Films CSV, not in roadmap |
| Plastic People | — | Not in Films CSV, not in roadmap |
| Drowned Land | — | Not in Films CSV, not in roadmap |
| How to Power a City | — | Not in Films CSV, not in roadmap |
| Rooted | — | Not in Films CSV, not in roadmap |
| Chasing Time | — | **Not even in Films CSV** (no F26 record) |
| Planetwalker | — | Part of F26-007 (Oscar Shorts composite) |
| 40 Acres | — | Not in Films CSV, not in roadmap |
| Young Filmmakers Winner Shorts | — | Variable (depends on winners) |
| From Rails to Trails | — | Not in Films CSV, not in roadmap |
| In Our Nature | — | Not in Films CSV, not in roadmap |
| Whose Water? | — | Not in Films CSV, not in roadmap |

### What's going on

The Films CSV (`02-films.csv`) has these columns: Film ID, Film Title, Release Year, Primary/Secondary/Tertiary Topic, Marginalized Voices, Film Website, Trailer Link, Caption Status, Audio Description, Spanish Available, Intake Received, Notes. **There is no runtime column.**

The Film Website and Trailer Link columns contain placeholder text ("Film website") — not actual URLs.

The roadmap JSON has no runtime field in its column headers.

### Where runtimes might actually be

1. **Airtable Films table (live)** — May have a runtime field that wasn't in the Feb 6 export. Worth checking via API.
2. **Film intake survey responses** — If filmmakers submitted runtimes, those might be in Airtable but not in the CSV export.
3. **Film websites** — The actual film websites (not the placeholder text) would list runtimes. This requires manual lookup or web scraping.
4. **Chasing Time** has no Films table record at all — it needs to be added.

### Action needed

This is a **complete gap** in local data. Runtimes must be sourced from filmmaker submissions (check Airtable live) or looked up manually from film distributor/festival pages. This blocks run-of-show computation for every venue.

---

## 3. Eventbrite Event URLs (remaining 8 of 22)

**Bottom line: 14 events published (all unlisted/preview). 8 events not yet created.**

### Published (14 events)

| Event | Venue | Film | Eventbrite ID | Status |
|-------|-------|------|---------------|--------|
| row_2 | Columbia College | Reasons for Hope | 1983830318887 | Published, unlisted |
| row_3 | Trinity Lutheran | Beyond Zero | 1983830320893 | Published, unlisted |
| row_4 | Climate Action Evanston | Plastic People | 1983830336941 | Published, unlisted |
| row_5 | Uncommon Ground | TBD Film | 1983830338947 | Published, unlisted — **film name needs update** |
| row_6 | Columbia College | Drowned Land | 1983830340953 | Published, unlisted |
| row_8 | Oak Park or ICA | How to Power a City | 1983830343962 | Published, unlisted |
| row_9 | Bethel New Life | Rooted | 1983830346971 | Published, unlisted |
| row_10 | Triton or ICA | How to Power a City | 1983830349980 | Published, unlisted |
| row_11 | Cultivate/AGC | Young Filmmakers | 1983830350983 | Published, unlisted |
| row_12 | Kehrein Center | 40 Acres | 1983830351986 | Published, unlisted |
| row_13 | BGE/Patagonia | 40 Acres | 1983830357001 | Published, unlisted |
| row_14 | Broadway UMC | Rails to Trails | 1983830359007 | Published, unlisted |
| row_17 | BUILD Chicago | Young Filmmakers | 1983830361013 | Published, unlisted |
| row_18 | Calumet College | Rails to Trails | 1983830362016 | Published, unlisted |

**Note:** The eventbrite-state.json maps venue names to venue IDs but doesn't explicitly link event rows to venue names. Row-to-venue mapping is inferred from film title + date matching against the roadmap.

### Not yet created (8 events)

| Venue | Date | Film | What's blocking |
|-------|------|------|-----------------|
| IIT Bronzeville | 4/24 | Rooted + Planetwalker | New venue — no contact info, no intake response |
| Go Green Park Ridge | 4/24 | Chasing Time + Planetwalker | Has contact, likely just not created yet |
| Chicago Climate Action Museum | 4/24 | Chasing Time + Planetwalker | New venue — no contact info |
| Euclid Ave UMC | 4/24 | Chasing Time + Planetwalker | Has contact, likely just not created yet |
| Epiphany Center | 4/25 | Whose Water? | **TENTATIVE** — film being confirmed |
| Chicago Cultural Center | 4/26 | In Our Nature | Has no contact in data, but is a known recurring venue |
| Dominican University | 4/27 | Rooted | Has contact, likely just not created yet |
| One of ICA/Triton | 4/24 | How to Power a City | 3 venues showing this film, only 2 Eventbrite events |

### Additional issue

- Uncommon Ground's Eventbrite event still says "TBD Film" — needs updating to "Beyond Zero" (confirmed on roadmap).

---

## 4. AV / Tech Contact per Venue

**Bottom line: 10 named AV contacts recovered from 2025 Host Helper sheets. All flagged (NEEDS VERIFICATION) — these are last year's contacts.**

| Venue | AV Contact (2025 sheet) | Email | Still current? | AV Equipment (2026 intake) |
|-------|------------------------|-------|----------------|---------------------------|
| Columbia College | *No 2025 sheet* | — | — | ✓ Projector, sound, screen (HIF-004) |
| Trinity Lutheran | *No 2025 sheet* | — | — | ✓ Projector, sound, screen (HIF-003) |
| Uncommon Ground | **Isaac Rodriguez** | Bookings@uncommonground.com | (NEEDS VERIFICATION) | ✓ Projector, sound, screen (HIF-008) |
| Climate Action Evanston | *No 2025 sheet found* | — | — | ✓ Projector, sound, screen (HIF-015) |
| Village of Oak Park | **Joe Kreml** | jkreml@oak-park.us | (NEEDS VERIFICATION) | ✓ Projector, sound, screen (HIF-009) |
| ICA | Rory Gilchrist (same as host) | rgilchrist@ica-usa.org | (NEEDS VERIFICATION) | No intake response |
| Triton College | **Maria Correa** | mariacorrea@triton.edu | (NEEDS VERIFICATION) | ✓ Projector, sound, screen (HIF-001) |
| Bethel New Life | *None* — 2024 plan was "OEFF Tech Team onsite" | — | (NEEDS VERIFICATION) | **No projector** (HIF-013) |
| IIT Bronzeville | **Alicia Bunton** | abunton1@iit.edu | (NEEDS VERIFICATION) | No intake response |
| Go Green Park Ridge | Mark Kleinschmit (same as host) | markkleiny@gmail.com | (NEEDS VERIFICATION) | **No AV equipment listed** (HIF-011) |
| CAM | — | — | — | No intake response |
| Euclid Ave UMC | *No 2025 sheet* | — | — | ✓ Projector, sound, screen (HIF-016) |
| Cultivate/AGC | **Farzad Farrokhnia** | farz@cultivate-collective.org | (NEEDS VERIFICATION) | **No projector**, has rolling screens + sound (HIF-007) |
| BUILD Chicago | *Empty in 2025 sheet* | — | — | **No projector** (HIF-005) |
| Broadway UMC | **Woo Evans** | woodolla2004@gmail.com | (NEEDS VERIFICATION) | ✓ Projector, sound, screen (HIF-006) |
| Calumet College | Monica Puente (same as host) | mpuente1@ccsj.edu | (NEEDS VERIFICATION) | No intake response |
| Kehrein Center | *Empty in 2025 sheet* | — | — | No intake response |
| BGE/Patagonia | *No 2025 sheet* | — | — | ✓ Projector, sound, screen (HIF-014) |
| Epiphany Center | Drew/Jordyn/Tatianna (same as host team) | drew@epiphanychi.com | (NEEDS VERIFICATION) | No intake response |
| CCC | **Alex Vazquez** | Jose.Vazquez2@cityofchicago.org | (NEEDS VERIFICATION) | No intake response |
| Dominican University | **Hannah Wald** | hwald@dom.edu | (NEEDS VERIFICATION) | ✓ Projector, sound, screen (HIF-002) |

### Summary after 2025 sheet recovery

- **Named AV contacts recovered:** 10 (up from 0)
- **Distinct AV contact (not same as host):** 7 — Isaac Rodriguez (Uncommon Ground), Joe Kreml (Oak Park), Maria Correa (Triton), Alicia Bunton (IIT), Farzad Farrokhnia (Cultivate), Woo Evans (Broadway), Hannah Wald (Dominican)
- **Still no AV contact anywhere:** 8 — Columbia, Trinity, Climate Action Evanston, CAM, Euclid, BUILD, Kehrein, BGE

### AV equipment flags (from 2026 intake)

Venues that will need OEFF-supplied equipment or a partner venue:
- **Bethel New Life:** No projector. 2024 plan was OEFF tech team onsite.
- **BUILD Chicago:** No projector. AV contact never filled in.
- **Go Green Park Ridge:** No AV equipment listed at all. Want theater venue.
- **Cultivate/AGC:** No projector, but has large rolling screens + sound.

---

## Overall Assessment

| Urgent Item | Before 2025 sheets | After 2025 sheets | What's still actually missing |
|-------------|--------------------|--------------------|-------------------------------|
| Host contacts (name + email) | 16 of 22 | **21 of 22** | Only CAM is truly missing. 4 venues need verification (different person in 2025 vs 2026). |
| Cell phones | 0 of 22 | **7 of 22** | 15 still missing. Intake form doesn't collect cell — add to a future touchpoint. |
| AV contacts (named) | 0 of 22 | **10 of 22** | 8 venues still have no AV contact anywhere. All 10 recovered are (NEEDS VERIFICATION). |
| Film runtimes | 0 of ~13 | **0 of ~13** | Complete gap. Not in any source. Needs Airtable live check or manual lookup. |
| Eventbrite URLs | 14 of 22 | 14 of 22 | 8 not created. ~5 just need creating; ~3 blocked on venue/contact gaps. |

### Recommended next steps (in priority order)

1. **Verify the 2025 contacts.** Send the (NEEDS VERIFICATION) list to Ana/Josh — they'll know who's current. This is the highest-leverage action: one email turns 10 stale AV contacts and 5 recovered host contacts into confirmed data.
2. **CAM contact.** Only venue with zero contact anywhere. Who is the relationship with?
3. **Check Airtable live** (via API) for runtime field and any contact fields not in the Feb 6 CSV export.
4. **Film runtimes.** Add a runtime field to the Films table. Source from film websites or filmmaker survey responses. This blocks run-of-show computation for every venue.
5. **Create missing Eventbrite events** for venues that have contacts and confirmed films (Go Green, Euclid, Dominican, CCC, and one of ICA/Triton).
6. **Add Chasing Time** to the Films table — it has no F26 record but is assigned to 3 venues.
