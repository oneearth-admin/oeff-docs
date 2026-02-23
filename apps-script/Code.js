/**
 * OEFF 2026 Host Venue Intake — Google Form Generator
 * Optimized for Airtable interop (Table 7: HOST INTAKE)
 *
 * HOW TO USE:
 * 1. Go to https://script.google.com
 * 2. Create a new project
 * 3. Paste this entire file into the editor
 * 4. Click Run → select createHostIntakeForm
 * 5. Authorize when prompted
 * 6. Check Execution Log for form URLs
 *
 * WHAT THIS CREATES:
 * - A Google Form with all intake fields
 * - A linked response Sheet with an auto-processor
 * - An "Airtable Ready" sheet that splits checkbox groups
 *   into individual boolean columns matching Table 7 schema
 *
 * AIRTABLE FIELD MAPPING:
 * Form responses auto-transform to match these Airtable fields:
 *   Intake_ID (HIF-XXX) — auto-generated
 *   Organization_Name, Venue_Address, Capacity
 *   Contact_Name, Contact_Email, Contact_Phone, Contact_Role
 *   Contact2_Name, Contact2_Email, Contact2_Phone, Contact2_Role
 *   AV_Contact_Name, AV_Contact_Email
 *   Marketing_Contact_Name, Marketing_Contact_Email
 *   Film_ID, Film_Title, Screening_Date, Screening_Time
 *   Has_Projector, Has_Screen, Has_Sound, Has_Computer,
 *   Has_WiFi, Has_Microphone, Has_AV_Lead
 *   ADA_Wheelchair, ADA_Elevator, ADA_Restrooms, ADA_Parking,
 *   ADA_Seating, ADA_Transit, ADA_Captions, ADA_Hearing_Loop,
 *   ADA_Lighting, ADA_Signage
 *   Promo_Channels (multi-select compatible)
 *   Frontline_Community, Host_Meeting_Attended
 *   Film_Notes, AV_Notes, Accessibility_Notes, Promo_Notes,
 *   Marketing_Asset_URL, Motivation, Additional_Comments
 */


// ═══════════════════════════════════════════════════════════════
// PART 1: CREATE THE FORM
// ═══════════════════════════════════════════════════════════════

