#!/usr/bin/env python3
"""Check an ElevenLabs speech planning job without generating or rewriting audio.

Usage: python scripts/speech_preflight.py job.json
Use '-' to read JSON from stdin. Exit 0 means no errors, not audible approval.
The job envelope is not an API request: route and normalized voice_settings
must be mapped to the selected endpoint's current schema before submission.
Only Python's standard library is required. No network calls are made.
"""

import argparse
import json
import math
import re
import sys
from pathlib import Path


REVIEWED_DATE = "2026-11-18"
MODELS = {
    "eleven_v4": (10000, "v4"),
    "eleven_v4_turbo": (None, "v4"),
    "eleven_v3": (5000, "v3"),
    "eleven_multilingual_v2": (10000, "legacy"),
    "eleven_flash_v2_5": (40000, "legacy"),
    "eleven_flash_v2": (30000, "legacy"),
    "eleven_turbo_v2_5": (40000, "legacy"),
}
TAG = re.compile(r"\[[^\[\]\r\n]*\]")
XML = re.compile(r"</?[A-Za-z][^>]*>")
WORD = re.compile(r"[^\W_]+(?:['\u2019][^\W_]+)*", re.UNICODE)
PLACEHOLDER = re.compile(
    r"\{\{[^}]+\}\}|\$\{[^}]+\}|"
    r"\[(?:INSERT\b|YOUR\b|PLACEHOLDER\b|TODO\b|TBD\b)[^\]]*\]|"
    r"\b(?:YOUR[_ -]VOICE[_ -]ID|YOUR[_ -]API[_ -]KEY|VOICE_ID_HERE)\b",
    re.IGNORECASE,
)
ID_PLACEHOLDERS = {
    "voice_id", "your_voice_id", "your-voice-id", "voice-id", "replace_me",
    "placeholder", "todo", "tbd", "your voice id", "your-id", "selected_voice_id",
}
JOB_FIELDS = {
    "route", "model_id", "voice_id", "text", "inputs", "voice_settings",
    "previous_request_ids", "next_request_ids", "previous_text", "next_text",
    "future_text", "pronunciation_dictionary_locators", "seed",
    "apply_text_normalization", "language_code",
}
SETTING_FIELDS = {"stability", "similarity", "similarity_boost", "style", "speed", "use_speaker_boost"}
LIMITATIONS = [
    "This is a planning-job check, not complete endpoint or agent-schema validation.",
    "Account access, model availability, voice identity, cost, and audio are not checked.",
    "Word counts are rough estimates, especially for languages without word spaces.",
    "Warnings are review cues. This tool does not rewrite text or prove natural delivery.",
]


