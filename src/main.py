import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import SPREADSHEET_ID



from gmail_service import get_gmail_service, get_unread_messages, mark_as_read
from email_parser import parse_email
from sheets_service import get_sheets_service, append_row



gmail_service = get_gmail_service()
creds = gmail_service._http.credentials
sheets_service = get_sheets_service(creds)

messages = get_unread_messages(gmail_service)

for msg in messages:
    email = parse_email(gmail_service, msg['id'])
    row = [
        email['from'],
        email['subject'],
        email['date'],
        email['content']
    ]
    append_row(sheets_service, SPREADSHEET_ID, row)
    mark_as_read(gmail_service, msg['id'])

  