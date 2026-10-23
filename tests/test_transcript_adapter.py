"""Offline fixtures for the YouTube mindmap transcript adapter."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

_ADAPTER_PATH = Path(__file__).resolve().parents[1] / "app" / "transcript_adapter.py"
_SPEC = importlib.util.spec_from_file_location("transcript_adapter", _ADAPTER_PATH)
_ADAPTER = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader is not None
_SPEC.loader.exec_module(_ADAPTER)

DEFAULT_YOUTUBE_ACTOR_ID = _ADAPTER.DEFAULT_YOUTUBE_ACTOR_ID
apify_transcript_input = _ADAPTER.apify_transcript_input
extract_transcript_payload = _ADAPTER.extract_transcript_payload


class TranscriptAdapterTests(unittest.TestCase):
    """Keep the mindmap route's field names when the Actor payload changes."""

    def test_default_actor_id_uses_live_slug(self) -> None:
        self.assertEqual(DEFAULT_YOUTUBE_ACTOR_ID, "johnvc~YoutubeTranscripts")

    def test_apify_input_uses_youtube_url(self) -> None:
        payload = apify_transcript_input("https://www.youtube.com/watch?v=abc")
        self.assertEqual(
            payload,
            {
                "youtube_url": "https://www.youtube.com/watch?v=abc",
                "languages": ["en"],
                "output_formats": ["text"],
            },
        )

    def test_extracts_non_timestamped_and_title(self) -> None:
        transcript, title = extract_transcript_payload(
            [
                {
                    "title": "Intro to AWS",
                    "non_timestamped": "Hello from the captions.",
                    "timestamped": [{"text": "Hello", "start": 0, "duration": 1}],
                }
            ]
        )
        self.assertEqual(transcript, "Hello from the captions.")
        self.assertEqual(title, "Intro to AWS")

    def test_extracts_legacy_transcript_list(self) -> None:
        transcript, title = extract_transcript_payload(
            [
                {
                    "videoTitle": "Legacy shape",
                    "transcript": [{"text": "First"}, {"text": "Second"}],
                }
            ]
        )
        self.assertEqual(transcript, "First Second")
        self.assertEqual(title, "Legacy shape")

    def test_truncates_to_six_thousand_chars(self) -> None:
        transcript, _title = extract_transcript_payload(
            {"non_timestamped": "x" * 7000, "title": "Long"}
        )
        self.assertEqual(len(transcript), 6000)

    def test_empty_payload_raises(self) -> None:
        with self.assertRaises(ValueError):
            extract_transcript_payload([{"title": "No captions"}])


if __name__ == "__main__":
    unittest.main()
