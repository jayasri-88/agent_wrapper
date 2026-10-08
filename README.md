# 📚 StudyMate Agent

A friendly AI-powered study assistant for engineering students, built with Google Gemini and FastAPI.

## Features

- **Calculator** — evaluates math expressions safely (no guessing)
- **Wikipedia Search** — looks up factual summaries on any topic
- **Current Time** — returns the current date and time
- **Notes** — save and list study notes across a session

## Project Structure

```
studymate-agent/
├── app/
│   ├── agent.py       # Gemini client, system prompt, chat session factory
│   ├── main.py        # FastAPI routes (/chat, /health, /)
│   └── tools.py       # Calculator, Wikipedia, time, and notes tools
├── static/
│   └── index.html     # Chat UI
├── .env               # API keys (not committed)
├── requirements.txt
└── test_agent.py
```

## Setup

1. **Clone the repo and create a virtual environment**
   ```bash
   git clone <repo-url>
   cd studymate-agent
   python -m venv venv
   venv\Scripts\activate      # Windows
   # source venv/bin/activate  # macOS/Linux
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**

   Create a `.env` file in the project root:
   ```
   GEMINI_API_KEY=your_api_key_here
   GEMINI_MODEL=gemini-3.8-flash
   ```
   Get your API key from [Google AI Studio](https://aistudio.google.com/).

4. **Run the server**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Open the chat UI**

   Navigate to [http://localhost:8000](http://localhost:8000) in your browser.

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/chat` | Send a message, get a reply |
| GET | `/health` | Health check |
| GET | `/` | Chat UI |

### POST `/chat`
```json
{
  "session_id": "abc123",
  "message": "What is Ohm's law?"
}
```
Response:
```json
{
  "reply": "Ohm's law states that V = IR ..."
}
```

## Notes

- Each unique `session_id` maintains its own conversation memory.
- Notes are persisted to `notes.json` in the project root.
- Never commit your `.env` file — it's listed in `.gitignore`.
