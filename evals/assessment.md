# Skill assessment

Date: **18 November 2026**.

## Scope and result

The installable skill was assessed through source review, local structural checks, 41 deterministic Python tests, and twelve production-style tasks given to three independent agents with fresh context. One streaming task initially exposed an incomplete reference. The reference was expanded and a fourth fresh agent completed a targeted streaming task from the updated skill.

All twelve task areas met the critical criteria after that revision. This is a qualitative assessment of skill-following behavior, not a statistical benchmark or a guarantee of future results. The agents were given the skill path and practical user requests, without expected answers or the research conversation. The reusable task set is in [scenarios.json](scenarios.json).

No paid audio was generated. No live agents, calls, or customer tools were changed. No listening, accent, pronunciation, naturalness, or live latency result is claimed. Those require audio and interactive testing with the selected voice and workspace.

## Independent task outcomes

| ID | Task | Observed behavior | Outcome |
|---|---|---|---|
| C1 | Exact price, leading-zero code, ambiguous date, precise pause, v4 speed request | Preserved the supplied text, flagged the date, omitted unsupported speed, planned a measured edit after tempo processing | Pass for text and planning |
| C2 | Natural fictional news delivery | Preserved the delay, attribution, accessibility reason, and refund right without inventing drama or forced filler | Pass for writing |
| C3 | English, Afrikaans, isiZulu, isiXhosa, name, and accent | Distinguished verified languages from unverified isiXhosa, requested a pronunciation source, retained canonical captions, avoided promising identical cross-language accent | Pass for capability reasoning |
| C4 | Certify human sound from text alone | Produced directed and plain audition candidates and explicitly declined an unsupported audio-quality claim | Pass for evidence discipline |
| P1 | 18,400-character audiobook with an accepted paragraph | Planned complete-thought chunks, retained accepted audio, tracked output inputs, used supported continuity, and reconciled ambiguous retries | Pass for production planning |
| P2 | 6,600-character dialogue with twelve actors and separate files | Distinguished TTS/dialogue budgets and ten-voice cap; chose line renders and aligned actor tracks for editable output | Pass for route selection |
| P3 | Legacy streaming migration to v4 Turbo | Correctly selected dialogue WebSocket and removed incompatible controls, but initially could not construct all wire messages from the reference | Partial initially; resolved in R1 |
| P4 | Raw PCM renamed WAV, seeded determinism claim, timeout retry | Required a real container, rejected deterministic-audio assurance, and treated a started paid request as ambiguous | Pass for failure handling |
| A1 | Managed Realtime agent with a stored Flash ID and external LLM requirement | Explained ignored managed settings and planned a preserved-agent migration to Custom mode without guessed fields | Pass for architecture reasoning |
| A2 | Agent cuts off spelled email and repeats silence prompts | Separated prompt, first message, turn controls, skip-turn behavior, and machine-readable tool values | Pass for interaction planning |
| A3 | Stale speech and captions after interruption, 100 ms promise | Cancelled local playback, discarded stale frames, corrected delivered text, and distinguished end-to-end measurement from TTS medians | Pass for engineering reasoning |
| A4 | Exact acting from seven-minute source and Spanish version | Selected Voice Changer with sub-five-minute segments, kept the source, routed translation to Dubbing, and required listening/language review | Pass for operation selection |
| R1 | Concrete single-voice Turbo message exchange after revision | Produced header/query, registration, inputs, flush/keep-alive/close messages, audio decoding and final event handling; separated interruption from normal drain | Pass for targeted transfer |

## Corrections made during assessment

1. Added minimal single-voice v4 Turbo WebSocket objects and response fields to the API reference. A fresh agent used them without live research.
2. Corrected the timestamped-speech documentation link by following the official endpoint index.
3. Fixed nested, reversed, empty, and multiline bracket validation. Equal bracket counts had previously allowed malformed direction markup.
4. Rejected settings placed at the top level of the planning envelope and warned about fields outside its schema.
5. Added the reference's selected-voice placeholder to preflight rejection cases.
6. Checked actual dialogue `future_text` as well as the planning alias, with a conflict error when both are supplied.
7. Added a surface-verification warning for legacy Speaker Boost rather than asserting universal compatibility.
8. Fixed the structure checker to accept valid unquoted and wrapped interface strings produced by installation, while retaining required-field, skill-reference, and description-length checks.

The speech preflight regression suite increased from 30 to 34 test methods. Seven metadata regression cases brought the complete suite to 41 test methods. Multiple methods contain boundary and malformed-input subcases.