def validate_job(job):
    """Return safe diagnostics; never include source text or credential values."""
    result = {
        "ok": False, "errors": [], "warnings": [],
        "metrics": {"characters": 0, "spoken_characters": 0,
                    "word_estimate": 0, "text_items": 0},
        "capabilities_reviewed": REVIEWED_DATE, "limitations": LIMITATIONS[:],
    }

    def issue(level, code, path, message):
        result[level].append({"code": code, "path": path, "message": message})

    def error(code, path, message):
        issue("errors", code, path, message)

    def warn(code, path, message):
        issue("warnings", code, path, message)

    def valid_id(value, path):
        if not isinstance(value, str) or not value.strip():
            error("missing_id", path, "Supply a nonempty ID from the intended workspace.")
            return False
        if value.strip().lower() in ID_PLACEHOLDERS or PLACEHOLDER.search(value):
            error("placeholder_id", path, "Resolve the placeholder before generation.")
            return False
        if any(c in value for c in "<>[]{}") or any(c.isspace() for c in value):
            error("invalid_id", path, "Use a retrieved ID without markup or whitespace.")
            return False
        return True

    if not isinstance(job, dict):
        error("invalid_job", "$", "The job must be a JSON object.")
        return result
    if set(job) - JOB_FIELDS - SETTING_FIELDS:
        warn("unvalidated_fields", "$", "Additional fields are outside this planning schema; validate them against the actual endpoint.")
    if set(job) & SETTING_FIELDS:
        error("misplaced_setting", "$", "Place supported voice controls inside voice_settings; top-level controls are not checked as settings.")
    route = job.get("route")
    model = job.get("model_id")
    if not isinstance(route, str) or route not in {"tts", "dialogue", "agent"}:
        error("invalid_route", "route", "Use tts, dialogue, or agent.")
        route = None
    if not isinstance(model, str) or model not in MODELS:
        error("unknown_model", "model_id", "Select a documented model or refresh capabilities first.")
        model = None
    limit, family = MODELS.get(model, (None, None))
    if model == "eleven_v4_turbo" and route != "agent":
        error("unsupported_route", "route", "v4 Turbo needs an agent or dialogue WebSocket; this tool does not validate WebSocket jobs.")
    if route == "dialogue" and model not in {"eleven_v4", "eleven_v3"}:
        error("unsupported_route", "model_id", "This dialogue REST preflight supports v4 and v3 only.")
    if route == "agent":
        warn("agent_schema_unchecked", "route", "Check Custom versus native Realtime mode, the live agent schema, and turn settings separately.")

    items = []
    if route == "dialogue":
        inputs = job.get("inputs")
        voices = set()
        if not isinstance(inputs, list) or not inputs:
            error("invalid_inputs", "inputs", "Supply a nonempty list of text and voice_id objects.")
        else:
            for index, entry in enumerate(inputs):
                path = "inputs[{}]".format(index)
                if not isinstance(entry, dict):
                    error("invalid_input", path, "Each dialogue input must be an object.")
                    continue
                if valid_id(entry.get("voice_id"), path + ".voice_id"):
                    voices.add(entry["voice_id"])
                items.append((path + ".text", entry.get("text")))
            if len(voices) > 10:
                error("too_many_voices", "inputs", "Dialogue REST allows at most ten unique voice IDs.")
    elif route in {"tts", "agent"}:
        if route == "tts" or "voice_id" in job:
            valid_id(job.get("voice_id"), "voice_id")
        items.append(("text", job.get("text")))

    for path, text in items:
        if not isinstance(text, str):
            error("invalid_text", path, "Speech text must be a string.")
            continue
        tags = TAG.findall(text)
        spoken = XML.sub("", TAG.sub("", text))
        words = WORD.findall(spoken)
        metrics = result["metrics"]
        metrics["characters"] += len(text)
        metrics["spoken_characters"] += len(spoken)
        metrics["word_estimate"] += len(words)
        metrics["text_items"] += 1
        if not any(c.isalnum() for c in spoken):
            error("empty_speech", path, "Include spoken words; this checker does not cover sound-only jobs.")
        if PLACEHOLDER.search(text):
            error("unresolved_placeholder", path, "Resolve template placeholders before synthesis.")
        if re.search(r"[\[\]]", TAG.sub("", text)) or any(not tag[1:-1].strip() for tag in tags):
            error("unbalanced_tags", path, "Repair unmatched, nested, empty, or multiline audio tags.")
        if family in {"v4", "v3"} and XML.search(text):
            error("unsupported_ssml", path, "This model does not support SSML; use speech text and supported audio tags.")
        if family == "legacy" and tags:
            warn("legacy_brackets", path, "This model does not support audio tags; bracketed directions can be spoken aloud.")
        if re.search(r"\([^)]*\)", text):
            warn("parentheses_are_text", path, "Parentheses are ordinary text, not a reliable performance-control syntax.")
        if any(re.search(r"\bpause\b.*\d|\d.*\bpause\b", tag, re.I) for tag in tags):
            warn("unverified_pause_duration", path, "Numeric pause tags do not promise exact timing; measure or edit the audio.")
        if any(re.search(r"\bpause\b", tag, re.I) for tag in tags):
            warn("approximate_pause", path, "Audio-tag pauses are approximate and require listening or measurement.")
        if len(tags) >= 5 and len(tags) > max(1, len(words)) / 6:
            warn("dense_tags", path, "Many delivery tags may overdirect this passage; audition a simpler version.")
        if len(re.findall(r"\.{3,}|\u2026", text)) >= 3:
            warn("many_ellipses", path, "Repeated ellipses may introduce unwanted hesitation.")
        caps = [word for word in words if len(word) >= 3 and word.isupper()]
        if len(caps) >= 3 and len(caps) > len(words) / 3:
            warn("heavy_capitalization", path, "Heavy capitalization may become shouting or letter spelling.")
        if re.search(r"\d|https?://|www\.", spoken):
            warn("audition_normalization", path, "Audition numbers, identifiers, dates, and links without silently changing their meaning.")
        if family == "legacy":
            for pause in re.findall(r"<break\b[^>]*>", text, re.I):
                match = re.search(r'''time\s*=\s*["']([0-9]+(?:\.[0-9]+)?)s["']''', pause, re.I)
                if not match or not 0 < float(match.group(1)) <= 3:
                    error("invalid_break", path, "Use a break time in seconds greater than zero and no longer than three seconds.")
            if re.search(r"<phoneme\b", text, re.I) and model != "eleven_flash_v2":
                warn("verify_phoneme_support", path, "Do not infer phoneme support from general SSML support; verify this model and language.")
    count = result["metrics"]["characters"]
    if route == "tts" and limit is not None and count > limit:
        error("text_limit", "text", "Text exceeds the documented per-request character limit for this model.")
    if route == "dialogue" and count > 2000:
        error("dialogue_reliability_budget", "inputs", "Split below the conservative 2000-character total dialogue budget; longer requests may truncate or fail.")

    settings = job.get("voice_settings")
    if settings is not None:
        if not isinstance(settings, dict):
            error("invalid_settings", "voice_settings", "Voice settings must be an object or null.")
        else:
            allowed = ({"stability", "similarity_boost"} if family == "v4" else
                       {"stability"} if family == "v3" else
                       {"stability", "similarity_boost", "style", "speed", "use_speaker_boost"})
            for key, value in settings.items():
                if key == "similarity":
                    error("setting_alias", "voice_settings", "This job uses REST naming: similarity_boost, not the connector alias similarity.")
                    continue
                if key not in allowed:
                    error("unsupported_setting", "voice_settings", "A setting is unknown or unsupported for this model; inspect the applicable schema.")
                    continue
                path = "voice_settings." + key
                if value is None:
                    continue
                if key == "use_speaker_boost":
                    if not isinstance(value, bool):
                        error("invalid_setting_type", path, "Speaker boost must be a boolean.")
                    if model != "eleven_multilingual_v2":
                        warn("verify_speaker_boost", path, "Speaker boost availability varies by model and surface; verify before sending this field.")
                    continue
                if type(value) not in (int, float) or (type(value) is float and not math.isfinite(value)):
                    error("invalid_number", path, "Use a finite numeric value, not a boolean or string.")
                elif key == "speed":
                    if value <= 0:
                        error("invalid_speed", path, "Speed must be positive.")
                    elif not 0.7 <= value <= 1.2:
                        warn("verify_speed_range", path, "This value is outside the conservative 0.7 to 1.2 range; check the model and surface schema.")
                elif not 0 <= value <= 1:
                    error("setting_range", path, "Use a value from zero to one.")
                elif family == "v3" and key == "stability" and value not in (0, 0.5, 1):
                    warn("verify_v3_stability", path, "v3 commonly uses 0, 0.5, or 1; confirm the current surface before using another value.")

    for field in ("previous_request_ids", "next_request_ids"):
        value = job.get(field)
        if value is not None:
            if not isinstance(value, list):
                error("invalid_request_ids", field, "Use a list of up to three completed request IDs.")
            else:
                if len(value) > 3:
                    error("request_id_limit", field, "Use at most three request IDs.")
                for index, item in enumerate(value):
                    valid_id(item, "{}[{}]".format(field, index))
            if value and family == "v3":
                error("unsupported_stitching", field, "Request stitching is not supported for v3.")
            elif value:
                warn("verify_stitching_context", field, "Use completed matching-model requests within two hours; retained history is required.")
    if "future_text" in job and route != "dialogue":
        error("wrong_context_field", "future_text", "future_text belongs to dialogue; use next_text for supported TTS conditioning.")
    if job.get("next_text") is not None and job.get("future_text") is not None:
        error("ambiguous_context", "$", "Choose one forward-context field, not both next_text and future_text.")
    for field in ("previous_text", "next_text", "future_text"):
        value = job.get(field)
        if value is not None and not isinstance(value, str):
            error("invalid_context", field, "Context must be text or null.")
        elif value:
            if family == "v3":
                error("unsupported_stitching", field, "Do not rely on text context stitching for v3.")
            if route == "dialogue":
                if len(value) > 100:
                    error("dialogue_context_limit", field, "Dialogue REST context fields are limited to 100 characters.")
                if field == "next_text":
                    warn("dialogue_context_mapping", field, "Map this planning field to future_text in the dialogue REST payload.")
    locators = job.get("pronunciation_dictionary_locators")
    if locators is not None:
        if not isinstance(locators, list):
            error("invalid_locators", "pronunciation_dictionary_locators", "Use a list of dictionary locator objects.")
        else:
            if len(locators) > 3:
                error("dictionary_limit", "pronunciation_dictionary_locators", "Use at most three dictionaries per request.")
            for index, locator in enumerate(locators):
                path = "pronunciation_dictionary_locators[{}]".format(index)
                if not isinstance(locator, dict):
                    error("invalid_locator", path, "Each locator must be an object.")
                    continue
                valid_id(locator.get("pronunciation_dictionary_id"), path + ".pronunciation_dictionary_id")
                if locator.get("version_id") is None:
                    warn("unpinned_dictionary", path, "Pin a dictionary version for reproducible pronunciation.")
                else:
                    valid_id(locator["version_id"], path + ".version_id")
    if "seed" in job and job["seed"] is not None:
        seed = job["seed"]
        if type(seed) is not int or not 0 <= seed <= 4294967295:
            error("invalid_seed", "seed", "Seed must be an integer between zero and 4294967295.")
    normalization = job.get("apply_text_normalization", "auto")
    if not isinstance(normalization, str) or normalization not in {"auto", "on", "off"}:
        error("invalid_normalization", "apply_text_normalization", "Use auto, on, or off.")
    language = job.get("language_code")
    if language is not None:
        if not isinstance(language, str) or not language.strip():
            error("invalid_language", "language_code", "Use a supported language code from the current endpoint schema.")
        else:
            warn("verify_language_support", "language_code", "Verify model language support and the endpoint's code format; this checker has no live catalog.")
            if model == "eleven_multilingual_v2":
                warn("unsupported_language_enforcement", "language_code", "Multilingual v2 does not support language_code enforcement.")
    result["ok"] = not result["errors"]
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("job", help="Path to a speech planning JSON file, or - for stdin")
    args = parser.parse_args(argv)
    try:
        raw = sys.stdin.read() if args.job == "-" else Path(args.job).read_text(encoding="utf-8")
        job = json.loads(raw, parse_constant=lambda _: (_ for _ in ()).throw(ValueError()))
    except (OSError, UnicodeError, ValueError):
        result = validate_job(None)
        result["errors"] = [{"code": "invalid_input", "path": "$", "message": "Could not read valid UTF-8 JSON. Input details are withheld."}]
    else:
        result = validate_job(job)
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    sys.exit(main())