function createHostIntakeForm() {
  var form = FormApp.create('OEFF 2026 — Host Venue Intake Form');
  form.setDescription(
    'One Earth Film Festival 2026\n' +
    'Festival Week: April 22 – 28, 2026\n\n' +
    'Help us understand your venue so we can match you with the right film ' +
    'and support your screening. We\'ll follow up within 5 business days.'
  );
  form.setConfirmationMessage(
    'Thank you! Your intake form has been received.\n' +
    'The OEFF team will review and follow up to confirm your screening details.\n\n' +
    'Festival Week: April 22 – 28, 2026'
  );
  form.setAllowResponseEdits(true);
  form.setCollectEmail(true);

  // ─── SECTION 1: Venue Information ───

  form.addSectionHeaderItem()
    .setTitle('Venue Information')
    .setHelpText('Tell us about your space so we can plan for a great screening.');

  form.addTextItem()
    .setTitle('Organization Name')
    .setRequired(true)
    .setHelpText('Official name of your organization or venue');

  form.addTextItem()
    .setTitle('Venue Address')
    .setRequired(true)
    .setHelpText('Full street address including city, state, ZIP');

  form.addTextItem()
    .setTitle('Capacity')
    .setRequired(true)
    .setHelpText('Maximum seating capacity (number only)')
    .setValidation(FormApp.createTextValidation()
      .requireWholeNumber()
      .requireNumberGreaterThan(0)
      .build());

  form.addParagraphTextItem()
    .setTitle('Venue Description')
    .setRequired(true)
    .setHelpText('Room name, layout, special features, or setup considerations');

  form.addMultipleChoiceItem()
    .setTitle('Frontline Community')
    .setRequired(true)
    .setHelpText('Does your venue serve a frontline or environmental justice community?')
    .setChoiceValues(['Yes', 'No', 'Not sure']);

  // ─── SECTION 2: Primary Contact 1 ───

  form.addPageBreakItem()
    .setTitle('Primary Contact 1');

  form.addTextItem()
    .setTitle('Contact 1 — Name')
    .setRequired(true);

  form.addTextItem()
    .setTitle('Contact 1 — Role')
    .setRequired(false)
    .setHelpText('e.g., Program Director, Green Team Lead');

  form.addTextItem()
    .setTitle('Contact 1 — Email')
    .setRequired(true)
    .setValidation(FormApp.createTextValidation()
      .requireTextIsEmail()
      .build());

  form.addTextItem()
    .setTitle('Contact 1 — Phone')
    .setRequired(false);

  // ─── SECTION 3: Primary Contact 2 ───

  form.addPageBreakItem()
    .setTitle('Primary Contact 2 (optional)')
    .setHelpText('Add a second point of contact if applicable.');

  form.addTextItem()
    .setTitle('Contact 2 — Name')
    .setRequired(false);

  form.addTextItem()
    .setTitle('Contact 2 — Role')
    .setRequired(false);

  form.addTextItem()
    .setTitle('Contact 2 — Email')
    .setRequired(false);

  form.addTextItem()
    .setTitle('Contact 2 — Phone')
    .setRequired(false);

  // ─── SECTION 4: AV & Marketing Contacts ───

  form.addPageBreakItem()
    .setTitle('AV & Marketing Contacts (optional)')
    .setHelpText('Separate contacts for technical setup and event promotion.');

  form.addTextItem()
    .setTitle('AV Contact — Name')
    .setRequired(false)
    .setHelpText('Who handles projector, sound, and screen setup?');

  form.addTextItem()
    .setTitle('AV Contact — Email')
    .setRequired(false);

  form.addTextItem()
    .setTitle('Marketing Contact — Name')
    .setRequired(false)
    .setHelpText('Who handles event promotion and social media?');

  form.addTextItem()
    .setTitle('Marketing Contact — Email')
    .setRequired(false);

  // ─── SECTION 5: Film Selection ───

  form.addPageBreakItem()
    .setTitle('Film Selection')
    .setHelpText(
      'Choose the film you\'d like to screen. Each option shows the film ID, title, year, and primary topic.\n' +
      'If you\'re still deciding, select "Undecided" and we\'ll follow up.'
    );

  form.addListItem()
    .setTitle('Film')
    .setRequired(true)
    .setChoiceValues([
      'F26-001 | Jane Goodall: Reasons for Hope (2025) — Wildlife',
      'F26-002 | Plastic People (2024) — Waste & Recycling',
      'F26-003 | Beyond Zero (2020) — Built Environment',
      'F26-004 | Drowned Land (2025) — Environmental & Social Justice (Indigenous Voices)',
      'F26-005 | Rooted (2021) — Sustainable Food/Ag',
      'F26-006 | How to Power a City (2024) — Energy',
      'F26-007 | Oscar Shorts: The Last Ranger / Planetwalker (2024) — Wildlife / Historical Perspectives',
      'F26-008 | 40 Acres (2024) — People/Cultures (Dystopian Fiction/Horror)',
      'F26-009 | Climate Action Museum (CAM) Awards Partnership — Climate Change',
      'F26-010 | Whose Water? (2024) — Water',
      'F26-011 | Rails to Trails (2025) — Transportation',
      'F26-012 | In Our Nature (2025) — Environmental & Social Justice',
      'Undecided — help me choose'
    ]);

  form.addDateItem()
    .setTitle('Screening Date')
    .setRequired(true)
    .setHelpText('Festival runs April 22 – 28, 2026. Select your preferred date.');

  form.addMultipleChoiceItem()
    .setTitle('Screening Time')
    .setRequired(false)
    .setChoiceValues([
      'Morning (before noon)',
      'Afternoon (noon – 5pm)',
      'Evening (after 5pm)',
      'Flexible'
    ]);

  form.addParagraphTextItem()
    .setTitle('Film Notes')
    .setRequired(false)
    .setHelpText('Topics of interest, audience considerations, backup choices');

  // ─── SECTION 6: AV Equipment ───

  form.addPageBreakItem()
    .setTitle('AV & Technical Setup')
    .setHelpText('Check everything your venue provides. OEFF can help fill gaps.');

  form.addCheckboxItem()
    .setTitle('Available Equipment')
    .setRequired(false)
    .setChoiceValues([
      'Projector',
      'Projection screen',
      'Sound system / speakers',
      'Computer / laptop for playback',
      'Wi-Fi for streaming',
      'Microphone (for Q&A / panel)',
      'On-site AV technician'
    ]);

  form.addParagraphTextItem()
    .setTitle('AV Notes')
    .setRequired(false)
    .setHelpText('Equipment limitations, special setup needs, or help needed from OEFF');

  // ─── SECTION 7: Accessibility & ADA ───

  form.addPageBreakItem()
    .setTitle('Accessibility & ADA Compliance')
    .setHelpText('Help us ensure every attendee can participate. Check all that apply.');

  form.addCheckboxItem()
    .setTitle('Physical Accessibility')
    .setRequired(false)
    .setChoiceValues([
      'Wheelchair accessible entrance',
      'Elevator access',
      'Accessible restrooms',
      'Accessible parking',
      'Flexible seating (wheelchair spaces)',
      'Near public transit'
    ]);

  form.addCheckboxItem()
    .setTitle('Sensory & Communication Accessibility')
    .setRequired(false)
    .setChoiceValues([
      'Can display captions / subtitles',
      'Hearing loop / assistive listening',
      'Adjustable lighting',
      'Clear wayfinding signage'
    ]);

  form.addParagraphTextItem()
    .setTitle('Accessibility Notes')
    .setRequired(false)
    .setHelpText('Barriers, accommodations your venue offers, or support needed');

  // ─── SECTION 8: Marketing & Promotion ───

  form.addPageBreakItem()
    .setTitle('Marketing & Promotion')
    .setHelpText('How will you spread the word? OEFF provides posters, social templates, and press copy.');

  form.addCheckboxItem()
    .setTitle('Promotion Channels')
    .setRequired(true)
    .setChoiceValues([
      'Email newsletter',
      'Print newsletter',
      'Social media',
      'Physical / community boards',
      'Partner networks',
      'Local press / media'
    ]);

  form.addParagraphTextItem()
    .setTitle('Promotion Notes')
    .setRequired(false)
    .setHelpText('Partner orgs, estimated reach, outreach ideas');

  form.addTextItem()
    .setTitle('Marketing Asset URL')
    .setRequired(false)
    .setHelpText('Link to your logos, brand assets, or marketing materials (Google Drive, Dropbox, website)');

  // ─── SECTION 9: Closing ───

  form.addPageBreakItem()
    .setTitle('Anything Else?');

  form.addParagraphTextItem()
    .setTitle('Motivation')
    .setRequired(false)
    .setHelpText('Why does your organization want to host a screening? This helps us match films and tell your story.');

  form.addParagraphTextItem()
    .setTitle('Additional Comments')
    .setRequired(false)
    .setHelpText('Questions, requests, or anything else for the OEFF team');

  form.addMultipleChoiceItem()
    .setTitle('Host Meeting Attended')
    .setRequired(false)
    .setHelpText('Have you attended a host orientation meeting?')
    .setChoiceValues(['Yes', 'Not yet']);

  // ─── Create linked Sheet + install trigger ───

  var ss = SpreadsheetApp.create('OEFF 2026 Host Intake — Responses');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());

  // Create the Airtable-ready sheet
  var atSheet = ss.insertSheet('Airtable Ready');
  var headers = [
    'Intake_ID', 'Timestamp', 'Email_Address',
    'Organization_Name', 'Venue_Address', 'Capacity',
    'Venue_Description', 'Frontline_Community',
    'Contact1_Name', 'Contact1_Role', 'Contact1_Email', 'Contact1_Phone',
    'Contact2_Name', 'Contact2_Role', 'Contact2_Email', 'Contact2_Phone',
    'AV_Contact_Name', 'AV_Contact_Email',
    'Marketing_Contact_Name', 'Marketing_Contact_Email',
    'Film_ID', 'Film_Title', 'Screening_Date', 'Screening_Time', 'Film_Notes',
    'Has_Projector', 'Has_Screen', 'Has_Sound', 'Has_Computer',
    'Has_WiFi', 'Has_Microphone', 'Has_AV_Lead',
    'AV_Notes',
    'ADA_Wheelchair', 'ADA_Elevator', 'ADA_Restrooms', 'ADA_Parking',
    'ADA_Seating', 'ADA_Transit',
    'ADA_Captions', 'ADA_Hearing_Loop', 'ADA_Lighting', 'ADA_Signage',
    'Accessibility_Notes',
    'Promo_Channels', 'Promo_Notes', 'Marketing_Asset_URL',
    'Motivation', 'Additional_Comments', 'Host_Meeting_Attended'
  ];
  atSheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  atSheet.getRange(1, 1, 1, headers.length).setFontWeight('bold');
  atSheet.setFrozenRows(1);

  // Install the auto-processor trigger
  ScriptApp.newTrigger('processNewResponse')
    .forForm(form)
    .onFormSubmit()
    .create();

  Logger.log('══════════════════════════════════════════');
  Logger.log('OEFF Host Intake Form — Created Successfully');
  Logger.log('══════════════════════════════════════════');
  Logger.log('Form edit:     ' + form.getEditUrl());
  Logger.log('Form live:     ' + form.getPublishedUrl());
  Logger.log('Response sheet: ' + ss.getUrl());
  Logger.log('══════════════════════════════════════════');
  Logger.log('NEXT: The form auto-processes responses into');
  Logger.log('the "Airtable Ready" sheet. Export that sheet');
  Logger.log('as CSV to import directly into Airtable.');
  Logger.log('══════════════════════════════════════════');
}


