# PrepPulse - AI Learning and Resource Platform

PrepPulse is a Flask-based student learning platform with AI-assisted tutoring, resource sharing, automated note generation, YouTube transcript-to-mindmap conversion, resume analysis, progress tracking, and admin moderation tools.

## What Is Live Now

- AI chatbot with RAG context from local knowledge-base files.
- Chat history APIs to load and delete user conversations.
- Instant Note Maker to generate AI notes, export PDF, and submit to resources.
- Resources module with upload, review workflow, filters, preview, download, comments, and AI refinement.
- Admin resource moderation with:
    - Pending approvals pagination (default 3 per page).
    - Live resources management (edit/delete approved resources).
    - Review comments and uploader email notifications.
- YouTube Mindmap generator using transcript extraction and Mermaid output.
- Resume upload and analysis with robust extraction fallbacks.
- Progress tracker, habits, leaderboard, onboarding, auth, and admin utilities.
- Knowledge-base refinement endpoints for adding courses, assessments, and certifications.

## Core Features

- Authentication
    - Register, login, logout, forgot/reset password via SMTP.
- AI Chatbot
    - OpenAI-based responses, optional speech synthesis, prompt-injection guards, RAG context.
- Chat History
    - Paginated history retrieval and delete endpoints.
- Notes and Resources
    - Generate notes with AI, create PDF, upload to resource review queue.
    - Resource deduplication by content hash.
    - User-owned resource edit/delete flows.
    - Resource comments and AI refinement (summary, Q and A, mindmaps).
- YouTube Mindmap
    - Transcript fetch (Apify with fallback), LLM mindmap generation, Mermaid links.
- Resume Analyzer
    - Resume parsing for PDF or DOCX and AI analysis.
- Admin Panel
    - Users, database explorer, SQL console, leaderboard, and resources moderation.
- KB Management
    - Add and search structured learning content through API.

## Tech Stack

- Backend: Flask, Python
- Database: SQLite
- AI: OpenAI APIs, Gemini (optional), Apify (optional)
- Frontend: Jinja2 templates, vanilla JavaScript, CSS
- File Processing: PyPDF2, python-docx, reportlab
- HTTP integrations: requests, youtube-transcript-api

## Project Layout

```text
AITAM/
|- run.py
|- requirements.txt
|- app/
|  |- __init__.py
|  |- db.py
|  |- routes.py
|  |- rag_pipeline.py
|  |- kb_manager.py
|  |- static/
|  |  |- css/
|  |  |- js/
|  |- templates/
|- Knowledge base/
|- data/
|  |- resources/
|  |- resumes/
|- scripts/
```

## Setup

### Prerequisites

- Python 3.9+
- SMTP credentials for password reset emails
- OpenAI key for chatbot and AI features

### Install

```bash
git clone <repo-url>
cd AITAM

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt
```

### Environment Variables

Create a .env file in the project root:

```env
SECRET_KEY=replace-with-random-secret

OPEN_API_KEY=your-openai-key

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@example.com
SMTP_PASSWORD=your-app-password
SMTP_USE_TLS=true

APIFY_API_TOKEN=optional-apify-token
APIFY_YOUTUBE_ACTOR_ID=johnvc~YoutubeTranscripts

GEMINI_API_KEY=optional-gemini-key
GEMINI_MODEL=gemini-1.5-flash
```

Important: never hardcode secrets in tracked files. Keep tokens and keys only in environment variables.

### Run

```bash
python run.py
```

App URL: http://127.0.0.1:5000

## Main Routes and APIs

### Pages

- GET /
- GET or POST /login
- GET or POST /register
- GET or POST /forgot-password
- GET or POST /reset-password/<token>
- GET or POST /onboarding
- GET /dashboard
- GET /progress
- GET /mock-tests
- GET /resume
- GET /note-maker
- GET /resources
- GET /youtube-mindmap
- GET /admin

### Chat

- POST /chat
- GET /api/chat-history
- DELETE /api/chat-history/delete
- DELETE /api/chat-history/<message_id>

### Notes

- POST /api/notes/generate
- POST /api/notes/create-pdf
- POST /api/notes/upload-to-resources

### Resources (User)

- GET /api/resources
- GET /api/resources/mine
- POST /api/resources/upload
- PUT /api/resources/<resource_id>
- DELETE /api/resources/<resource_id>
- GET /api/resources/<resource_id>/download
- GET /api/resources/<resource_id>/comments
- POST /api/resources/<resource_id>/refine
- GET /api/resources/<resource_id>/refinement

### Resources (Admin)

- GET /api/admin/resources/pending?page=1&page_size=3
- GET /api/admin/resources/live?page=1&page_size=5
- GET /api/admin/resources/stats
- PUT /api/admin/resources/<resource_id>/approve
- PUT /api/admin/resources/<resource_id>/reject
- PUT /api/admin/resources/<resource_id>
- DELETE /api/admin/resources/<resource_id>
- POST /api/admin/resources/<resource_id>/comment
- GET /api/admin/resources/<resource_id>/comments

### YouTube Mindmap

- POST /api/youtube-mindmap/generate

### Resume

- POST /api/resume/upload
- POST /api/resume/analyze
- GET /api/resume/latest
- GET /api/resume/file/<resume_id>
- GET /api/resume/file

### Progress and Tests

- GET or POST /api/mock-tests
- PUT or DELETE /api/mock-tests/<test_id>
- GET or POST /api/habits
- PUT or DELETE /api/habits/<habit_id>
- POST /api/habits/toggle
- GET /api/habits/logs
- GET /api/leaderboard

### Knowledge Base Management

- POST /api/kb/add-course
- POST /api/kb/add-assessment
- POST /api/kb/add-certification
- GET /api/kb/search
- GET /api/kb/status

## Notes for Maintainers

- Database path is configured in app.__init__ as data/preppulse.db.
- RAG vector initialization runs during app startup.
- If you update the knowledge-base JSON files, restart the app and validate KB and RAG behavior.
- A helper script exists for sqlite to postgres migration in scripts/migrate_sqlite_to_postgres.py.

## License

Built for a hackathon and ongoing internal development.
