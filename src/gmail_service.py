from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os

SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/spreadsheets'
]


def get_gmail_service():
    creds = None

    # If token already exists, load it
    if os.path.exists('credentials/token.json'):
        creds = Credentials.from_authorized_user_file(
            'credentials/token.json', SCOPES
        )

    # If no valid credentials, do OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials/credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save token for next runs
        with open('credentials/token.json', 'w') as token:
            token.write(creds.to_json())

    # Create Gmail API service
    service = build('gmail', 'v1', credentials=creds)
    return service

def get_unread_messages(service):
    """
    Fetch unread messages from the user's inbox.
    Returns a list of message IDs.
    """ 
    results = service.users().messages().list(
        userId='me',
        q='is:unread'
    ).execute()


    messages = results.get('messages', [])

    return messages

def mark_as_read(service, message_id):
    service.users().messages().modify(
        userId='me',
        id=message_id,
        body={'removeLabelIds': ['UNREAD']}
    ).execute()
