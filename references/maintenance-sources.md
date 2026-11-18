# Evidence and maintenance

Research snapshot: **18 November 2026**. Keep this reference out of routine task context unless refreshing or resolving conflicting claims. The skill combines paraphrased vendor capabilities, labelled firsthand community reports, and original writing, integration, and evaluation recommendations. Example scripts are original and hypothetical.

## Refresh narrowly

1. Identify the uncertain field or feature. Do not restart a full product investigation.
2. Read the current model-specific page and the exact endpoint/tool schema. Check the dated changelog if their claims conflict.
3. Confirm the capability in the relevant account when needed. A model catalog entry is not proof of access or acceptable output.
4. Record verified date, surface, source URL, finding, and remaining uncertainty in the project. Update this reusable snapshot when behavior has materially changed.
5. Update affected examples and checker constraints together. Run the offline tests and a fresh scenario that depends on the changed behavior. Use an authorized audio sample when the claim concerns sound.

Thirty days is a maintenance heuristic, not an official expiry period. A request for the latest release or an actual incompatibility justifies an immediate targeted check. Never turn a model's marketing description into a guaranteed output quality, exact timing, or end-to-end latency promise.

## Evidence hierarchy

| Question | Primary evidence |
|---|---|
| Which model is recommended now? | Current model page plus release/changelog |
| Is a control meaningful for this model? | Model-specific capability page and exposed runtime controls |
| Which field name or limit belongs here? | That endpoint or tool schema |
| Can this account use it? | Actual account catalog or authorized request |
| Does it sound right? | The generated audio, heard in the intended context |
| Which practitioner technique is worth trying? | Firsthand report with model, inputs, outcomes, and limitations; then a project-specific audition |

If current sources still disagree, preserve the uncertainty. Choose a documented common path or perform a small scoped check. Do not make a broad assertion from one older example.

The [community register](community-practice.md#source-register) records independent blogs, Reddit, LinkedIn, and a public developer issue. Keep experience reports separate from capability documentation. Mark unknown models, affiliate or product interests, missing audio, selected-take bias, and later corrections. Do not adopt a social-media recipe from popularity or a search excerpt alone.

## Known documentation conflicts

| Conflict | Operating decision |
|---|---|
| Shared settings include fields unavailable in v4 | Use only model-supported fields; do not infer support from shared types |
| General speed help says all models | V4-specific and agent speed pages exclude v4/v3 families |
| Older guides recommend v3 as newest | Default new content to verified v4 |
| Dialogue overview suggests unlimited cast | Respect the REST endpoint's ten distinct voices and 2,000-character reliability guidance |
| Standalone v4 WebSocket voice counts differ | Verify that case; do not confuse it with REST dialogue or single-voice v4 Turbo |
| Generic accent guidance conflicts with v4 | Follow v4 cross-language behavior and audition the required accent |
| Dictionary guides differ on non-English v3 phonemes | Prefer v4 for new work; verify required v3 behavior |
| PLS examples imply universal case sensitivity | Inspect API rule flags as well as imported PLS behavior |
| Old troubleshooting suggests every clip under 800 characters | Use as a local repair tactic, not a universal request limit |
| Old agent latency field remains in configuration | Do not tune the deprecated no-op |
| Broad provider skill contains legacy quickstarts | Use it for tool workflow; refresh the affected model fact |

## Primary-source map

The references link specific claims directly. Use this index to locate only what needs refreshing.

| Topic | Official source |
|---|---|
| Current models and language lists | [Models](https://elevenlabs.io/docs/overview/models) |
| V4 features and settings | [Eleven v4](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/eleven-v4) |
| Release history | [Changelog](https://elevenlabs.io/docs/changelog) |
| Audio tag syntax | [Tag help](https://elevenlabs.io/docs/help-center/product/core-capabilities/text-to-speech/how-do-audio-tags-work-with-eleven-v3-and-v4) |
| Open-ended tag examples | [Audio tags](https://elevenlabs.io/blog/elevenlabs-audio-tags-list) |
| Punctuation, IPA, and prompting | [Best practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices) |
| Pause compatibility | [Pauses](https://elevenlabs.io/docs/help-center/product/core-capabilities/text-to-speech/how-can-i-add-pauses) |
| Voice discovery | [List voices](https://elevenlabs.io/docs/api-reference/voices/search) |
| REST speech | [Create speech](https://elevenlabs.io/docs/api-reference/text-to-speech/convert) |
| REST dialogue | [Create dialogue](https://elevenlabs.io/docs/api-reference/text-to-dialogue/convert) |
| Chunk continuity | [Request stitching](https://elevenlabs.io/docs/eleven-api/guides/how-to/text-to-speech/request-stitching) |
| Incremental v4 speech | [Dialogue WebSocket](https://elevenlabs.io/docs/eleven-api/guides/how-to/websockets/realtime-tdd) |
| Pronunciation rules | [Dictionary guide](https://elevenlabs.io/docs/eleven-api/guides/how-to/text-to-speech/pronunciation-dictionaries) |
| Agent architectures | [Realtime models](https://elevenlabs.io/docs/eleven-agents/customization/realtime-models) |
| Live expression | [Expressive mode](https://elevenlabs.io/docs/eleven-agents/customization/voice/expressive-mode) |
| Live conversation pacing | [Conversation flow](https://elevenlabs.io/docs/eleven-agents/customization/conversation-flow) |
| Agent prompts | [Prompting guide](https://elevenlabs.io/docs/eleven-agents/best-practices/prompting-guide) |
| Behavior evaluation | [Agent testing](https://elevenlabs.io/docs/eleven-agents/customization/agent-testing) |
| Latency definitions | [Measurement methodology](https://elevenlabs.io/docs/eleven-api/concepts/latency-methodology) |
| Audio repairs | [Troubleshooting](https://elevenlabs.io/docs/eleven-creative/troubleshooting) |

## Maintain the small execution path

Keep `SKILL.md` short and route-specific details in references. Avoid accumulating a full SDK manual or an untested list of magic settings. Keep the preflight helper dependency-free and offline. Its hard failures represent known incompatibilities or explicit conservative operating budgets; its warnings are prompts for review. Do not silently widen support to a newly named model.

After an update, verify frontmatter, links, example payloads, script behavior, and a fresh agent's ability to complete representative tasks from the skill alone. Preserve the distinction between those checks and audible validation. Commit the completed change with a normal descriptive message and let configured CI run.
