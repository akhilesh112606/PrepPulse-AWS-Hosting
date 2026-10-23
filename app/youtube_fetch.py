"""Fetch YouTube transcripts with the live Apify Actor input shape."""

from __future__ import annotations

import logging
import os

import requests as http_requests
from flask import current_app

from .transcript_adapter import DEFAULT_YOUTUBE_ACTOR_ID, apify_transcript_input


def fetch_transcript_from_apify(youtube_url: str):
    """Fetch a transcript using the configured Apify Actor.

    Uses ``youtube_url`` / ``languages`` / ``output_formats`` instead of the
    old ``urls`` body, which the live Actor does not accept. Falls back to
    ``youtube-transcript-api`` the same way the original route did.

    Args:
        youtube_url: Watch, Shorts, embed, or youtu.be URL.

    Returns:
        Dataset items from Apify, or the youtube-transcript-api fallback shape.
    """
    from . import routes as routes_mod

    apify_token = current_app.config.get("APIFY_API_TOKEN") or os.getenv("APIFY_API_TOKEN")
    actor_id = current_app.config.get("APIFY_YOUTUBE_ACTOR_ID") or os.getenv(
        "APIFY_YOUTUBE_ACTOR_ID", DEFAULT_YOUTUBE_ACTOR_ID
    )

    if not apify_token:
        logging.info("APIFY_API_TOKEN missing. Falling back to youtube-transcript-api.")
        return routes_mod._fetch_transcript_from_youtube_api(youtube_url)

    url = (
        f"https://api.apify.com/v2/acts/{actor_id}/run-sync-get-dataset-items"
        f"?token={apify_token}&timeout=120"
    )
    payload = apify_transcript_input(youtube_url)

    try:
        response = http_requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=120,
        )
        response.raise_for_status()
        return response.json()
    except http_requests.RequestException as exc:
        status_code = getattr(getattr(exc, "response", None), "status_code", None)
        if status_code == 404:
            logging.warning(
                "Apify actor '%s' not found (404). Falling back to youtube-transcript-api.",
                actor_id,
            )
        else:
            logging.warning(
                "Apify transcript fetch failed. Falling back to youtube-transcript-api: %s",
                exc,
            )
        return routes_mod._fetch_transcript_from_youtube_api(youtube_url)
