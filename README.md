# Gmail-Sorting# 🤖 Agentic AI Gmail Organizer

An intelligent Gmail automation tool that uses AI to **read, classify, and organize emails automatically**.

This project demonstrates a simple **agentic AI system** that:

* Perceives emails from Gmail
* Thinks using an LLM (AI model)
* Acts by applying labels automatically

---

## 🚀 Features

* 📬 Fetch emails from Gmail API
* 🧠 AI-powered email classification
* 🏷️ Auto-label emails (Important, Work, Personal, Promotions, Spam)
* ⚡ Lightweight and easy to run locally
* 🔐 Secure OAuth 2.0 authentication

---

## 🧱 Tech Stack

* Python
* Gmail API
* OpenAI API (LLM for classification)
* OAuth 2.0 Authentication

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/agentic-gmail-ai.git
cd agentic-gmail-ai
```

---

### 2. Install dependencies

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib openai
```

---

### 3. Enable Gmail API

1. Go to Google Cloud Console
2. Create a project
3. Enable **Gmail API**
4. Create OAuth credentials (**Desktop App**)
5. Download `credentials.json` and place it in the project root

---

### 4. Configure Redirect URI

In OAuth settings, add:

```
http://localhost:8080/
```

---

### 5. Add OpenAI API Key

Update your script:

```python
OPENAI_API_KEY = "your-api-key"
```

---

### 6. Run the application

```bash
python gmail_sorting.py
```

A browser window will open for Gmail authentication.

---

## 🧠 How It Works

1. Fetch recent emails from Gmail
2. Extract email content (snippet)
3. Send content to AI model for classification
4. Apply corresponding Gmail label

---

## 🔄 Agent Workflow

```
Perception → Reasoning → Action
   ↓            ↓         ↓
Read Emails → Classify → Label Emails
```

---

## 🛠️ Project Structure

```
agentic-gmail-ai/
│
├── gmail_sorting.py
├── credentials.json
├── README.md
└── requirements.txt
```

---

## ⚠️ Common Issues

### redirect_uri_mismatch

* Ensure redirect URI is:

```
http://localhost:8080/
```

* Use:

```python
flow.run_local_server(port=8080)
```

---

### NameError: run_agent not defined

* Ensure function is defined before calling it

---

### Gmail API not enabled

* Enable Gmail API in Google Cloud Console

---

## 🚀 Future Enhancements

* 📊 Email priority scoring
* ✉️ Auto-reply system
* 🧠 Memory-based learning
* ⚡ Kafka-based real-time processing
* 🌐 Web dashboard (FastAPI + React)
* 🤖 Multi-agent architecture

---

## 🔐 Security Notes

* Do NOT commit:

  * `credentials.json`
  * `token.json`
  * API keys

Use `.gitignore` to protect sensitive data.

---

## 📌 Use Cases

* Inbox automation
* Productivity enhancement
* Email triage systems
* AI agent experimentation

---

## 🤝 Contributing

Contributions are welcome!
Feel free to fork the repo and submit a PR.

---

## 📄 License

MIT License

---

## ⭐ Support

If you found this useful, consider giving it a ⭐ on GitHub!
