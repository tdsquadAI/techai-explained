import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


spec = importlib.util.spec_from_file_location(
    "upload_to_youtube", Path(__file__).with_name("upload_to_youtube.py")
)
uploader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(uploader)


class UploadSafetyTests(unittest.TestCase):
    def test_missing_credentials_fail_without_exposing_values(self):
        with (
            patch.dict(
                os.environ, {"YOUTUBE_CLIENT_ID": "configured-client"}, clear=True
            ),
            contextlib.redirect_stderr(io.StringIO()) as errors,
        ):
            with self.assertRaises(SystemExit) as result:
                uploader.check_credentials()

        self.assertEqual(result.exception.code, 1)
        self.assertIn("YOUTUBE_REFRESH_TOKEN", errors.getvalue())
        self.assertIn("YOUTUBE_CLIENT_SECRET", errors.getvalue())
        self.assertNotIn("configured-client", errors.getvalue())

    def test_invalid_tracker_is_not_treated_as_an_empty_tracker(self):
        with tempfile.TemporaryDirectory() as directory:
            tracker_path = Path(directory) / "upload-tracker.json"
            with patch.object(uploader, "TRACKER_PATH", tracker_path):
                for contents in ("{invalid", "[]"):
                    with self.subTest(contents=contents):
                        tracker_path.write_text(contents, encoding="utf-8")
                        with self.assertRaises(ValueError):
                            uploader.load_tracker()

    def test_failed_tracker_replacement_preserves_existing_records(self):
        with tempfile.TemporaryDirectory() as directory:
            tracker_path = Path(directory) / "upload-tracker.json"
            tracker_path.write_text('{"existing": {}}', encoding="utf-8")
            with (
                patch.object(uploader, "TRACKER_PATH", tracker_path),
                patch.object(Path, "replace", side_effect=PermissionError("read only")),
            ):
                with self.assertRaises(PermissionError):
                    uploader.save_tracker({"new": {}})

            self.assertEqual(
                json.loads(tracker_path.read_text(encoding="utf-8")), {"existing": {}}
            )
            self.assertEqual(list(Path(directory).glob("*.tmp")), [])

    def test_non_quota_failure_fails_after_success_or_quota_deferral(self):
        for second_result in ("uploaded", "quota_exceeded"):
            with (
                self.subTest(second_result=second_result),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = Path(directory)
                tracker_path = root / "upload-tracker.json"
                output = root / "output" / "2026-11-10"
                output.mkdir(parents=True)
                for topic in ("dotnet", "ai"):
                    (output / f"{topic}-brief.mp4").touch()

                with (
                    patch.object(uploader, "__file__", str(root / "upload_to_youtube.py")),
                    patch.object(uploader, "TRACKER_PATH", tracker_path),
                    patch.object(uploader, "check_credentials"),
                    patch.object(uploader, "get_youtube_client"),
                    patch.object(
                        uploader, "upload_video",
                        side_effect=[RuntimeError("upload failed"), second_result],
                    ),
                    patch("sys.argv", [
                        "upload_to_youtube.py", "--date", "2026-11-10",
                        "--language", "en", "--delay", "0",
                    ]),
                    contextlib.redirect_stdout(io.StringIO()),
                    contextlib.redirect_stderr(io.StringIO()),
                ):
                    with self.assertRaises(SystemExit) as result:
                        uploader.main()

                self.assertEqual(result.exception.code, 1)
                if second_result == "uploaded":
                    tracker = json.loads(tracker_path.read_text(encoding="utf-8"))
                    self.assertEqual(
                        tracker["2026-11-10/ai-brief.mp4"]["video_id"], "uploaded"
                    )

    def test_quota_only_deferral_remains_successful(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "output" / "2026-11-10"
            output.mkdir(parents=True)
            (output / "dotnet-brief.mp4").touch()

            with (
                patch.object(uploader, "__file__", str(root / "upload_to_youtube.py")),
                patch.object(uploader, "TRACKER_PATH", root / "upload-tracker.json"),
                patch.object(uploader, "check_credentials"),
                patch.object(uploader, "get_youtube_client"),
                patch.object(uploader, "upload_video", return_value="quota_exceeded"),
                patch("sys.argv", [
                    "upload_to_youtube.py", "--date", "2026-11-10",
                    "--language", "en", "--delay", "0",
                ]),
                contextlib.redirect_stdout(io.StringIO()) as output_text,
            ):
                uploader.main()

            self.assertIn("1 deferred", output_text.getvalue())
            self.assertFalse((root / "upload-tracker.json").exists())

    def test_tracker_write_failure_stops_uploads(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "output" / "2026-11-10"
            output.mkdir(parents=True)
            for topic in ("dotnet", "ai"):
                (output / f"{topic}-brief.mp4").touch()

            with (
                patch.object(uploader, "__file__", str(root / "upload_to_youtube.py")),
                patch.object(uploader, "TRACKER_PATH", root / "upload-tracker.json"),
                patch.object(uploader, "check_credentials"),
                patch.object(uploader, "get_youtube_client"),
                patch.object(uploader, "upload_video", return_value="published") as upload,
                patch.object(uploader, "save_tracker", side_effect=OSError("disk full")),
                patch("sys.argv", [
                    "upload_to_youtube.py", "--date", "2026-11-10",
                    "--language", "en", "--delay", "0",
                ]),
                contextlib.redirect_stdout(io.StringIO()),
            ):
                with self.assertRaisesRegex(RuntimeError, "published.*Restore the record"):
                    uploader.main()
            self.assertEqual(upload.call_count, 1)


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
