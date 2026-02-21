import os.path
from typing import List

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/forms.body",
    "https://www.googleapis.com/auth/drive",
]

def get_google_credentials(credentials_path: str = "credentials.json", token_path: str = "token.json") -> Credentials:
    """Gets valid user credentials from storage or runs the OAuth flow.

    Args:
        credentials_path (str): Path to the credentials.json file.
        token_path (str): Path to the token.json file for caching.

    Returns:
        Credentials: The Google OAuth2 credentials.
    """
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired Google credentials...")
            creds.refresh(Request())
        else:
            if not os.path.exists(credentials_path):
                raise FileNotFoundError(
                    f"'{credentials_path}' not found. Please follow the setup guide in docs/setup/google-cloud/CREDENTIALS_SETUP.md"
                )
            
            print("\nOpening your browser for Google Authentication...")
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            
            # Using port=0 allows the OS to pick any available port, 
            # preventing "Address already in use" errors (WinError 10048).
            creds = flow.run_local_server(
                port=0, 
                prompt='select_account',
                open_browser=True
            )
        
        with open(token_path, "w") as token:
            token.write(creds.to_json())
            print("Credentials saved to token.json")

    return creds
