"""Map Apify YouTube transcript Actor payloads onto PrepPulse's extractor."""

from __future__ import annotations

import re
from typing import Any

DEFAULT_YOUTUBE_ACTOR_ID = "johnvc~YoutubeTranscripts"


def apify_transcript_input(youtube_url: str) -> dict[str, Any]:
    """Build the request body for the default YouTube transcript Actor.

    Args:
        youtube_url: Watch, Shorts, embed, or youtu.be URL.

    Returns:
        Actor input with ``youtube_url``, English language preference, and
        plain-text output. The structured ``non_timestamped`` field is always
        present on this Actor even when ``output_formats`` is empty.
    """
    return {
        "youtube_url": youtube_url,
        "languages": ["en"],
        "output_formats": ["text"],
    }


def extract_transcript_payload(apify_response: Any) -> tuple[str, str]:
    """Extract transcript text and title from different Apify response shapes.

    Prefers ``non_timestamped`` and ``title`` (johnvc/YoutubeTranscripts), then
    the shapes this mindmap route already accepted (``transcript``,
    ``captions``, ``text``, ``videoTitle``).

    Args:
        apify_response: Dataset items list or a single item.

    Returns:
        Tuple of (transcript text truncated to 6000 chars, video title).

    Raises:
        ValueError: If no transcript text can be found.
    """
    items = apify_response if isinstance(apify_response, list) else [apify_response]
    transcript_text = ""
    video_title = "YouTube Video"

    for item in items:
        data = item if isinstance(item, dict) else {"text": str(item)}

        if isinstance(data, list):
            transcript_text += " ".join(
                str(entry.get("text") if isinstance(entry, dict) else entry)
                for entry in data
                if entry
            ) + " "

        if isinstance(data.get("non_timestamped"), str) and data["non_timestamped"].strip():
            transcript_text += data["non_timestamped"] + " "
            if data.get("title"):
                video_title = str(data.get("title"))
            continue

        if isinstance(data.get("transcript"), str):
            transcript_text += data["transcript"] + " "
        elif isinstance(data.get("transcript"), list):
            transcript_text += " ".join(
                str(entry.get("text") if isinstance(entry, dict) else entry)
                for entry in data["transcript"]
                if entry
            ) + " "

        if isinstance(data.get("captions"), list):
            transcript_text += " ".join(
                str(entry.get("text") if isinstance(entry, dict) else entry)
                for entry in data["captions"]
                if entry
            ) + " "

        if isinstance(data.get("text"), str):
            transcript_text += data["text"] + " "

        if data.get("title"):
            video_title = str(data.get("title"))
        if data.get("videoTitle"):
            video_title = str(data.get("videoTitle"))

    if not transcript_text.strip():
        def extract_text_deep(obj):
            if isinstance(obj, dict):
                return " ".join(
                    [
                        (value if key == "text" and isinstance(value, str) else extract_text_deep(value))
                        for key, value in obj.items()
                    ]
                )
            if isinstance(obj, list):
                return " ".join(extract_text_deep(entry) for entry in obj)
            return ""

        transcript_text = " ".join(extract_text_deep(item) for item in items)

    cleaned = re.sub(r"\s+", " ", transcript_text).strip()
    if not cleaned:
        raise ValueError("Could not extract transcript from this YouTube video.")

    return cleaned[:6000], video_title
