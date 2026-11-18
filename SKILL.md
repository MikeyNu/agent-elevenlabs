---
name: elevenlabs-speech
description: Create, direct, integrate, and troubleshoot natural ElevenLabs voice audio. Use for text-to-speech, voiceovers, narration, commentary, podcasts, dialogue, character speech, expressive audio tags, pronunciation, multilingual delivery, voice cloning or conversion, dubbing, streaming speech, and the speaking behavior of conversational voice agents. Apply when audio sounds robotic, overacted, badly paced, mispronounced, truncated, or unresponsive. Includes current model routing, focused references, and an offline preflight checker so routine tasks do not require repeated broad research.
---

# ElevenLabs Speech

## Start here

Direct a performance that serves the listener. Preserve the user's meaning, choose the right voice and route, then validate the actual audio. Use this file plus only the reference needed for the task.

**Verified snapshot: 18 November 2026.** Default new content to `eleven_v4`. Use `eleven_v4_turbo` for explicitly selected expressive real-time TTS. Read an existing agent's voice mode before changing it: managed Realtime agents control their own speech stack. See [model capabilities](references/model-capabilities.md) for evidence and exceptions.

Do not repeat broad ElevenLabs research for each task. Use the bundled sources and a focused capability check when the user asks for the latest model, the snapshot is over 30 days old, a parameter fails, a new language or route is involved, or documentation conflicts affect the task. Check the relevant model, endpoint, and changelog once; record the finding with the project. See [maintenance and sources](references/maintenance-sources.md). Never substitute a model silently to get a request through.

## Route the task

| Need | Read next | Result to produce |
|---|---|---|
| Natural narration, commentary, ads, character lines | [Performance direction](references/performance-direction.md) | Clean script and restrained, model-compatible direction |
| Names, prices, abbreviations, accent, languages | [Pronunciation and localization](references/pronunciation-localization.md) | Verified pronunciation plan, original text retained |
| API, SDK, dialogue, long-form, streaming, captions | [API workflows](references/api-workflows.md) | Correct endpoint and payload, complete audio and timing |
| Interactive assistant or telephone agent | [Realtime agents](references/realtime-agents.md) | Speech behavior plus turn and interruption configuration |
| Robotic, distorted, misread, inconsistent, or cut-off audio | [Troubleshooting and QA](references/troubleshooting-qa.md) | Diagnosed cause, smallest effective repair, listening evidence |
| Existing acted audio or translated performance | [Performance alternatives](references/performance-alternatives.md) | Voice Changer, Dubbing, or isolation workflow |
| A concrete genre example | [Scenario recipes](references/scenarios.md) | Adapted pattern with facts and tone preserved |

Music-only, sound-effects-only, and transcription-only requests belong to those capabilities. Use them here when supporting a voice deliverable; do not treat their model IDs or controls as TTS settings.

## Execute the workflow

### 1. Establish the speech brief

Infer from the task: audience, purpose, language and accent, voice identity, emotional intention, medium, target duration, and whether rewriting is allowed. Reuse known project choices. Ask only for information that blocks correctness, such as an ambiguous date, required name pronunciation, missing source audio, or an unknown offer. Do not ask for a voice ID when a connected voice search can resolve one.

Keep three separate representations when needed:

- **Canonical text:** the approved wording, names, quotations, numbers, and captions.
- **Synthesis text:** spoken wording plus supported cues and verified pronunciation substitutions.
- **Direction/configuration:** scene notes, tone rationale, voice/model/settings, and edit timings. Keep these out of the spoken payload.

For exact-wording tasks, preserve every spoken word and the intended meaning. Add only requested performance markup. Do not invent facts, claims, quotes, offers, fillers, or personal reactions to make a script sound natural.

### 2. Select a suitable voice and model

Search available voices by language, accent, use case, and the requested vocal character. Preserve an established voice unless a change is needed or requested. Verify model availability and clone readiness in the actual workspace. Obtain permission for a cloned voice where required by the service and use case.

Keep saved/default voice settings for the first take. Adjust settings to solve an observed problem, one dimension at a time. A generic API schema is not proof that every model supports every field. V4 uses Stability and Similarity; omit legacy Speed, Style, and unexposed Speaker Boost controls. Connector `similarity` and REST `similarity_boost` are different field names. Read the actual surface's schema.

### 3. Write for the ear, then annotate

Use complete thought units, clear references, conversational wording where appropriate, and varied sentence length. Put the important information where the listener can follow it. Make emphasis selective. Use natural punctuation first; add cues only where they improve an intentional change in delivery.

For v4/v3, use square-bracket audio tags such as `[curious]`, `[softly]`, or `[short pause]`. Parentheses are ordinary text, not reliable direction syntax. Tags are contextual instructions, not guaranteed commands. Do not force a fixed tag count or add a tag to every sentence.

Example, for a fictional scheduling update:

```text
The demo has moved to Friday. We need two more days for testing.
[curious] Can you make the new time?
```

Keep direction tags out of legacy tag-free models. Do not use SSML break tags with v4 or v3. Do not promise exact milliseconds from `[pause]`; measure and edit the timeline for exact silence. Keep sound effects and background music on controllable tracks when their presence or timing is required.

### 4. Preflight before synthesis

For programmatic work, create a small planning-job JSON and run:

```bash
python scripts/speech_preflight.py /absolute/path/to/speech-job.json
```

Resolve script paths relative to this skill's directory. See [API workflows](references/api-workflows.md#offline-preflight) for the job format. The checker does not generate audio, rewrite text, verify credentials, validate the entire API schema, or prove naturalness. Treat warnings as review prompts, not automatic reasons to change wording. It deliberately supports a small, verified set of routes.

Check character and speaker budgets, factual fidelity, pronunciation, supported cues/settings, target output format, and chunk boundaries. Measure duration after generation; a word-count estimate is only a planning aid.

### 5. Audition, then scale

For a new voice or difficult delivery, generate a representative short excerpt within the task's budget. Include the hardest name, emotional transition, or language switch. Compare a plain baseline with one directed candidate when useful. For a very short deliverable, audition the deliverable itself.

Listen before rendering a long piece. Change the smallest relevant variable, then compare. If two targeted revisions do not help, reassess voice suitability, source recording, model, or route instead of stacking more cues. Reuse accepted clips and repair only failing sections. Do not automatically resubmit an ambiguous timed-out paid request.

### 6. Verify the result

Follow the [QA rubric](references/troubleshooting-qa.md). Listen for complete words, correct names and values, intentional emphasis, comfortable pacing, consistent identity, sensible emotions, and clean joins. Check the opening and ending. For agents, also exercise user pauses, interruptions, delayed tools, and language switching.

Use transcription and timing tools as supporting evidence. A matching transcript cannot prove naturalness. If no audio was generated or listening is unavailable, report **text/configuration assessed; audio not auditioned**. Never report audio quality as verified from a script, a linter, or a successful HTTP response.

### 7. Deliver a reusable result

Provide the final audio when generated, the clean script, the model and voice used, material settings/dictionary versions, duration, and a concise account of validation and remaining limitations. Include the directed synthesis text when it helps reproduction. Preserve canonical subtitles separately from pronunciation workarounds and audio tags.

Save a small project-local generation record with clip IDs, output-affecting settings, request IDs when available, and selected take. Keep API keys and sensitive scripts out of shared skill files. Complete already-authorized generation or integration work; do not stop at offering to do it.
