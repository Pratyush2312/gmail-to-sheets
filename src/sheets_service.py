from googleapiclient.discovery import build


def get_sheets_service(creds):
    """
    Creates and returns a Google Sheets API service object.
    """
    service = build('sheets', 'v4', credentials=creds)
    return service


def append_row(service, spreadsheet_id, row):
    """
    Appends a single row to the Google Sheet.
    """

    body = {
        'values': [row]
    }

    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range='Sheet1!A:D',
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()
