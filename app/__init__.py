import os
from flask import Flask
from pathlib import Path

from .db import init_db
from .transcript_adapter import DEFAULT_YOUTUBE_ACTOR_ID, extract_transcript_payload
from .youtube_fetch import fetch_transcript_from_apify

def create_app():
    app = Flask(__name__)
    app.config["DATABASE"] = str(
        Path(app.root_path).parent / "data" / "preppulse.db"
    )
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
    app.config["RESET_TOKEN_MAX_AGE"] = int(os.getenv("RESET_TOKEN_MAX_AGE", "900"))
    app.config["SMTP_HOST"] = os.getenv("SMTP_HOST", "smtp.gmail.com")
    app.config["SMTP_PORT"] = int(os.getenv("SMTP_PORT", "587"))
    app.config["SMTP_USER"] = os.getenv("SMTP_USER", "")
    app.config["SMTP_PASSWORD"] = os.getenv("SMTP_PASSWORD", "")
    app.config["SMTP_USE_TLS"] = os.getenv("SMTP_USE_TLS", "true").lower() in ("1", "true", "yes")
    app.config["OPEN_API_KEY"] = os.getenv("OPEN_API_KEY", "")
    app.config["APIFY_API_TOKEN"] = os.getenv("APIFY_API_TOKEN", "")
    app.config["APIFY_YOUTUBE_ACTOR_ID"] = os.getenv("APIFY_YOUTUBE_ACTOR_ID", DEFAULT_YOUTUBE_ACTOR_ID)
    app.config["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY", "")
    app.config["GEMINI_MODEL"] = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

    init_db(app)
    
    # Initialize RAG pipeline with knowledge base
    with app.app_context():
        try:
            from .rag_pipeline import get_rag_pipeline
            rag = get_rag_pipeline(app.config["DATABASE"])
            app.logger.info("✅ RAG Vector Database initialized successfully")
        except Exception as e:
            app.logger.warning(f"⚠️  RAG initialization: {str(e)}")

    # Import routes
    from .routes import main
    from . import routes as routes_mod
    # The mindmap helpers in routes.py still name the old Actor input. Point
    # them at the live Actor body and extractor without rewriting that module.
    routes_mod._fetch_transcript_from_apify = fetch_transcript_from_apify
    routes_mod._extract_transcript_payload = extract_transcript_payload
    app.register_blueprint(main)

    return app
