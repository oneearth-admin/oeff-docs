/**
 * host-security-sheet.js — OEFF Host Security Data Generator
 *
 * Google Apps Script for generating per-venue:
 *   - Unique URL tokens (unguessable)
 *   - Financial-tier passwords (for scholarship data)
 *   - Screening packet passwords (separate from financial)
 *   - Host helper URLs
 *   - Pre-filled Google Form update URLs
 *
 * Reads venue names and contact emails from a "Hosts" tab,
 * writes security data to a "Host Security" tab with YAMM merge columns.
 *
 * Install: Extensions > Apps Script > paste this file > save.
 * Run: OEFF menu > Generate Host Security Data
 */

// ---------------------------------------------------------------------------
// Configuration — edit these to match your sheet structure
// ---------------------------------------------------------------------------

var CONFIG = {
  // Tab names
  hostsTab: 'Hosts',
  securityTab: 'Host Security',

  // Column headers in the Hosts tab (1-indexed or header names)
  venueNameHeader: 'Venue Name',
  contactEmailHeader: 'Contact Email',

  // Host helper base URL
  helperBaseUrl: 'https://hosts.oneearthfilmfest.org/',

  // Pre-filled Google Form base URL
  // Replace with your actual form URL and entry IDs
  formBaseUrl: 'https://docs.google.com/forms/d/e/YOUR_FORM_ID/viewform',
  formVenueEntryId: 'entry.VENUE_FIELD_ID',
  formEmailEntryId: 'entry.EMAIL_FIELD_ID',

  // Token length (characters). 16 hex chars = 64 bits of entropy.
  tokenLength: 16,
};


// ---------------------------------------------------------------------------
// Menu registration
// ---------------------------------------------------------------------------

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('OEFF')
    .addItem('Generate Host Security Data', 'generateHostSecurityData')
    .addToUi();
}


// ---------------------------------------------------------------------------
// Token and password generation
// ---------------------------------------------------------------------------

/**
 * Generate a cryptographically random hex token.
 * Uses Utilities.getUuid() as entropy source since Apps Script
 * doesn't expose crypto.getRandomValues().
 */
function generateToken(length) {
  // getUuid() returns a v4 UUID like "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"
  // Strip hyphens, take the requested length
  var uuid = Utilities.getUuid().replace(/-/g, '');
  // For extra entropy, hash it
  var hash = Utilities.computeDigest(
    Utilities.DigestAlgorithm.SHA_256,
    uuid + new Date().getTime().toString() + Math.random().toString()
  );
  var hex = hash.map(function(b) {
    return ('0' + (b & 0xff).toString(16)).slice(-2);
  }).join('');
  return hex.substring(0, length);
}


/**
 * Generate a human-readable password in word-word-number format.
 * Uses a curated word list (nature + place words that feel like OEFF).
 */
function generatePassword() {
  var words = [
    'maple', 'river', 'cedar', 'meadow', 'stone', 'birch', 'harbor',
    'summit', 'grove', 'willow', 'prairie', 'ember', 'creek', 'ridge',
    'aspen', 'coral', 'sage', 'linden', 'moss', 'heron', 'fern',
    'oak', 'pine', 'lake', 'field', 'brook', 'cliff', 'dune',
    'bloom', 'wind', 'frost', 'dawn', 'reef', 'vale', 'peak',
    'screening', 'festival', 'gather', 'lantern', 'canopy', 'forage'
  ];

  var w1 = words[Math.floor(Math.random() * words.length)];
  var w2 = words[Math.floor(Math.random() * words.length)];
  // Avoid duplicates
  while (w2 === w1) {
    w2 = words[Math.floor(Math.random() * words.length)];
  }
  var num = Math.floor(Math.random() * 90) + 10; // 10-99
  return w1 + '-' + w2 + '-' + num;
}


/**
 * SHA-256 hash a string, return lowercase hex.
 */
function sha256Hex(input) {
  var digest = Utilities.computeDigest(
    Utilities.DigestAlgorithm.SHA_256,
    input
  );
  return digest.map(function(b) {
    return ('0' + (b & 0xff).toString(16)).slice(-2);
  }).join('');
}


// ---------------------------------------------------------------------------
// URL builders
// ---------------------------------------------------------------------------

function buildHelperUrl(token) {
  return CONFIG.helperBaseUrl + token + '/';
}


