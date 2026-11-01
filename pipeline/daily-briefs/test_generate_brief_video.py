import contextlib
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import AsyncMock, call, patch


spec = importlib.util.spec_from_file_location(
    "generate_brief_video", Path(__file__).with_name("generate_brief_video.py")
)
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)


class GenerateTtsTests(unittest.IsolatedAsyncioTestCase):
    async def test_success_uses_default_voice_without_retry(self):
        with (
            patch.object(generator.edge_tts, "Communicate") as communicate,
            patch.object(generator.asyncio, "sleep", new_callable=AsyncMock) as sleep,
        ):
            communicate.return_value.save = AsyncMock()

            await generator.generate_tts("Daily news", "audio.mp3")

            communicate.assert_called_once_with("Daily news", generator.TTS_VOICE)
            communicate.return_value.save.assert_awaited_once_with("audio.mp3")
            sleep.assert_not_awaited()

    async def test_no_audio_retries_with_fresh_request_and_preserves_voice(self):
        for voice in (generator.TTS_VOICE, generator.TTS_VOICE_HE):
            with self.subTest(voice=voice), tempfile.TemporaryDirectory() as directory:
                output = Path(directory) / "audio.mp3"
                first = AsyncMock()
                second = AsyncMock()

                async def fail(path):
                    Path(path).write_bytes(b"partial")
                    raise generator.edge_tts.exceptions.NoAudioReceived("No audio")

                async def succeed(path):
                    self.assertFalse(Path(path).exists())
                    Path(path).write_bytes(b"complete")

                first.save.side_effect = fail
                second.save.side_effect = succeed
                with (
                    patch.object(
                        generator.edge_tts, "Communicate", side_effect=[first, second]
                    ) as communicate,
                    patch.object(
                        generator.asyncio, "sleep", new_callable=AsyncMock
                    ) as sleep,
                    contextlib.redirect_stderr(io.StringIO()) as errors,
                ):
                    await generator.generate_tts("Daily news", output, voice=voice)

                self.assertEqual(
                    communicate.call_args_list, [call("Daily news", voice)] * 2
                )
                sleep.assert_awaited_once_with(2)
                self.assertIn("retrying", errors.getvalue())
                self.assertEqual(output.read_bytes(), b"complete")

    async def test_exhausted_retries_raise_and_remove_partial_audio(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "audio.mp3"
            error = generator.edge_tts.exceptions.NoAudioReceived("No audio")

            async def fail(path):
                Path(path).write_bytes(b"partial")
                raise error

            with (
                patch.object(generator.edge_tts, "Communicate") as communicate,
                patch.object(generator.asyncio, "sleep", new_callable=AsyncMock) as sleep,
                contextlib.redirect_stderr(io.StringIO()),
            ):
                communicate.return_value.save = AsyncMock(side_effect=fail)

                with self.assertRaises(generator.edge_tts.exceptions.NoAudioReceived):
                    await generator.generate_tts("Daily news", output)

                self.assertEqual(communicate.call_count, 3)
                self.assertEqual(sleep.await_args_list, [call(2), call(4)])
                self.assertFalse(output.exists())

    async def test_file_errors_are_not_retried(self):
        with (
            patch.object(generator.edge_tts, "Communicate") as communicate,
            patch.object(generator.asyncio, "sleep", new_callable=AsyncMock) as sleep,
        ):
            communicate.return_value.save = AsyncMock(
                side_effect=PermissionError("Cannot write audio")
            )

            with self.assertRaises(PermissionError):
                await generator.generate_tts("Daily news", "audio.mp3")

            communicate.assert_called_once()
            sleep.assert_not_awaited()


if __name__ == "__main__":
    unittest.main()
