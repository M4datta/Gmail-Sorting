import base64
import os
from email.mime.text import MIMEText

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from openai import OpenAI

# -------- CONFIG --------
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
OPENAI_API_KEY = "your-openai-key"

client = OpenAI(api_key=OPENAI_API_KEY)

# -------- AUTH --------
def authenticate_gmail():
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
    creds = flow.run_local_server(port=8080)
    service = build('gmail', 'v1', credentials=creds)
    return service

# -------- FETCH EMAILS --------
def get_emails(service):
    results = service.users().messages().list(
        userId='me', maxResults=10).execute()
    messages = results.get('messages', [])
    return messages

def get_email_content(service, msg_id):
    msg = service.users().messages().get(userId='me', id=msg_id).execute()
    snippet = msg.get('snippet', '')
    return snippet

# -------- AI CLASSIFIER --------
def classify_email(text):
    prompt = f"""
    Classify this email into one category:
    Important, Work, Personal, Promotions, Spam
    
    Email:
    {text}
    """

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()

# -------- APPLY LABEL --------
def apply_label(service, msg_id, label_name):
    labels = service.users().labels().list(userId='me').execute()
    label_id = None

    for label in labels['labels']:
        if label['name'] == label_name:
            label_id = label['id']

    # create label if not exists
    if not label_id:
        new_label = {
            "name": label_name,
            "labelListVisibility": "labelShow",
            "messageListVisibility": "show"
        }
        label = service.users().labels().create(
            userId='me', body=new_label).execute()
        label_id = label['id']

    service.users().messages().modify(
        userId='me',
        id=msg_id,
        body={'addLabelIds': [label_id]}
    ).execute()

# -------- AGENT LOOP --------
def run_agent():
    service = authenticate_gmail()
    messages = get_emails(service)

    for msg in messages:
        msg_id = msg['id']
        content = get_email_content(service, msg_id)

        category = classify_email(content)
        print(f"Email: {content[:50]}...")
        print(f"Category: {category}\n")

        apply_label(service, msg_id, category)

# -------- RUN --------
if __name__ == "__main__":
    run_agent()
