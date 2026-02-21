# Google Cloud Setup Guide

This guide explains how to set up the Google Cloud Project and obtain the `credentials.json` file required for this automation.

## 1. Create Project & Enable APIs
1.  Open [Google Cloud Console](https://console.cloud.google.com/).
2.  Create a project named `BibleQuiz-Automation`.
3.  Enable the following APIs:
    - **Google Sheets API**
    - **Google Forms API**
    - **Google Drive API**

## 2. OAuth Consent Screen
1.  Navigate to **APIs & Services > OAuth consent screen**.
2.  User Type: **External**.
3.  App Name: `Bible Quiz Automator`.
4.  Add your email to **Test Users** (Mandatory for testing mode).

## 3. Create Desktop Credentials
1.  Navigate to **APIs & Services > Credentials**.
2.  Click **Create Credentials > OAuth client ID**.
3.  Select **Desktop app**.
4.  Name: `BibleQuiz-CLI`.
5.  Download the JSON and rename it to `credentials.json`.
6.  Place `credentials.json` in the project root.

## 4. Troubleshooting
- **Error 403: Access Not Configured:** Ensure all 3 APIs are enabled.
- **Error 403: org_internal:** Ensure you added your email as a "Test User" in the Consent Screen settings.
- **Token Expired:** Delete `token.json` (if it exists) to trigger a fresh login.
