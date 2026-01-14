import base64
import re


def clean_html(html):
    """Remove HTML tags and extra spaces"""
    text = re.sub('<[^<]+?>', '', html)
    return text.strip()


def parse_email(service, message_id):
    message = service.users().messages().get(
        userId='me',
        id=message_id,
        format='full'
    ).execute()

    headers = message.get('payload', {}).get('headers', [])

    email_data = {
        'from': '',
        'subject': '',
        'date': '',
        'content': ''
    }

    for header in headers:
        name = header.get('name')
        value = header.get('value')

        if name == 'From':
            email_data['from'] = value.split('<')[-1].replace('>', '') if '<' in value else value
        elif name == 'Subject':
            email_data['subject'] = value
        elif name == 'Date':
            email_data['date'] = value

    payload = message.get('payload', {})
    parts = payload.get('parts', [])

    # Prefer text/plain
    for part in parts:
        if part.get('mimeType') == 'text/plain':
            data = part.get('body', {}).get('data')
            if data:
                email_data['content'] = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                return email_data

    # Fallback to HTML
    for part in parts:
        if part.get('mimeType') == 'text/html':
            data = part.get('body', {}).get('data')
            if data:
                html = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                email_data['content'] = clean_html(html)
                return email_data

    return email_data
