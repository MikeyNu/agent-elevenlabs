# Natural speech for live ElevenAgents

Verified: 2026-11-18. Treat the examples below as starting points to audition, not universal presets.

## Contents

- [Select the agent architecture](#select-the-agent-architecture)
- [Preserve the existing configuration](#preserve-the-existing-configuration)
- [Separate instructions from speech](#separate-instructions-from-speech)
- [Control expression and turn timing](#control-expression-and-turn-timing)
- [Handle languages and pronunciation](#handle-languages-and-pronunciation)
- [Handle cues across output surfaces](#handle-cues-across-output-surfaces)
- [Verify audible behavior](#verify-audible-behavior)
- [Resolve documentation drift](#resolve-documentation-drift)

## Select the agent architecture

Read [model-capabilities.md](model-capabilities.md) before choosing a model.

| Requirement | Route |
| --- | --- |
| Preserve a chosen LLM and use expressive speech | Custom voice mode with `tts.model_id: eleven_v4_turbo` |
| Use an integrated voice agent with vendor-managed components | Realtime mode with `eleven_realtime_v1_mini` |
| Handle complex instructions or multi-step tools that Mini fails | Evaluate `eleven_realtime_v1_max` |
| Add speech streaming to an existing application | Follow [api-workflows.md](api-workflows.md) |

In Realtime mode, ElevenLabs manages the LLM, ASR provider, TTS model, and expressive mode. Stored `tts.model_id` and `tts.expressive_mode` values are ignored. Voice, system prompt, first message, languages, tools, and turn settings still apply. Realtime models are rolling out by workspace. Custom LLMs and transfers between Custom and Realtime agents have restrictions. Keep Custom mode when the task requires explicit control of managed components. Do not switch modes merely to obtain a newer-sounding voice. [Source: Realtime models](https://elevenlabs.io/docs/eleven-agents/customization/realtime-models)

## Preserve the existing configuration

Read the current agent, branch/version, voice, model, prompt, first message, languages, tools, and relevant turn settings before editing. Compare the requested change with that snapshot. Use the available tool's current schema, preserve unrelated settings, and inspect its returned configuration. Do not recreate an existing agent or replace its whole tool list to adjust its tone.

Keep a reviewable change and rollback reference. Apply authorized changes through the available draft/version workflow, then verify the exact saved version. Never invent a tool name, voice ID, model ID, or configuration field from a prompt example.

## Separate instructions from speech

The system prompt governs behavior and response style; platform settings govern turn mechanics and available languages. Keep those responsibilities separate. [Source: Agent prompting guide](https://elevenlabs.io/docs/eleven-agents/best-practices/prompting-guide)

Use this original prompt pattern as a starting point, adapting its role and actual tool contract:

```text
# Role
Help callers arrange appointments using the configured booking tools.

# Speaking style
Speak plainly, with contractions and varied sentence lengths.
Answer the immediate question first. Usually use one or two short sentences.
Ask one useful question at a time, then leave room for the caller.
When a caller is frustrated, use a calm, measured delivery.
For good news, sound warm without becoming theatrical.
Use supported audio tags sparingly when a specific phrase needs direction.
Do not read headings, tool arguments, or stage directions aloud.

# Accuracy
Use tool results for availability and completed bookings.
Do not describe a booking as confirmed before the tool reports success.
Keep identifiers in the exact format required by each tool.
```

Store the first message separately, as speech:

```text
Hi, I'm the booking assistant. What would you like to arrange?
```

Use dynamic variables for known greeting details and overrides when replacing an entire message. Validate required values before starting the conversation. Keep credentials out of spoken variables. [Source: Personalization](https://elevenlabs.io/docs/eleven-agents/customization/personalization)

Choose normalization deliberately. `text_normalisation_type: system_prompt` asks the LLM to verbalize numbers and symbols. `elevenlabs` uses a separate TTS normalizer, retaining formatted transcripts with some added latency. Neither removes the need to test critical names, prices, codes, and dates. Keep a spoken email separate from its machine-readable tool value. [Source: Normalization](https://elevenlabs.io/docs/eleven-agents/best-practices/prompting-guide#text-normalization)

## Control expression and turn timing

In Custom mode, selecting `eleven_v4_turbo` enables expressive mode automatically. Contextual tone instructions can work without explicit tags. Documented examples include `[slow]`, `[whispers]`, `[excited]`, `[laughs]`, and `[sighs]`. The guide describes approximately four to five words of influence per tag, varying by voice and language. Do not generalize this scope to standalone TTS, or assume a tag controls a whole paragraph. Audition the actual voice. [Source: Expressive mode](https://elevenlabs.io/docs/eleven-agents/customization/voice/expressive-mode)

Treat these as separate controls:

| Symptom | First adjustment to investigate |
| --- | --- |
| Interrupts a caller who is thinking or spelling | Turn eagerness and supported spelling-patience settings |
| Speaks over a real correction | Interruption events and client playback cleanup |
| Repeatedly prompts during user silence | Turn timeout and pause behavior |
| Long silence while preparing an answer | Measure latency, then consider a soft-timeout message |
| Sounds flat despite good timing | Voice fit, phrase structure, and restrained expression |

`turn_eagerness` supports `patient`, `normal`, and `eager`. `turn_timeout` is a separate silence setting, documented from 1 to 30 seconds. Soft timeout supplies feedback while a response is delayed; it is not an instruction to add filler to every answer. Begin conservatively and use the current schema for available options. [Source: Conversation flow](https://elevenlabs.io/docs/eleven-agents/customization/conversation-flow)

Enable and use the real `skip_turn` system tool when callers request time to think. It yields silence; punctuation or an audio tag cannot replace this behavior. [Source: Skip turn](https://elevenlabs.io/docs/eleven-agents/customization/tools/system-tools/skip-turn)

For tools, `interruption_mode` distinguishes `allow`, `disable_during_tool`, and `disable_during_tool_and_turn`. Preserve interruptibility unless the specific action or read-back requires otherwise. [Source: Tool interruptions](https://elevenlabs.io/docs/eleven-agents/customization/tools/tool-configuration/tool-interruptions)

In custom clients, stop queued playback for interrupted responses and handle `agent_response_correction` so the transcript reflects what was delivered. Verify format/sample-rate compatibility. Prefer the official SDK's event handling unless the application needs its own implementation. [Source: Client events](https://elevenlabs.io/docs/eleven-agents/customization/events/client-events)

## Handle languages and pronunciation

Configure supported languages and appropriate voices explicitly. Enable `language_detection` when automatic switching is needed; the tool is not enabled automatically. It can react to another language or an explicit request. Its `only_at_conversation_start` setting has special first-two-turn behavior, so inspect that setting before diagnosing a failed later switch. [Source: Language detection](https://elevenlabs.io/docs/eleven-agents/customization/tools/system-tools/language-detection)

The dedicated dictionary guide currently documents phoneme support for v4, v4 Turbo, v3, and Flash v2. Other models need aliases. Pin dictionary versions, handle case-sensitive entries, and audition with the chosen voice and language. Model language coverage and a particular agent's configured languages are separate constraints. [Source: Pronunciation dictionaries](https://elevenlabs.io/docs/eleven-agents/customization/voice/pronunciation-dictionary)

## Handle cues across output surfaces

For a configured, approved fallback, adapt the text to that engine's cue support before synthesis. Keep performance cues separate from visible captions and ordinary spoken text. Buffer incomplete cues across stream chunks; a prompt change alone cannot clean already queued text. [Practitioner evidence and limits: C9](community-practice.md#source-register)

Preserve literal brackets in identifiers, quotations, and other approved content. Prefer structured speech/cue segments when the pipeline permits them. If parsing tagged text, recognize only the agreed cue syntax and distinguish it from literal content; never strip every bracketed span. Define a bounded failure path for malformed or unfinished markup, so it cannot hang the stream, swallow words, or leak as unintended speech. Track delivered text before resuming after failure and avoid duplicate playback.

## Verify audible behavior

Use [troubleshooting-qa.md](troubleshooting-qa.md) for scoring. Check actual audio for a greeting, frustrated caller, slowly spelled identifier, interruption, thinking pause, delayed tool, and language switch. Test that a quiet acknowledgment does not incorrectly cancel useful speech. Compare source facts, transcript, and audio after interrupted turns.

Use Next Reply, Tool Call, and Simulation tests for behavior. Mock external tools and select error fallback where unintended real calls must be prevented. Inspect all tools because system/workflow tools are not mocked. Repeat unstable scenarios; a transcript pass does not prove natural prosody. [Source: Agent Testing](https://elevenlabs.io/docs/eleven-agents/customization/agent-testing)

Measure end-of-user-speech to audible playback in the actual application. Published TTS latency medians exclude network and application overhead. [Source: Latency methodology](https://elevenlabs.io/docs/eleven-api/concepts/latency-methodology)

Record time to the first useful content separately if filler or acknowledgment audio starts sooner. Also test first-message playback on representative devices: a transcript and speaking event can exist while a client fails to play audio. [Community examples C9-C12](community-practice.md#source-register) provide diagnostic cases, not current-model performance guarantees.

## Resolve documentation drift

Prefer specific current feature pages and actual schemas over older overview summaries. Known conflicts include old v3 expressive-mode descriptions, Flash-only phoneme claims, and fixed-language statements. Do not tune agent latency with `optimize_streaming_latency`; it is a deprecated no-op. Refresh only the affected capability and record what was verified. [Source: July 2026 changelog](https://elevenlabs.io/docs/changelog/2026/7/13)
