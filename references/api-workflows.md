# API and production workflows

Verified 18 November 2026. Use the connected tool schema or installed SDK signature for exact argument names. The examples are request shapes, not proof that a particular account can use a voice, model, or output tier.

## Contents

- [Choose the surface](#choose-the-surface)
- [Offline preflight](#offline-preflight)
- [TTS and dialogue requests](#tts-and-dialogue-requests)
- [Long-form continuity](#long-form-continuity)
- [Streaming](#streaming)
- [Formats, captions, and completion](#formats-captions-and-completion)
- [Failures and cost control](#failures-and-cost-control)

## Choose the surface

Prefer an available ElevenLabs connector for operations it supports. Inspect its model schema before setting parameters. A connector may use `prompt`, `voice`, or `similarity` where REST uses `text`, a path `voice_id`, or `similarity_boost`. Do not paste one surface's payload into another. Leave voice overrides out of a new connector voiceover unless needed or requested.

For code, use the official `elevenlabs` Python package or `@elevenlabs/elevenlabs-js` JavaScript package and inspect the installed version. REST can avoid SDK-version ambiguity. Keep the API key in server-side secret storage or `ELEVENLABS_API_KEY`; never in browser code or committed examples. Preserve the project's configured regional endpoint.

Discover actual models with `GET /v1/models` and check capability flags. Resolve voices through [`GET /v2/voices`](https://elevenlabs.io/docs/api-reference/voices/search), respecting pagination. Do not select a copied demo ID merely because an old example uses it.

## Offline preflight

The bundled checker accepts a **planning envelope**, not a raw API request:

```json
{
  "route": "tts",
  "model_id": "eleven_v4",
  "voice_id": "SELECTED_VOICE_ID",
  "text": "The upload is ready. [curious] Shall we open it?"
}
```

Replace `SELECTED_VOICE_ID` with an available voice before using the example. Run `python scripts/speech_preflight.py job.json` from the skill directory. Exit 0 means no detected blocking issue; exit 2 means errors. Review warnings manually. The checker never sends a request or prints the script back.

Use `route: dialogue` with `inputs: [{text, voice_id}]`. Use `route: agent` only for a speech sample and selected TTS model; this does not validate a complete agent configuration. The helper does not cover managed Realtime, WebSocket messages, Voice Changer, Dubbing, or every provider setting. Follow their dedicated schemas rather than forcing them into the envelope.

Optional fields cover supported voice settings, dictionary locators, conditioning, seed, language, and normalization. Dialogue accepts `future_text`; a planning `next_text` produces a reminder to map it to `future_text`. Do not supply both. Refer to the script's `--help` and diagnostics. Do not send the envelope's `route` field to ElevenLabs. For TTS, move `voice_id` into the URL and include only endpoint-supported fields in the body. For dialogue, use endpoint `settings` where required; do not blindly copy the envelope's `voice_settings`.

## TTS and dialogue requests

For a complete single-speaker script, use `POST /v1/text-to-speech/{voice_id}`. Set the model explicitly and specify `output_format` as a query parameter. A minimal body is:

```json
{
  "model_id": "eleven_v4",
  "text": "The upload is ready. [curious] Shall we open it?"
}
```

Do not rely on an endpoint default to select the newest model. See [Create speech](https://elevenlabs.io/docs/api-reference/text-to-speech/convert). HTTP output streaming is a separate choice from incrementally sending text over a WebSocket.

For a conversation, use `POST /v1/text-to-dialogue`, with `model_id: eleven_v4` and one `{text, voice_id}` object per turn. Keep speaker labels outside spoken text. The current endpoint caps unique voices at ten and advises a combined text budget of 2,000 characters for reliable output. Treat that as a route-specific reliability budget, not the standalone TTS limit. It uses `future_text`, not TTS `next_text`, and its adjacent-text fields allow 100 characters. See [Create dialogue](https://elevenlabs.io/docs/api-reference/text-to-dialogue/convert).

Do not assume a dialogue response contains isolated speaker stems. If the deliverable needs separately editable lines, render them separately and direct continuity at the scene level. If natural shared timing is the priority, audition the dialogue route.

## Long-form continuity

Split at complete paragraphs, scene boundaries, or full conversational turns. Keep words, quotations, and essential context intact. Choose chunks within the route budget rather than using a universal sentence length. Cache accepted output and repair the affected chunk with its neighbors as context.

V4 TTS supports request stitching; v3 does not. A previous response must be fully consumed before its request ID conditions the next generation. Keep at most the three most recent prior IDs, nearest last; the guide requires IDs less than two hours old. Use the same model, voice, and settings. Reference: [request stitching](https://elevenlabs.io/docs/eleven-api/guides/how-to/text-to-speech/request-stitching).

Choose text conditioning when audio IDs are unavailable and the model/endpoint supports it. IDs take precedence over the corresponding text fields. Do not insert context into the spoken text to compensate for an unsupported conditioning field. Zero-retention configurations can remove history-dependent functionality; check the [retention documentation](https://elevenlabs.io/docs/eleven-api/resources/zero-retention-mode).

Decode and join compatible audio deliberately. Do not assume concatenating independent encoded file bytes produces a well-formed deliverable. Preserve word tails and natural breaths, inspect joins, and re-encode once where practical.

## Streaming

| Input | Route | Key distinction |
|---|---|---|
| Whole script already known | HTTP speech or dialogue stream | Consume the entire response and final timing |
| Incremental v4/v3 family text | `/v1/text-to-dialogue/stream-input` WebSocket | Register voices, then send `inputs` frames |
| Incremental legacy TTS | `/v1/text-to-speech/{voice_id}/stream-input` WebSocket | Different message shape and buffering controls |

For v4 Turbo, the documented dialogue WebSocket registers exactly one voice. Set `model_id=eleven_v4_turbo`. Use `flush` for a completed short buffer, `close_socket` at completion, and `keep_alive` when idle. Preserve word boundaries between fragments and leave enough linguistic context for phrasing. See the [dialogue streaming guide](https://elevenlabs.io/docs/eleven-api/guides/how-to/websockets/realtime-tdd).

For that single-voice route, authenticate with the server-side `xi-api-key` header. The minimal message sequence uses already resolved `voice_id` and prepared `text` variables:

```python
registration = {"voices": [voice_id]}
content = {"inputs": [{"text": text, "voice_id": voice_id, "new_turn": False}]}
flush_completed_turn = {"flush": True}
keep_connection_alive = {"keep_alive": True}
finish_session = {"close_socket": True}
```

Send registration first, followed by content frames. Use `new_turn` at actual turn boundaries according to the current protocol. Use a flush when needed, not on every token. Keep receiving after `close_socket`: decode each nonempty `audio` field from base64, handle `error`, and finish on the final `is_final: true` frame. Then drain queued playback. Those fields are documented in the linked guide; this sequence is not a complete client or a multi-context message schema.

Do not transfer legacy `chunk_length_schedule` into dialogue messages. The [legacy streaming guide](https://elevenlabs.io/docs/eleven-api/guides/how-to/websockets/realtime-tts) excludes standalone v3/v4 from that route. The dialogue how-to and API reference disagree about multi-voice standalone v4 WebSockets; verify that specific case before use. Ordinary REST dialogue and single-voice v4 Turbo are separate, documented cases.

In a custom player, process errors and final events, drain the final audio, and cancel stale queued playback when interrupted. Closing a context can flush audio instead of discarding it. See [multi-context behavior](https://elevenlabs.io/docs/api-reference/text-to-dialogue/ttd-multi-websocket) and the agent reference.

## Formats, captions, and completion

Select the codec, sample rate, and container for the destination. MP3 is a practical preview; raw PCM needs explicit format metadata and is not a WAV file merely because it is renamed. Telephony may require mono mu-law or A-law. Confirm current format entitlements from the endpoint rather than promising a subscription tier.

Use a timestamp-enabled endpoint when available. Keep canonical captions free of direction tags and phonetic substitutions. Inspect alignment offsets after splitting and joining. [Forced alignment](https://elevenlabs.io/docs/api-reference/forced-alignment/create) can align supplied text to an existing recording; it does not prove that the recording says the supplied words. Verify the words independently before alignment.

The [non-streaming timing endpoint](https://elevenlabs.io/docs/api-reference/text-to-speech/convert-with-timestamps) returns JSON with `audio_base64` and optional `alignment`/`normalized_alignment`. Decode its audio field; do not save the whole JSON as an MP3. Check the specific streaming endpoint's framing separately.

Save to a temporary output, confirm successful status and plausible audio, consume the full stream, then promote it to the final filename. Confirm duration and the final spoken clause. HTTP success alone does not rule out early termination.

## Failures and cost control

Separate invalid requests and permissions from transient overload. Correct 400/422 payload problems and 401/403 credentials or access without blind retries. For 429 or transient 5xx, inspect the provider error, quota, concurrency, and any retry guidance; apply bounded backoff with jitter where appropriate. An ambiguous timeout may already have generated billable audio. Check the known job/history before resubmitting.

Bound concurrency to the actual account and route. Track a fingerprint of all output-affecting inputs, including model, voice, text, settings, dictionary versions, context, format, and seed. Reuse completed outputs. A seed is best-effort repeatability, not guaranteed identical audio. These operational measures extend the [official API integration guidance](https://elevenlabs.io/blog/text-to-speech-api-integration).

Keep a generation manifest and resumable completion state. Store request IDs when supplied, selected takes, and failures without secrets. Do not overwrite good clips while retrying a failed section. A future change announced on [16 November](https://elevenlabs.io/docs/changelog/2026/11/16) introduces `/v1/convai` server-side timeouts from **26 November 2026**; handle 504 responses with operation-aware recovery, not unconditional replay of mutating work.