// ═══════════════════════════════════════════════════════════════
// PART 2: AUTO-PROCESSOR (runs on each form submit)
// Splits checkbox groups into individual boolean columns,
// extracts Film_ID from dropdown, generates Intake_ID
// ═══════════════════════════════════════════════════════════════

function processNewResponse(e) {
  var responses = e.response.getItemResponses();
  var data = {};

  // Collect all responses keyed by question title
  responses.forEach(function(item) {
    data[item.getItem().getTitle()] = item.getResponse();
  });

  // Parse Film_ID from dropdown: "F26-001 | Jane Goodall..."
  var filmRaw = data['Film'] || '';
  var filmId = '';
  var filmTitle = '';
  if (filmRaw.indexOf('|') > -1) {
    var parts = filmRaw.split('|');
    filmId = parts[0].trim();
    filmTitle = parts[1].trim().split('—')[0].trim();
  } else {
    filmTitle = filmRaw;
  }

  // Parse equipment checkboxes into individual booleans
  var equipment = data['Available Equipment'] || [];
  if (typeof equipment === 'string') equipment = equipment.split(', ');

  var hasProjector  = equipment.indexOf('Projector') > -1;
  var hasScreen     = equipment.indexOf('Projection screen') > -1;
  var hasSound      = equipment.indexOf('Sound system / speakers') > -1;
  var hasComputer   = equipment.indexOf('Computer / laptop for playback') > -1;
  var hasWifi       = equipment.indexOf('Wi-Fi for streaming') > -1;
  var hasMicrophone = equipment.indexOf('Microphone (for Q&A / panel)') > -1;
  var hasAvLead     = equipment.indexOf('On-site AV technician') > -1;

  // Parse physical accessibility
  var physical = data['Physical Accessibility'] || [];
  if (typeof physical === 'string') physical = physical.split(', ');

  var adaWheelchair = physical.indexOf('Wheelchair accessible entrance') > -1;
  var adaElevator   = physical.indexOf('Elevator access') > -1;
  var adaRestrooms  = physical.indexOf('Accessible restrooms') > -1;
  var adaParking    = physical.indexOf('Accessible parking') > -1;
  var adaSeating    = physical.indexOf('Flexible seating (wheelchair spaces)') > -1;
  var adaTransit    = physical.indexOf('Near public transit') > -1;

  // Parse sensory accessibility
  var sensory = data['Sensory & Communication Accessibility'] || [];
  if (typeof sensory === 'string') sensory = sensory.split(', ');

  var adaCaptions    = sensory.indexOf('Can display captions / subtitles') > -1;
  var adaHearingLoop = sensory.indexOf('Hearing loop / assistive listening') > -1;
  var adaLighting    = sensory.indexOf('Adjustable lighting') > -1;
  var adaSignage     = sensory.indexOf('Clear wayfinding signage') > -1;

  // Promotion channels — keep as comma-separated for Airtable multi-select
  var promoRaw = data['Promotion Channels'] || [];
  if (typeof promoRaw === 'string') promoRaw = promoRaw.split(', ');
  var promoChannels = promoRaw.join(', ');

  // Normalize Frontline_Community to boolean
  var frontlineRaw = data['Frontline Community'] || '';
  var frontline = (frontlineRaw === 'Yes') ? 'Yes' :
                  (frontlineRaw === 'No') ? 'No' : 'Not sure';

  // Normalize Host Meeting to boolean
  var meetingRaw = data['Host Meeting Attended'] || '';
  var meetingAttended = (meetingRaw === 'Yes');

  // Format screening date
  var screeningDate = data['Screening Date'] || '';
  if (screeningDate instanceof Date) {
    screeningDate = Utilities.formatDate(screeningDate, 'America/Chicago', 'yyyy-MM-dd');
  }

  // Generate Intake_ID: HIF-XXX
  var ss = getResponseSpreadsheet();
  var atSheet = ss.getSheetByName('Airtable Ready');
  var lastRow = atSheet.getLastRow();
  var nextNum = lastRow; // row 1 is header, so lastRow = count of data rows
  var intakeId = 'HIF-' + padNum(nextNum, 3);

  // Timestamp
  var timestamp = Utilities.formatDate(
    e.response.getTimestamp(), 'America/Chicago', 'yyyy-MM-dd HH:mm:ss'
  );

  // Write the row
  var row = [
    intakeId,
    timestamp,
    e.response.getRespondentEmail(),
    data['Organization Name'] || '',
    data['Venue Address'] || '',
    data['Capacity'] || '',
    data['Venue Description'] || '',
    frontline,
    data['Contact 1 — Name'] || '',
    data['Contact 1 — Role'] || '',
    data['Contact 1 — Email'] || '',
    data['Contact 1 — Phone'] || '',
    data['Contact 2 — Name'] || '',
    data['Contact 2 — Role'] || '',
    data['Contact 2 — Email'] || '',
    data['Contact 2 — Phone'] || '',
    data['AV Contact — Name'] || '',
    data['AV Contact — Email'] || '',
    data['Marketing Contact — Name'] || '',
    data['Marketing Contact — Email'] || '',
    filmId,
    filmTitle,
    screeningDate,
    data['Screening Time'] || '',
    data['Film Notes'] || '',
    hasProjector, hasScreen, hasSound, hasComputer,
    hasWifi, hasMicrophone, hasAvLead,
    data['AV Notes'] || '',
    adaWheelchair, adaElevator, adaRestrooms, adaParking,
    adaSeating, adaTransit,
    adaCaptions, adaHearingLoop, adaLighting, adaSignage,
    data['Accessibility Notes'] || '',
    promoChannels,
    data['Promotion Notes'] || '',
    data['Marketing Asset URL'] || '',
    data['Motivation'] || '',
    data['Additional Comments'] || '',
    meetingAttended
  ];

  atSheet.appendRow(row);
}


