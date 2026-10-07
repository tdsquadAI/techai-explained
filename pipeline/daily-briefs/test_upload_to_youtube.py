import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


spec = importlib.util.spec_from_file_location(
    "upload_to_youtube", Path(__file__).with_name("upload_to_youtube.py")
)
uploader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(uploader)


class UploadTrackingTests(unittest.TestCase):
    def test_legacy_brief_only_suppresses_its_upload_day(self):
        tracker = {
            "ai-brief.mp4": {
                "video_id": "legacy",
                "uploaded_at": "2026-04-05T08:10:26",
            }
        }
        self.assertTrue(
            uploader.brief_already_uploaded(tracker, "ai-brief.mp4", "2026-04-05")
        )
        self.assertFalse(
            uploader.brief_already_uploaded(tracker, "ai-brief.mp4", "2026-10-06")
        )

    def test_new_brief_record_only_suppresses_its_content_day(self):
        tracker = {"2026-10-06/ai-brief.mp4": {"video_id": "new"}}
        self.assertTrue(
            uploader.brief_already_uploaded(tracker, "ai-brief.mp4", "2026-10-06")
        )
        self.assertFalse(
            uploader.brief_already_uploaded(tracker, "ai-brief.mp4", "2026-10-07")
        )
        self.assertFalse(
            uploader.brief_already_uploaded(tracker, "ai-he-brief.mp4", "2026-10-06")
        )

    def test_daily_uploads_persist_per_date_and_language_without_reuploading_series(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tracker_path = root / "upload-tracker.json"
            tracker_path.write_text(json.dumps({
                "01-ai-agents.mp4": {"video_id": "series"},
                "ai-brief.mp4": {
                    "video_id": "legacy",
                    "uploaded_at": "2026-04-05T08:10:26",
                },
            }), encoding="utf-8")
            series = root / "series"
            series.mkdir()
            (series / "01-ai-agents.mp4").touch()
            for date in ("2026-10-06", "2026-10-07"):
                output = root / "output" / date
                output.mkdir(parents=True)
                for filename in ("ai-brief.mp4", "ai-he-brief.mp4"):
                    (output / filename).touch()

            with (
                patch.object(uploader, "__file__", str(root / "upload_to_youtube.py")),
                patch.object(uploader, "TRACKER_PATH", tracker_path),
                patch.object(uploader, "check_credentials"),
                patch.object(uploader, "get_youtube_client"),
                patch.object(uploader, "upload_video", return_value="uploaded") as upload,
                contextlib.redirect_stdout(io.StringIO()),
            ):
                for date in ("2026-10-06", "2026-10-06", "2026-10-07"):
                    with patch("sys.argv", [
                        "upload_to_youtube.py", "--date", date,
                        "--topic", "ai", "--language", "both",
                        "--series-dir", str(series), "--delay", "0",
                    ]):
                        uploader.main()

            self.assertEqual(upload.call_count, 4)
            self.assertEqual(
                [call.args[4] for call in upload.call_args_list],
                ["en", "he", "en", "he"],
            )
            tracker = json.loads(tracker_path.read_text(encoding="utf-8"))
            for date in ("2026-10-06", "2026-10-07"):
                for filename in ("ai-brief.mp4", "ai-he-brief.mp4"):
                    self.assertEqual(tracker[f"{date}/{filename}"]["video_id"], "uploaded")
            self.assertEqual(tracker["01-ai-agents.mp4"]["video_id"], "series")
            self.assertEqual(tracker["ai-brief.mp4"]["video_id"], "legacy")


if __name__ == "__main__":
    unittest.main()
