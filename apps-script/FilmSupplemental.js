/**
 * OEFF 2026 Film Supplemental Form — Google Form Generator
 *
 * Short follow-up form for filmmakers who already submitted the
 * Film Intake Survey. Captures the fields that weren't on the
 * intake form: attendance, Q&A, social media, marketing.
 *
 * HOW TO USE:
 * 1. Go to https://script.google.com
 * 2. Create a new project (or add to existing OEFF project)
 * 3. Paste this entire file into the editor
 * 4. Click Run → select createFilmSupplementalForm
 * 5. Authorize when prompted
 * 6. Check Execution Log for form URLs
 *
 * WHAT THIS CREATES:
 * - A Google Form (~5 minutes to complete)
 * - A linked response Sheet with an auto-processor
 * - An "Airtable Ready" sheet that maps to Film Contacts + Participants tables
 */


// Film dropdown options — matches Film Intake Survey
var FILMS_2026 = [
  'F26-001 | Jane Goodall: Reasons for Hope',
  'F26-002 | Plastic People',
  'F26-003 | Beyond Zero',
  'F26-004 | Drowned Land',
  'F26-005 | Rooted',
  'F26-006 | How to Power a City',
  'F26-007 | The Last Ranger / Planetwalker',
  'F26-008 | 40 Acres',
  'F26-010 | Whose Water?',
  'F26-011 | Rails to Trails',
  'F26-012 | In Our Nature'
];


// ═══════════════════════════════════════════════════════════════
// PART 1: CREATE THE FORM
// ═══════════════════════════════════════════════════════════════

function createFilmSupplementalForm() {
  var form = FormApp.create('OEFF 2026 — Filmmaker Follow-Up');
  form.setDescription(
    'One Earth Film Festival 2026\n' +
    'Festival Week: April 22 – 28, 2026\n\n' +
    'Thanks for submitting the Film Intake Survey! This short follow-up ' +
    'helps us coordinate promotion, schedule any post-screening conversation, ' +
    'and connect audiences with your work.\n\n' +
    'Should take about 5 minutes.'
  );
  form.setConfirmationMessage(
    'Thank you! We\'ll be in touch soon with screening details and next steps.'
  );
  form.setAllowResponseEdits(true);
  form.setLimitOneResponsePerUser(false); // multiple films possible


  // ── Section 1: Identity ──
  form.addPageBreakItem()
    .setTitle('Your Film');

  var filmDropdown = form.addListItem()
    .setTitle('Film Title')
    .setHelpText('Select your film from the dropdown.')
    .setRequired(true);
  filmDropdown.setChoiceValues(FILMS_2026);

  form.addTextItem()
    .setTitle('Your Name')
    .setRequired(true);

  form.addTextItem()
    .setTitle('Your Email')
    .setRequired(true);


  // ── Section 2: Filmmaker Attendance ──
  form.addPageBreakItem()
    .setTitle('Post-Screening Conversation')
    .setHelpText(
      'We love connecting audiences with filmmakers after screenings. ' +
      'This can be a brief Q&A, a moderated conversation, or a virtual check-in.\n\n' +
      'OEFF offers a $100 stipend for virtual appearances and up to $300 for in-person.'
    );

  form.addMultipleChoiceItem()
    .setTitle('Would you or a representative be available for a post-screening conversation?')
    .setChoiceValues(['Yes — in person', 'Yes — virtually', 'Maybe — let\'s discuss', 'No'])
    .setRequired(true);

  form.addTextItem()
    .setTitle('If yes: name and role of the person who would participate')
    .setHelpText('e.g., "Jane Smith, Director" or "Same as above"')
    .setRequired(false);

  form.addTextItem()
    .setTitle('If yes: their email (if different from yours)')
    .setRequired(false);

  form.addMultipleChoiceItem()
    .setTitle('Preferred format?')
    .setChoiceValues([
      'Brief Q&A (10-15 min)',
      'Moderated conversation (20-30 min)',
      'Panel with other filmmakers',
      'Open to any format'
    ])
    .setRequired(false);


  // ── Section 3: Promotion & Social ──
  form.addPageBreakItem()
    .setTitle('Promotion')
    .setHelpText(
      'Help us amplify your screening. We\'ll tag you in our posts ' +
      'and share any materials you provide.'
    );

  form.addParagraphTextItem()
    .setTitle('Social media handles')
    .setHelpText('Film and/or filmmaker accounts — Instagram, X, Facebook, TikTok, Letterboxd, etc.')
    .setRequired(false);

  form.addMultipleChoiceItem()
    .setTitle('Premiere status for this screening')
    .setChoiceValues([
      'Chicago-area premiere',
      'Midwest premiere',
      'US premiere',
      'Not a premiere',
      'Not sure'
    ])
    .setRequired(false);

  form.addParagraphTextItem()
    .setTitle('Any updates about the film since you submitted?')
    .setHelpText('Awards, press, new trailer, upcoming releases — anything we should know for promo.')
    .setRequired(false);

  form.addMultipleChoiceItem()
    .setTitle('Do you have a trailer or clip we can use for promotion?')
    .setChoiceValues(['Yes — I\'ll send the link', 'Yes — it\'s on our website', 'No', 'Not sure'])
    .setRequired(false);

  form.addTextItem()
    .setTitle('Trailer/clip link (if available)')
    .setRequired(false);

  form.addMultipleChoiceItem()
    .setTitle('Where can audiences watch or buy your film after the festival?')
    .setChoiceValues([
      'Available on a streaming platform',
      'Available for purchase/rental online',
      'Not yet available — festival circuit only',
      'Other — I\'ll explain below'
    ])
    .setRequired(false);

  form.addTextItem()
    .setTitle('Platform or purchase link (if applicable)')
    .setRequired(false);


  // ── Done ──

  // Create linked spreadsheet
  var ss = SpreadsheetApp.create('OEFF 2026 Film Supplemental — Responses');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());

  // Log URLs
  Logger.log('═══════════════════════════════════════════════');
  Logger.log('FORM CREATED SUCCESSFULLY');
  Logger.log('═══════════════════════════════════════════════');
  Logger.log('Edit URL:     ' + form.getEditUrl());
  Logger.log('Live URL:     ' + form.getPublishedUrl());
  Logger.log('Response Sheet: ' + ss.getUrl());
  Logger.log('═══════════════════════════════════════════════');
  Logger.log('');
  Logger.log('NEXT STEPS:');
  Logger.log('1. Open the form edit URL and preview it');
  Logger.log('2. Run createAirtableReadySheet() to add the processor');
  Logger.log('3. Include the live URL in the Monday filmmaker email');

  return form;
}