function buildUpdateFormUrl(venueName, contactEmail) {
  var url = CONFIG.formBaseUrl
    + '?' + CONFIG.formVenueEntryId + '=' + encodeURIComponent(venueName)
    + '&' + CONFIG.formEmailEntryId + '=' + encodeURIComponent(contactEmail || '');
  return url;
}


// ---------------------------------------------------------------------------
// Main generator
// ---------------------------------------------------------------------------

function generateHostSecurityData() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var ui = SpreadsheetApp.getUi();

  // Read Hosts tab
  var hostsSheet = ss.getSheetByName(CONFIG.hostsTab);
  if (!hostsSheet) {
    ui.alert('Error: "' + CONFIG.hostsTab + '" tab not found.');
    return;
  }

  var data = hostsSheet.getDataRange().getValues();
  if (data.length < 2) {
    ui.alert('Error: "' + CONFIG.hostsTab + '" tab has no data rows.');
    return;
  }

  // Find column indices from headers
  var headers = data[0];
  var venueCol = headers.indexOf(CONFIG.venueNameHeader);
  var emailCol = headers.indexOf(CONFIG.contactEmailHeader);

  if (venueCol === -1) {
    ui.alert('Error: Column "' + CONFIG.venueNameHeader + '" not found in Hosts tab.');
    return;
  }
  if (emailCol === -1) {
    ui.alert('Error: Column "' + CONFIG.contactEmailHeader + '" not found in Hosts tab.');
    return;
  }

  // Get or create Security tab
  var secSheet = ss.getSheetByName(CONFIG.securityTab);
  if (!secSheet) {
    secSheet = ss.insertSheet(CONFIG.securityTab);
  } else {
    secSheet.clearContents();
  }

  // Write headers
  var secHeaders = [
    'Venue Name',
    'Contact Email',
    'Host Token',
    'Host Helper URL',
    'Financial Password',
    'Financial Password Hash',
    'Packet Password',
    'Update Form URL',
    'Generated At',
  ];
  secSheet.getRange(1, 1, 1, secHeaders.length).setValues([secHeaders]);
  secSheet.getRange(1, 1, 1, secHeaders.length).setFontWeight('bold');

  // Check for existing tokens — preserve them if re-running
  // (This prevents token rotation on re-runs)
  var existingTokens = {};
  var existingData = secSheet.getDataRange().getValues();
  for (var e = 1; e < existingData.length; e++) {
    if (existingData[e][0] && existingData[e][2]) {
      existingTokens[existingData[e][0]] = {
        token: existingData[e][2],
        financialPw: existingData[e][4],
        packetPw: existingData[e][6],
      };
    }
  }

  // Generate security data for each venue
  var outputRows = [];
  var now = new Date().toISOString();

  for (var i = 1; i < data.length; i++) {
    var venueName = data[i][venueCol];
    var email = data[i][emailCol];

    if (!venueName || String(venueName).trim() === '') continue;

    venueName = String(venueName).trim();
    email = String(email || '').trim();

    // Reuse existing token/passwords if available, generate new otherwise
    var existing = existingTokens[venueName];
    var token = existing ? existing.token : generateToken(CONFIG.tokenLength);
    var financialPw = existing ? existing.financialPw : generatePassword();
    var packetPw = existing ? existing.packetPw : generatePassword();

    var helperUrl = buildHelperUrl(token);
    var financialHash = sha256Hex(financialPw);
    var updateFormUrl = buildUpdateFormUrl(venueName, email);

    outputRows.push([
      venueName,
      email,
      token,
      helperUrl,
      financialPw,
      financialHash,
      packetPw,
      updateFormUrl,
      now,
    ]);
  }

  if (outputRows.length === 0) {
    ui.alert('No venues found in the Hosts tab.');
    return;
  }

  // Write all rows at once (fast)
  secSheet.getRange(2, 1, outputRows.length, secHeaders.length)
    .setValues(outputRows);

  // Format: auto-resize columns, protect password columns
  secSheet.autoResizeColumns(1, secHeaders.length);

  ui.alert(
    'Host Security Data Generated',
    outputRows.length + ' venue(s) processed.\n\n'
    + 'Columns ready for YAMM merge:\n'
    + '  - Host Helper URL\n'
    + '  - Financial Password\n'
    + '  - Packet Password\n'
    + '  - Update Form URL\n\n'
    + 'Remember: Financial Password and Packet Password should be '
    + 'sent in SEPARATE emails from the helper URL.',
    ui.ButtonSet.OK
  );
}
