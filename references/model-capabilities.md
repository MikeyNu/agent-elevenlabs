# Model capabilities and selection

Verified against official sources on **2026-11-18**. Treat this as a capability snapshot, not an indefinite promise. Use the cached routing for ordinary work; recheck the specific model or endpoint when availability changes, an unsupported parameter appears, or the user explicitly requests the latest release.

## Select the model and surface

| Need | Starting choice | Decision rule |
|---|---|---|
| Commentary, narration, adverts, character speech | `eleven_v4` | Current flagship; set the ID explicitly |
| Expressive speech for live conversations | `eleven_v4_turbo` | Use the supported real-time surface |
| Reproduce an approved v3 performance | `eleven_v3` | Retain only for a concrete compatibility or creative reason |
| Established inexpensive streaming integration | `eleven_flash_v2_5` | Re-evaluate quality against the task |
| Existing stable legacy narration pipeline | `eleven_multilingual_v2` | Keep when measured results justify it |
| Preserve a human-recorded performance in another voice | `eleven_multilingual_sts_v2` | Use Voice Changer instead of reconstructing the acting from text |

The [model catalog](https://elevenlabs.io/docs/overview/models) documents these IDs. V4 and v4 Turbo became available on [28 September 2026](https://elevenlabs.io/docs/changelog/2026/9/28). V3 is not the latest model. Confirm the selected voice is accessible through the actual account and surface; never invent a voice ID.

## Apply only supported controls

| Control | V4 family guidance |
|---|---|
| Stability | Adjust consistency versus performance variation |
| Similarity | Adjust adherence to the reference voice; maximum is not automatically best |
| Clone Strength | Apply only to a Professional Voice Clone trained for the selected v4 model; start at zero unless an existing approved preset says otherwise |
| Style exaggeration | Do not apply a legacy Style setting to v4 |
| Speed slider | Do not apply a legacy Speed setting to v4 |
| SSML | Do not use SSML as a v4 performance-control language |

[Professional Voice Cloning](https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/professional-voice-cloning) confirms the supported core settings and excludes Style, Speed, and SSML. The [conversational voice guide](https://elevenlabs.io/docs/eleven-agents/customization/voice/best-practices/conversational-voice-design) explains Clone Strength and recommends zero initially for most voices. The [9 November changelog](https://elevenlabs.io/docs/changelog/2026/11/9) confirms continuous 0 to 100% Stability in the v4 Text to Speech flow node. Do not transfer v3-specific discrete presets to v4.

Use saved settings as the baseline. If none exist, a moderate starting point is a trial, not an optimum. Change one setting at a time and compare the same excerpt. Keep any user-approved voice and model pairing until evidence supports changing it.

**Connector observation, 2026-11-18:** the inspected v4 connector schema did not expose speaker boost. Do not inject `speaker_boost` or `use_speaker_boost` into that connector. Inspect its current schema before passing parameters. This observation does not establish that every REST surface rejects those fields.

## Keep syntax and request limits separate

Use square-bracket directions on compatible models, not parenthetical stage directions. [Audio tag help](https://elevenlabs.io/docs/help-center/product/core-capabilities/text-to-speech/how-do-audio-tags-work-with-eleven-v3-and-v4) identifies the compatible families. Tags guide performance; they are not guaranteed timing or emotion commands. [Pause guidance](https://elevenlabs.io/docs/help-center/product/core-capabilities/text-to-speech/how-can-i-add-pauses) distinguishes v4/v3 audio cues from legacy SSML breaks.

The [model catalog](https://elevenlabs.io/docs/overview/models) lists TTS limits of 10,000 characters for v4 and 5,000 for v3. These are not dialogue request budgets.

For [Create dialogue](https://elevenlabs.io/docs/api-reference/text-to-dialogue/convert):

- Assign each turn its own `text` and `voice_id`.
- Use at most ten distinct voice IDs.
- Keep aggregate turn text at or below 2,000 characters for reliable generation.
- Set `model_id` explicitly because the documented default remains v3.
- Treat `seed` as best-effort repeatability, never identical-audio assurance.
- Apply this endpoint's own settings shape; do not copy TTS `voice_settings` blindly.

For content beyond a practical request size, split at complete thoughts. Preserve an approved performance across sections and inspect boundaries after joining.

## Maintain continuity

The [request-stitching guide](https://elevenlabs.io/docs/eleven-api/guides/how-to/text-to-speech/request-stitching) supports v4 and excludes v3. For that workflow, finish reading the earlier response before using its request ID. Send at most three recent IDs, ordered with the closest previous audio last; IDs should be less than two hours old. Check retention compatibility before relying on request history. Treat stitching as contextual conditioning, not automatic artifact-free editing.

## Resolve conflicting documentation

Apply current model-specific guidance to capabilities, current endpoint schemas to payloads and limits, and dated changelogs to recent changes. Treat generic or legacy pages as secondary. Verify account-specific availability through the exposed tool or API.

| Conflict encountered | Resolution |
|---|---|
| Generic API schema exposes Speed and Style | V4 capability guidance excludes them |
| Dialogue overview says unlimited speakers | Endpoint restricts distinct voices to ten |
| Generic troubleshooting suggests sub-800-character chunks | Use as a targeted recovery tactic, not the model limit |
| Marketing implies perfect repeatability | API seed documentation explicitly does not guarantee determinism |

If the evidence remains inconsistent, state the narrow uncertainty and test that capability on a small authorized sample. Do not silently change models or claim support from a shared schema alone.