// ═══════════════════════════════════════════════════════════════
// PART 2: AIRTABLE-READY PROCESSOR
// ═══════════════════════════════════════════════════════════════

function createAirtableReadySheet() {
  var ss = getSupplementalResponseSheet();

  // Check if Airtable Ready sheet already exists
  var existing = ss.getSheetByName('Airtable Ready');
  if (existing) {
    Logger.log('Airtable Ready sheet already exists. Refreshing...');
    existing.clear();
  } else {
    existing = ss.insertSheet('Airtable Ready');
  }

  // Headers matching Airtable schema
  var headers = [
    'Film_ID',
    'Film_Title',
    'Contact_Name',
    'Contact_Email',
    'Attendance_Available',
    'Attendance_Type',
    'Attendee_Name',
    'Attendee_Email',
    'Discussion_Format',
    'Social_Handles',
    'Premiere_Status',
    'Film_Updates',
    'Has_Trailer',
    'Trailer_Link',
    'Post_Festival_Availability',
    'Purchase_Link',
    'Submission_Timestamp'
  ];
  existing.getRange(1, 1, 1, headers.length).setValues([headers]);
  existing.getRange(1, 1, 1, headers.length).setFontWeight('bold');

  // Set up trigger
  var triggers = ScriptApp.getProjectTriggers();
  var hasSupplementalTrigger = triggers.some(function(t) {
    return t.getHandlerFunction() === 'onSupplementalSubmit';
  });
  if (!hasSupplementalTrigger) {
    ScriptApp.newTrigger('onSupplementalSubmit')
      .forSpreadsheet(ss)
      .onFormSubmit()
      .create();
    Logger.log('Form submit trigger created.');
  }

  Logger.log('Airtable Ready sheet configured with ' + headers.length + ' columns.');
}


function onSupplementalSubmit(e) {
  var ss = e.source;
  var sheet = ss.getSheetByName('Airtable Ready');
  if (!sheet) return;

  var response = e.values;
  // response[0] = timestamp
  // response[1] = Film Title (with F26-XXX prefix)
  // response[2] = Your Name
  // response[3] = Your Email
  // response[4] = Available for post-screening?
  // response[5] = Attendee name/role
  // response[6] = Attendee email
  // response[7] = Preferred format
  // response[8] = Social handles
  // response[9] = Premiere status
  // response[10] = Film updates
  // response[11] = Has trailer?
  // response[12] = Trailer link
  // response[13] = Post-festival availability
  // response[14] = Purchase link

  var filmField = response[1] || '';
  var filmId = filmField.split(' | ')[0] || '';
  var filmTitle = filmField.split(' | ')[1] || filmField;

  // Map attendance response to type
  var attendanceRaw = response[4] || '';
  var attendanceType = 'TBD';
  if (attendanceRaw.indexOf('in person') >= 0) attendanceType = 'In-Person';
  else if (attendanceRaw.indexOf('virtually') >= 0) attendanceType = 'Virtual';
  else if (attendanceRaw.indexOf('Maybe') >= 0) attendanceType = 'TBD';
  else if (attendanceRaw.indexOf('No') >= 0) attendanceType = 'None';

  var row = [
    filmId,
    filmTitle,
    response[2] || '',   // name
    response[3] || '',   // email
    attendanceRaw,       // raw attendance response
    attendanceType,      // normalized
    response[5] || '',   // attendee name
    response[6] || '',   // attendee email
    response[7] || '',   // format preference
    response[8] || '',   // social handles
    response[9] || '',   // premiere status
    response[10] || '',  // film updates
    response[11] || '',  // has trailer
    response[12] || '',  // trailer link
    response[13] || '',  // post-festival
    response[14] || '',  // purchase link
    response[0] || ''    // timestamp
  ];

  sheet.appendRow(row);
}


// ═══════════════════════════════════════════════════════════════
// HELPERS
// ═══════════════════════════════════════════════════════════════

function getSupplementalResponseSheet() {
  var files = DriveApp.searchFiles(
    'title contains "OEFF 2026 Film Supplemental — Responses" and mimeType = "application/vnd.google-apps.spreadsheet"'
  );
  if (files.hasNext()) {
    return SpreadsheetApp.open(files.next());
  }
  throw new Error('Response spreadsheet not found. Run createFilmSupplementalForm() first.');
}
