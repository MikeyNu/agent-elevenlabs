"""Offline regression cases for speech preflight. No API access is required."""

import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path

from speech_preflight import validate_job


def tts(**overrides):
    job = {"route": "tts", "model_id": "eleven_v4", "voice_id": "voice123abc",
           "text": "[warmly] Welcome back. Let's get started."}
    job.update(overrides)
    return job


def codes(result, kind="errors"):
    return {item["code"] for item in result[kind]}


class SpeechPreflightTests(unittest.TestCase):
    def test_v4_accepts_continuous_stability_without_mutation(self):
        job = tts(voice_settings={"stability": 0.37, "similarity_boost": 0.8})
        original = copy.deepcopy(job)
        self.assertTrue(validate_job(job)["ok"])
        self.assertEqual(job, original)

    def test_model_and_route_must_be_explicit_and_typed(self):
        for patch in ({"model_id": "eleven_v5"}, {"model_id": []},
                      {"route": "websocket"}, {"route": []}):
            with self.subTest(patch=patch):
                self.assertFalse(validate_job(tts(**patch))["ok"])

    def test_non_object_job_is_rejected(self):
        for job in (None, [], "hello", 1):
            self.assertIn("invalid_job", codes(validate_job(job)))

    def test_no_spoken_content_and_nonstring_text(self):
        for text in ("", "   ", "[laughs] [pause]", "...!", None, 24, []):
            with self.subTest(text=text):
                self.assertFalse(validate_job(tts(text=text))["ok"])

    def test_non_latin_speech_passes(self):
        for text in ("你好，欢迎回来。", "مرحباً بك مرة أخرى.", "Sanibonani, siyabonga."):
            result = validate_job(tts(text=text))
            self.assertTrue(result["ok"])
            self.assertGreater(result["metrics"]["word_estimate"], 0)

    def test_missing_and_placeholder_voice(self):
        for voice in (None, "", "YOUR_VOICE_ID", "SELECTED_VOICE_ID", "<voice_id>", "{{voice}}", "a b"):
            with self.subTest(voice=voice):
                self.assertFalse(validate_job(tts(voice_id=voice))["ok"])

    def test_nested_reversed_empty_and_multiline_tags(self):
        for text in ("[calm [softly] voice] Hello.", "]Hello[", "[] Hello.", "[ ] Hello.", "[very\nsoftly] Hello."):
            with self.subTest(text=text):
                self.assertIn("unbalanced_tags", codes(validate_job(tts(text=text))))

    def test_top_level_settings_do_not_escape_validation(self):
        self.assertIn("misplaced_setting", codes(validate_job(tts(speed=0.85))))
        self.assertIn("unvalidated_fields", codes(validate_job(tts(unknown_field="do not echo")), "warnings"))

    def test_dialogue_future_text_is_checked(self):
        job = {"route": "dialogue", "model_id": "eleven_v4", "inputs": [{"text": "Hello.", "voice_id": "speaker1"}], "future_text": "After."}
        self.assertTrue(validate_job(job)["ok"])
        job["future_text"] = "a" * 101
        self.assertIn("dialogue_context_limit", codes(validate_job(job)))
        job["future_text"] = "After."
        job["next_text"] = "Another future."
        self.assertIn("ambiguous_context", codes(validate_job(job)))
        self.assertIn("wrong_context_field", codes(validate_job(tts(future_text="After."))))

    def test_legacy_speaker_boost_requires_surface_check(self):
        result = validate_job(tts(model_id="eleven_flash_v2_5", voice_settings={"use_speaker_boost": True}))
        self.assertIn("verify_speaker_boost", codes(result, "warnings"))

    def test_unresolved_template_in_text_is_rejected(self):
        for text in ("Hi {{name}}.", "Call [YOUR PHONE NUMBER].", "Hello ${person}."):
            self.assertIn("unresolved_placeholder", codes(validate_job(tts(text=text))))

    def test_v4_exact_character_boundary_counts_tags(self):
        self.assertTrue(validate_job(tts(text="a" * 10000))["ok"])
        self.assertIn("text_limit", codes(validate_job(tts(text="a" * 10001))))
        self.assertIn("text_limit", codes(validate_job(tts(text="[warmly]" + "a" * 10000))))

    def test_v3_and_flash_character_boundaries(self):
        for model, limit in (("eleven_v3", 5000), ("eleven_flash_v2_5", 40000)):
            self.assertTrue(validate_job(tts(model_id=model, text="a" * limit))["ok"])
            self.assertIn("text_limit", codes(validate_job(tts(model_id=model, text="a" * (limit + 1)))))

    def test_v4_and_v3_reject_ssml(self):
        for model in ("eleven_v4", "eleven_v3"):
            for text in ('Hello. <break time="1.5s"/> Welcome.', '<phoneme ph="hi">Hi</phoneme>.'):
                self.assertIn("unsupported_ssml", codes(validate_job(tts(model_id=model, text=text))))

    def test_legacy_break_bounds(self):
        self.assertTrue(validate_job(tts(model_id="eleven_multilingual_v2", text='Wait. <break time="3s"/> Yes.'))["ok"])
        for time in ("3.1s", "1500ms", "0s", "many"):
            result = validate_job(tts(model_id="eleven_multilingual_v2", text='Wait. <break time="' + time + '"/> Yes.'))
            self.assertIn("invalid_break", codes(result))

    def test_legacy_audio_tags_warn_without_rewriting(self):
        self.assertIn("legacy_brackets", codes(validate_job(tts(model_id="eleven_multilingual_v2")), "warnings"))

    def test_parentheses_and_exact_pause_are_review_cues(self):
        result = validate_job(tts(text="(softly) Welcome. [pause 1.5s] Stay a while."))
        self.assertTrue(result["ok"])
        self.assertTrue({"parentheses_are_text", "unverified_pause_duration", "approximate_pause"} <= codes(result, "warnings"))

    def test_malformed_tags_are_rejected(self):
        for text in ("[warmly Hello.", "Hello. ]", "[[warmly]] Hello."):
            self.assertIn("unbalanced_tags", codes(validate_job(tts(text=text))))

    def test_heavy_tags_caps_and_ellipses_warn(self):
        result = validate_job(tts(text="[warmly] [sad] [happy] [sighs] [softly] THIS... IS... VERY... LOUD."))
        self.assertTrue({"dense_tags", "heavy_capitalization", "many_ellipses"} <= codes(result, "warnings"))

    def test_v4_settings_reject_legacy_fields(self):
        for key in ("speed", "style", "use_speaker_boost", "made_up"):
            self.assertIn("unsupported_setting", codes(validate_job(tts(voice_settings={key: 1}))))
        self.assertIn("setting_alias", codes(validate_job(tts(voice_settings={"similarity": 0.5}))))

    def test_settings_types_ranges_and_nonfinite_values(self):
        for value in (True, "0.5", [], float("nan"), float("inf"), -0.1, 1.1, 10 ** 400):
            with self.subTest(value=value):
                self.assertFalse(validate_job(tts(voice_settings={"stability": value}))["ok"])
        self.assertIn("invalid_settings", codes(validate_job(tts(voice_settings=[]))))

    def test_v3_nonstandard_stability_requires_verification(self):
        result = validate_job(tts(model_id="eleven_v3", voice_settings={"stability": 0.25}))
        self.assertIn("verify_v3_stability", codes(result, "warnings"))
        self.assertIn("unsupported_setting", codes(validate_job(tts(model_id="eleven_v3", voice_settings={"similarity_boost": 0.5}))))

    def test_legacy_speed_range_is_conservative_warning(self):
        result = validate_job(tts(model_id="eleven_flash_v2_5", voice_settings={"speed": 1.3}))
        self.assertTrue(result["ok"])
        self.assertIn("verify_speed_range", codes(result, "warnings"))
        self.assertIn("invalid_speed", codes(validate_job(tts(model_id="eleven_flash_v2_5", voice_settings={"speed": 0}))))
        self.assertIn("invalid_setting_type", codes(validate_job(tts(model_id="eleven_flash_v2_5", voice_settings={"use_speaker_boost": 1}))))

    def test_turbo_requires_unchecked_agent_or_websocket_surface(self):
        self.assertIn("unsupported_route", codes(validate_job(tts(model_id="eleven_v4_turbo"))))
        result = validate_job(tts(route="agent", model_id="eleven_v4_turbo"))
        self.assertTrue(result["ok"])
        self.assertIn("agent_schema_unchecked", codes(result, "warnings"))

    def test_dialogue_speaker_limit_and_reliability_budget(self):
        job = {"route": "dialogue", "model_id": "eleven_v4", "inputs": [
            {"text": "Welcome.", "voice_id": "speaker" + str(i)} for i in range(10)]}
        self.assertTrue(validate_job(job)["ok"])
        job["inputs"].append({"text": "Hi.", "voice_id": "speaker11"})
        self.assertIn("too_many_voices", codes(validate_job(job)))
        job["inputs"] = [{"text": "a" * 2000, "voice_id": "speaker1"}]
        self.assertTrue(validate_job(job)["ok"])
        job["inputs"][0]["text"] += "b"
        self.assertIn("dialogue_reliability_budget", codes(validate_job(job)))

    def test_dialogue_invalid_inputs_and_models(self):
        for inputs in (None, {}, [], ["hello"], [{"text": "Hello."}]):
            self.assertFalse(validate_job({"route": "dialogue", "model_id": "eleven_v4", "inputs": inputs})["ok"])
        self.assertIn("unsupported_route", codes(validate_job({"route": "dialogue", "model_id": "eleven_flash_v2_5", "inputs": []})))

    def test_request_stitching_limits_and_v3_block(self):
        self.assertTrue(validate_job(tts(previous_request_ids=["a", "b", "c"]))["ok"])
        self.assertIn("request_id_limit", codes(validate_job(tts(previous_request_ids=["a"] * 4))))
        self.assertIn("invalid_request_ids", codes(validate_job(tts(previous_request_ids="a"))))
        self.assertIn("unsupported_stitching", codes(validate_job(tts(model_id="eleven_v3", previous_text="Before."))))
        self.assertIn("unsupported_stitching", codes(validate_job(tts(model_id="eleven_v3", next_request_ids=["later"]))))

    def test_dialogue_context_mapping_and_limit(self):
        job = {"route": "dialogue", "model_id": "eleven_v4", "inputs": [{"text": "Hi.", "voice_id": "speaker1"}], "next_text": "After."}
        self.assertIn("dialogue_context_mapping", codes(validate_job(job), "warnings"))
        job["next_text"] = "a" * 101
        self.assertIn("dialogue_context_limit", codes(validate_job(job)))

    def test_seed_is_uint32_not_boolean(self):
        for seed in (0, 4294967295, None):
            self.assertTrue(validate_job(tts(seed=seed))["ok"])
        for seed in (True, -1, 4294967296, 1.0, "1"):
            self.assertIn("invalid_seed", codes(validate_job(tts(seed=seed))))

    def test_dictionary_types_limits_and_pinned_version(self):
        locator = {"pronunciation_dictionary_id": "dictionary123", "version_id": "version456"}
        self.assertTrue(validate_job(tts(pronunciation_dictionary_locators=[locator]))["ok"])
        self.assertIn("dictionary_limit", codes(validate_job(tts(pronunciation_dictionary_locators=[locator] * 4))))
        for value in ({}, ["id"], [{"id": "wrong_key"}]):
            self.assertFalse(validate_job(tts(pronunciation_dictionary_locators=value))["ok"])
        self.assertIn("unpinned_dictionary", codes(validate_job(tts(pronunciation_dictionary_locators=[{"pronunciation_dictionary_id": "dict123"}])), "warnings"))

    def test_language_and_normalization_types(self):
        self.assertIn("invalid_language", codes(validate_job(tts(language_code=[]))))
        self.assertIn("invalid_normalization", codes(validate_job(tts(apply_text_normalization=[]))))
        self.assertIn("unsupported_language_enforcement", codes(validate_job(tts(model_id="eleven_multilingual_v2", language_code="en")), "warnings"))

    def test_metrics_exclude_tags_from_spoken_count(self):
        result = validate_job(tts(text="[warmly] Hello there."))
        self.assertEqual(result["metrics"]["word_estimate"], 2)
        self.assertEqual(result["metrics"]["characters"], len("[warmly] Hello there."))
        self.assertEqual(result["metrics"]["spoken_characters"], len(" Hello there."))

    def test_diagnostics_do_not_echo_sensitive_values(self):
        secret = "private_secret_value_123"
        result = validate_job(tts(model_id=secret, text="Call " + secret, voice_settings={secret: secret}))
        self.assertNotIn(secret, json.dumps(result))

    def test_cli_exit_codes_and_invalid_json_redaction(self):
        script = str(Path(__file__).with_name("speech_preflight.py"))
        for data, status in ((json.dumps(tts()), 0), ('{"secret":"private123",broken}', 2), ('{"text": NaN}', 2)):
            run = subprocess.run([sys.executable, script, "-"], input=data, text=True, capture_output=True)
            self.assertEqual(run.returncode, status)
            result = json.loads(run.stdout)
            self.assertEqual(result["ok"], status == 0)
            self.assertNotIn("private123", run.stdout + run.stderr)


if __name__ == "__main__":
    unittest.main()
