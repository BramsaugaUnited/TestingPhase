import os
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from flask import Flask, jsonify
from bs4 import BeautifulSoup

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

app = Flask(__name__)

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def get_emails(service):
    results = service.users().messages().list(userId='me', q="from:submissions@formsubmit.co").execute()
    messages = results.get('messages', [])
    
    emails = []
    if not messages:
        print("No messages found.")
    else:
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            payload = msg['payload']
            headers = payload['headers']
            
            email_body = None
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body']['data']
                    text = base64.urlsafe_b64decode(data).decode('utf-8')
                    email_body = text
                    break
            
            if email_body:
                emails.append({'email_body': email_body})
                print("Email body:", email_body)
                print("=" * 50)
                
    return emails

@app.route('/api/membership_info', methods=['GET'])
def membership_info():
    service = authenticate_gmail()
    emails = get_emails(service)
    
    # Return email bodies in JSON response
    return jsonify(emails)

if __name__ == '__main__':
    app.run(debug=True)
