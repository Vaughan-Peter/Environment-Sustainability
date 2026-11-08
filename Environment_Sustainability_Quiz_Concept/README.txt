# Environment & Sustainability Quiz (Windows)

## Features
- Desktop GUI designed for a 600 x 500 pixel window
- Main menu and About page
- Student first name, last name, optional ID number, optional teacher name
- Grades 7 through 12
- Small (10), Medium (25), and Long (50) tests
- Environment, Sustainability, or Both topic filters
- Random question selection and answer review
- PDF report with score, topic breakdown, responses, correct answers, and explanations
- Question bank stored in `question_bank.json`, editable as JSON

## Install and run
1. Install Python 3.10 or newer from https://www.python.org/downloads/windows/
2. During installation, select **Add Python to PATH**.
3. Extract the ZIP file to a folder.
4. Open Command Prompt in that folder.
5. Install the PDF package:
   ```bat
   py -m pip install reportlab
   ```
6. Start the app:
   ```bat
   py app.py
   ```

Tkinter is normally included with the standard Windows Python installer. If the PDF library is not installed, the quiz still runs but PDF export will ask you to install it.

## Question bank
The app reads `question_bank.json` from the same folder. Each question contains:
- `id`
- `grade_min`, `grade_max`
- `category`
- `topic_group` (`Environment` or `Sustainability`)
- `type` (`mc` or `tf`)
- `question`
- `options`
- `answer` (zero-based index into `options`)
- `explanation`

Important: This is a starter question bank and should be reviewed by an educator before formal classroom use. The 1,000-entry bank includes generated variants and some questions are intentionally general; review for duplication, distractor quality, local curriculum alignment, and factual nuance before publishing. For best results, have a teacher verify each item and its correct answer.