// ═══════════════════════════════════════════════════════════════
// PART 3: HELPERS
// ═══════════════════════════════════════════════════════════════

function padNum(n, width) {
  var s = n.toString();
  while (s.length < width) s = '0' + s;
  return s;
}

function getResponseSpreadsheet() {
  // Find the spreadsheet linked to our form
  var files = DriveApp.searchFiles(
    'title contains "OEFF 2026 Host Intake — Responses" and mimeType = "application/vnd.google-apps.spreadsheet"'
  );
  if (files.hasNext()) {
    return SpreadsheetApp.open(files.next());
  }
  throw new Error('Response spreadsheet not found. Re-run createHostIntakeForm().');
}


// ═══════════════════════════════════════════════════════════════
// PART 4: MANUAL REPROCESSOR
// Run this if you need to rebuild the Airtable Ready sheet
// from all existing form responses
// ═══════════════════════════════════════════════════════════════

function reprocessAllResponses() {
  var files = DriveApp.searchFiles(
    'title contains "OEFF 2026 — Host Venue Intake Form" and mimeType = "application/vnd.google-apps.forms"'
  );
  if (!files.hasNext()) {
    Logger.log('Form not found.');
    return;
  }

  var form = FormApp.openById(files.next().getId());
  var allResponses = form.getResponses();

  // Clear existing data (keep header)
  var ss = getResponseSpreadsheet();
  var atSheet = ss.getSheetByName('Airtable Ready');
  if (atSheet.getLastRow() > 1) {
    atSheet.getRange(2, 1, atSheet.getLastRow() - 1, atSheet.getLastColumn()).clear();
  }

  Logger.log('Reprocessing ' + allResponses.length + ' responses...');

  allResponses.forEach(function(response) {
    processNewResponse({ response: response });
  });

  Logger.log('Done. ' + allResponses.length + ' rows written to Airtable Ready sheet.');
}
