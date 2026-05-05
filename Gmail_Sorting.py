import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from openai import OpenAI

# -------- CONFIG -------- #
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # safer

client = OpenAI(api_key=OPENAI_API_KEY)

# -------- AUTH -------- #
def authenticate_gmail():
    creds = None

    # ONLY try to load token safely
    if os.path.exists("token.json"):
        try:
            creds = Credentials.from_authorized_user_file(
                "token.json",
                SCOPES
            )

            # If token is missing refresh_token, force reset
            if not creds.refresh_token:
                print("⚠️ Invalid token detected. Re-auth required.")
                creds = None

        except Exception:
            print("⚠️ Corrupted token file. Re-auth required.")
            creds = None

    # If no valid credentials → login again
    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json",
            SCOPES
        )

        creds = flow.run_local_server(
            port=8080,
            access_type="offline",
            prompt="consent"
        )

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)
# -------- FETCH EMAILS -------- #
def get_emails(service):
    try:
        results = service.users().messages().list(
            userId='me',
            maxResults=10,
            q="in:inbox"
        ).execute()

        return results.get('messages', [])
    except Exception as e:
        print("❌ Error fetching emails:", e)
        return []

# -------- GET EMAIL CONTENT -------- #
def get_email_content(service, msg_id):
    try:
        msg = service.users().messages().get(
            userId='me',
            id=msg_id
        ).execute()

        return msg.get('snippet', '')
    except Exception as e:
        print("❌ Error reading email:", e)
        return ""

# -------- AI CLASSIFIER -------- #
def classify_email(text):
    try:
        prompt = f"""
        Return ONLY ONE word label.
        Allowed labels:
        Important, Work, Personal, Promotions, Spam

        Do NOT add explanation.
        Do NOT add punctuation.
        Email:
        {text}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("❌ AI Error:", e)
        return "Unknown"

# -------- APPLY LABEL -------- #
def apply_label(service, msg_id, label_name):
    try:
        labels = service.users().labels().list(userId='me').execute()
        label_id = None

        for label in labels['labels']:
            if label['name'] == label_name:
                label_id = label['id']
                break

        # Create label if not exists
        if not label_id:
            new_label = {
                "name": label_name,
                "labelListVisibility": "labelShow",
                "messageListVisibility": "show"
            }

            label = service.users().labels().create(
                userId='me',
                body=new_label
            ).execute()

            label_id = label['id']

        service.users().messages().modify(
            userId='me',
            id=msg_id,
            body={'addLabelIds': [label_id]}
        ).execute()

    except Exception as e:
        print("❌ Label Error:", e)

# -------- AGENT LOOP -------- #
def run_agent():
    print("🚀 Agent started")

    service = authenticate_gmail()
    print("✅ Gmail authenticated")

    messages = get_emails(service)
    print(f"📬 Found {len(messages)} emails")

    if not messages:
        print("⚠️ No emails found")
        return

    for msg in messages:
        msg_id = msg['id']
        print(f"\n➡ Processing email ID: {msg_id}")

        content = get_email_content(service, msg_id)

        if not content:
            print("⚠️ Empty email content")
            continue

        print("🤖 Classifying...")
        category = classify_email(content)

        print(f"🏷 Category: {category}")

        apply_label(service, msg_id, category)

    print("\n✅ Agent finished")

# -------- RUN -------- #
if __name__ == "__main__":
    run_agent()