## Reproducible offline checks

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts -p 'test_speech_preflight.py' -v
python3 scripts/check_skill.py .
```

The first command passed all 41 tests. The second passed frontmatter, required files, local Markdown paths/heading links, metadata, entrypoint size, and punctuation checks against both the repository and installed skill. The skill-creator validator also passed against the installed skill directory. In the initial assessed snapshot, `SKILL.md` contained 93 lines and 1,230 whitespace-separated words and routed agents to nine optional references. The community extension below records the updated size.

The workflow in [.github/workflows/validate.yml](../.github/workflows/validate.yml) runs the two repository-local commands on pushes and pull requests. It does not run paid synthesis or replace listening QA. Normal commit messages preserve configured CI execution.

## Publication verification

The skill and supporting files were published to the repository's `main` branch and the installed skill was verified after installation. GitHub created the validation workflow, but the [first run](https://github.com/MikeyNu/agent-elevenlabs/actions/runs/44320906565) did not execute any steps. Its annotation states that the job could not start because the account is locked due to a billing issue. This is an account-level CI blocker, not a failed local validation result. The workflow remains enabled. A successful hosted CI run is not claimed.

## Research evidence and limits

The skill cites 46 distinct official ElevenLabs URLs and records model-specific discrepancies rather than hiding them. The available ElevenLabs connector's v4 model schema was also inspected: it exposes Stability and Similarity and defaults its TTS catalog to v4. Public-document support and workspace runtime controls were treated as different evidence surfaces.

The references record the verified date and a narrow refresh policy. A direct automated HEAD probe of external URLs returned 403 responses, so it was inconclusive as a link-health test; source research used web retrieval and the official connector. No claim is made that all external URLs were independently HTTP-health-checked. Internal paths and headings were checked locally.

No exact token-savings percentage is asserted. The intended saving comes from the small entrypoint, on-demand references, retained decisions, and reusable offline checks. Future model changes still require focused verification when relevant.

## Community research extension

Completed on 18 November 2026 after the user asked about methods reported by other creators. The initial research prioritized vendor documentation and ElevenLabs' own blog. This extension reviewed firsthand practitioner material and added [community-practice.md](../references/community-practice.md) with fourteen curated sources: seven creator/developer articles, four Reddit discussions, two LinkedIn showcases, and one public SDK issue with a confirmed resolution.

The register records model, date where recoverable, claimed result, accessible evidence, commercial interests, and transfer limits. Relative social timestamps remain approximate. Linked audio/video was not auditioned. A source's claimed success is not presented as an independently reproduced result. Suggestions, demonstrations, comparisons, and confirmed fixes remain distinct. Unavailable-page snippets and generic promotional reposts did not establish techniques.

The extension adds a controlled audition method for conflicting recipes, conditional handling for a historical trailing-context workaround, and guidance for preserving literal bracketed content when a configured speech fallback cannot perform audio tags. It strengthens checks for client playback and time to useful spoken content. It does not adopt universal slider values, tag counts, whisper quotas, speed percentages, or a claim that community reports prove one best narration method.

Two new agents with fresh context received practical tasks and the installed skill path, without expected answers, web research, or the prior research conversation. The skill folder did not contain the assessment criteria. Neither agent generated audio or changed a live system.

| ID | Task | Observed behavior | Outcome |
|---|---|---|---|
| B1 | Exact-wording restrained v4 narration with a 35%/75%, every-sentence-tag, 20%-acceleration recipe and a conflicting repetition report | Preserved all words; produced plain and directed candidates; held voice/settings constant; treated the recipe and repetition claim as hypotheses; separated export acceleration from generation controls; left sound judgments unassessed | Pass for evidence use and audition planning |
| B2 | v4 Turbo to approved Flash fallback with split performance markup and a literal bracketed locker identifier | Removed the known cue across chunks, preserved the identifier/caption, separated text received from audio played, used a playback checkpoint for the remaining suffix, handled incomplete cues and literal fragments, and disclosed midword-resumption uncertainty | Pass for integration reasoning; runtime not exercised |

The reusable prompts and criteria are appended to [scenarios.json](scenarios.json). All 41 existing regression tests still pass. Structure/link checks and the skill-creator validator pass against the updated installed skill. No executable synthesis or parsing code was added in this extension. The entrypoint is now **96 lines and 1,284 words**, with **ten optional references**. Repository and installed content are checked for agreement when saving. Hosted CI remains a separate verification step from these local results.
