/**
 * OEFF Host Intake Form — Voice Alignment Update
 *
 * Run this once in Apps Script (linked to the form) to update
 * section descriptions, question help text, and confirmation message
 * to match OEFF's partnership-centered communication voice.
 *
 * HOW TO USE:
 * 1. Open the form in Google Forms
 * 2. Click ⋮ (three dots menu, top right) → Apps Script
 * 3. Paste this entire file, replacing the default code
 * 4. Click Save (floppy disk icon)
 * 5. Select updateFormText from the function dropdown
 * 6. Click Run
 * 7. Authorize when prompted (first run only)
 * 8. Check Execution Log to confirm success
 */

function updateFormText() {
  var form = FormApp.openById('1QHXvvXU9JPsKIITC50cbq77XKHReAUcC8ymKXMkboig');
  var items = form.getItems();

  // ─── Update confirmation message ───
  form.setConfirmationMessage(
    'We\'re glad you\'re hosting.\n\n' +
    'Thank you for opening your space to your community this Earth Week. ' +
    'We\'ve received your information and will be in touch within 5 business days ' +
    'to confirm your screening details and talk through next steps together.\n\n' +
    'Festival Week: April 22 \u2013 28, 2026'
  );

  // ─── Walk through all items and update by title ───
  for (var i = 0; i < items.length; i++) {
    var item = items[i];
    var title = item.getTitle();
    var type = item.getType();

    // Section headers (PAGE_BREAK items)
    if (type == FormApp.ItemType.PAGE_BREAK) {
      var pb = item.asPageBreakItem();

      if (title === 'Film Selection') {
        pb.setHelpText(
          'Which film speaks to your community? If you\'re still deciding, ' +
          'select Undecided and we\'ll help you find the right fit.'
        );
      }
      else if (title === 'AV & Technical Setup') {
        pb.setHelpText(
          'Check what your venue already has. We can help fill any gaps ' +
          '\u2014 that\'s what we\'re here for.'
        );
      }
      else if (title === 'Accessibility & ADA Compliance') {
        pb.setTitle('Accessibility');
        pb.setHelpText(
          'Every screening should be welcoming to everyone in your community. ' +
          'Check what your venue offers.'
        );
      }
      else if (title === 'Marketing & Promotion') {
        pb.setHelpText(
          'You know how to reach your community. We\'ll provide posters, ' +
          'social templates, and press copy to support your outreach.'
        );
      }
      else if (title === 'Anything Else?') {
        pb.setTitle('Your Screening Story');
      }
    }

    // Question-level help text updates
    if (title === 'Motivation') {
      item.setHelpText(
        'What drew you to this \u2014 a connection to the topic, ' +
        'your community\'s interests, a past screening that worked well?'
      );
    }
  }

  Logger.log('All form text updates applied successfully.');
  Logger.log('Updated: Film Selection, AV, Accessibility, Marketing, Your Screening Story, Motivation, Confirmation message');
}
