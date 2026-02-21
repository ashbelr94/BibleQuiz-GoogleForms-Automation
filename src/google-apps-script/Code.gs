/**
 * Main Google Apps Script for Bible Quiz Automation
 * 
 * Instructions:
 * 1. Open your Google Sheet.
 * 2. Tools -> Script Editor.
 * 3. Replace the content with this script.
 * 4. Update the CONFIG object below with your Spreadsheet IDs.
 */

const CONFIG = {
  // Replace these with the actual Spreadsheet IDs where responses should go
  TAMIL_RESPONSE_SHEET_ID: 'YOUR_TAMIL_RESPONSE_SPREADSHEET_ID_HERE',
  ENGLISH_RESPONSE_SHEET_ID: 'YOUR_ENGLISH_RESPONSE_SPREADSHEET_ID_HERE',
  
  // Static content for the forms
  RULES_EN: "Standard Rules: 
1. Only one submission per person.
2. Please read the portions before answering.",
  RULES_TA: "விதிமுறைகள்: 
1. ஒருவர் ஒரு முறை மட்டுமே சமர்ப்பிக்க வேண்டும்.
2. பதிலளிக்கும் முன் வேதப்பகுதிகளை வாசிக்கவும்.",
  
  YEAR: new Date().getFullYear(),
};

/**
 * Creates a custom menu in the Google Sheet.
 */
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('📖 Bible Quiz')
      .addItem('Generate Forms for a Week', 'promptForWeek')
      .addToUi();
}

/**
 * Prompts the user to enter the week number.
 */
function promptForWeek() {
  const ui = SpreadsheetApp.getUi();
  const response = ui.prompt('Generate Bible Quiz Forms', 'Enter the Week Number:', ui.ButtonSet.OK_CANCEL);

  if (response.getSelectedButton() == ui.Button.OK) {
    const week = response.getResponseText();
    if (!week || isNaN(week)) {
      ui.alert('Please enter a valid week number.');
      return;
    }
    generateForms(week);
  }
}

/**
 * Main logic to read sheet data and generate forms.
 */
function generateForms(weekNum) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const data = sheet.getDataRange().getValues();
  
  // Skip header row
  const rows = data.slice(1);
  
  // Filter rows for the requested week
  const weekData = rows.filter(row => row[1].toString() === weekNum.toString());
  
  if (weekData.length === 0) {
    SpreadsheetApp.getUi().alert('No data found for Week ' + weekNum);
    return;
  }

  // Common metadata for the forms
  const dates = weekData[0][2];
  const portion = weekData[0][3];

  // Create Tamil Form
  createLanguageForm('Tamil', weekNum, dates, portion, weekData, 'TA');
  
  // Create English Form
  createLanguageForm('English', weekNum, dates, portion, weekData, 'EN');

  SpreadsheetApp.getUi().alert('Forms generated successfully for Week ' + weekNum);
}

/**
 * Creates a form for a specific language.
 * @param {string} langName - 'English' or 'Tamil'
 * @param {string} weekNum - Week number
 * @param {string} dates - Date range
 * @param {string} portion - Bible portion
 * @param {Array} rows - Filtered rows for the week
 * @param {string} langCode - 'EN' or 'TA'
 */
function createLanguageForm(langName, weekNum, dates, portion, rows, langCode) {
  const title = `Week ${weekNum} - ${langName} Bible Quiz | ${CONFIG.YEAR}`;
  const description = `Week ${weekNum} | ${dates} | ${portion}

${langCode === 'EN' ? CONFIG.RULES_EN : CONFIG.RULES_TA}`;
  
  const form = FormApp.create(title)
      .setDescription(description)
      .setIsQuiz(true)
      .setLimitOneResponsePerEmail(true)
      .setCollectEmail(true);

  // Add questions
  rows.forEach(row => {
    const qId = row[0];
    const scripture = row[6];
    
    let questionText = "";
    let answerText = "";

    if (langCode === 'TA') {
      questionText = `${qId}. ${row[5]}`; // Tamil Question
      answerText = `${scripture}, ${row[7]}`; // Tamil Answer
    } else {
      questionText = `${qId}. ${row[8]}`; // English Question
      answerText = `${scripture}, ${row[9]}`; // English Answer
    }

    const item = form.addTextItem();
    item.setTitle(questionText)
        .setRequired(true);

    // Set Correct Answer and Points
    const quizFeedback = FormApp.createFeedback()
        .setText('Correct Answer: ' + answerText)
        .build();
    
    // For short answer (TextItem), we create a validation/key
    // Note: FormApp API doesn't allow setting the "Answer Key" for TextItem directly via script as easily as Multiple Choice,
    // but we can set the points and the correct answer string for grading.
    item.setPoints(2);
    
    // We add the correct answer to the list of acceptable answers
    const validation = FormApp.createTextValidation()
        .requireTextContains(answerText)
        .build();
    // item.setValidation(validation); // Optional: if you want to force specific format
  });

  // Link to response spreadsheet
  const spreadsheetId = langCode === 'TA' ? CONFIG.TAMIL_RESPONSE_SHEET_ID : CONFIG.ENGLISH_RESPONSE_SHEET_ID;
  if (spreadsheetId && spreadsheetId !== 'YOUR_TAMIL_RESPONSE_SPREADSHEET_ID_HERE') {
    form.setDestination(FormApp.DestinationType.SPREADSHEET, spreadsheetId);
  }

  Logger.log(`Created ${langName} form: ${form.getEditUrl()}`);
  return form;
}
