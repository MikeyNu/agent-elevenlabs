# Troubleshooting and listening QA

Use symptoms and evidence to choose the smallest repair. The thresholds and workflow below are project recommendations. They are not vendor guarantees, clinical assessments, or automatic measures of human likeness.

## Contents

- [Diagnose the audible problem](#diagnose-the-audible-problem)
- [Evaluate each take](#evaluate-each-take)
- [Separate evidence levels](#separate-evidence-levels)
- [Repair and stop](#repair-and-stop)

## Diagnose the audible problem

| Symptom | Check first | Targeted repair |
|---|---|---|
| Flat or robotic | Voice fit, written prose, uniformly high stability | Test a more suitable voice or a single phrasing change; then adjust supported stability |
| Overacted or breathless | Dense tags, repeated ellipses, forced fillers | Return to plain text and add only the needed cue |
| Directions spoken aloud | Correct model, bracket syntax, metadata in text | Remove notes from payload; use compatible square-bracket cues |
| Sudden sound effect | Ambiguous cue or non-verbal tag | State a clear delivery quality or move the effect to its own track |
| Incorrect word stress or name | Verified pronunciation, dictionary application/version | Repair the one pronunciation and audition in context |
| Numbers wrong | Source meaning, locale, normalization | Preserve value; explicitly render only the known intended reading |
| Voice drifts across sections | Model, voice, settings, source quality, context | Match configuration; condition where supported; repair the local join |
| Unexpected noise or plosives | Reference recording and whether flaw repeats | Compare a clean voice sample before further prompting |
| Longer take deteriorates | Length and exact point of deterioration | Split the failing portion at full thoughts, then compare |
| Abrupt start or cut-off ending | Script boundaries, response completion, route budget | Consume full output, reduce overloaded request, preserve all final words |
| Good transcript, unnatural delivery | Listening evidence | Listen and redraft/revoice; transcription cannot assess every performance issue |
| Agent interrupts or talks over a correction | Turn policy and stale playback | Fix interaction controls and queue cancellation, then retest live |

The vendor's [troubleshooting guide](https://elevenlabs.io/docs/eleven-creative/troubleshooting) discusses mispronunciation, unstable style settings, and degraded long generations. Its sub-800-character suggestion is a recovery tactic, not a universal v4 limit. The [emotion guidance](https://elevenlabs.io/docs/help-center/product/core-capabilities/text-to-speech/how-to-produce-emotions) supports experimenting with context and delivery rather than assuming one setting guarantees emotion.

If the same defect appears in every take at the same place, inspect the input and source voice. If it moves between takes, compare the sampling and cue complexity. This is a diagnostic heuristic, not proof of cause. Inspect the actual audio before attributing the failure.

## Evaluate each take

Keep a small scorecard. For each dimension, use 1 = unusable, 3 = usable with a noticeable issue, and 5 = ready for the intended audience. Scores are human judgments. Do not synthesize scores from the input script.

| Dimension | Listen or check for |
|---|---|
| Fidelity | All intended words, quotations, names, numbers, units, and meaning |
| Pronunciation | Names, acronyms, regional terms, stress, language transitions |
| Prosody | Useful emphasis, complete phrases, varied but coherent cadence |
| Emotional fit | Appropriate energy and reactions for the content |
| Identity | Stable voice, requested accent, consistency with approved clips |
| Technical quality | Clipping, noise, clicks, breaths cut in half, level jumps |
| Timing | Actual duration, intentional pauses, joins, complete ending |
| Interaction, if live | User space, interruption cleanup, tool delay, language switching |

Treat wrong critical facts, missing words, a truncated ending, incorrect identity, or inaudible speech as blockers regardless of the average score. Choose a project acceptance threshold before comparing takes; for ordinary published narration, aiming for at least 4 on applicable dimensions is a useful starting criterion. Leave unassessed dimensions blank.

Listen to the entire final short clip. For long material, inspect every repaired boundary and all high-risk words, then complete the required full-content review before claiming the entire work was auditioned. State when only samples were heard. Compare candidates at similar levels so loudness does not dominate the judgment.

## Separate evidence levels

| Evidence | Supports | Does not establish |
|---|---|---|
| Offline preflight | Known input and compatibility checks | Account access or audible quality |
| Successful request | Server accepted and returned data | Complete or natural speech |
| Duration/codec inspection | Technical metadata and gross truncation clues | Correct pronunciation |
| ASR comparison | Possible omissions, repetitions, substitutions | Perfect transcript or emotional fit |
| Forced alignment | Timing against a supplied transcript | That every supplied word was spoken |
| Listening | Performance judgment for the audio actually heard | Unheard sections or every future generation |
| Agent transcript simulation | Dialogue logic and tool choices exercised | Real microphone timing and playback behavior |

The [timestamped speech endpoint](https://elevenlabs.io/docs/api-reference/text-to-speech/convert-with-timestamps) and [alignment endpoint](https://elevenlabs.io/docs/api-reference/forced-alignment/create) supply different evidence. Use the audio itself to settle important discrepancies. Retain the canonical script so a successful transcript comparison cannot accidentally compare against an already corrupted rewrite.

If generation or listening is unavailable, deliver a usable script/configuration and say exactly what was assessed. Do not label a sample “human-like,” “production-ready,” or “fully tested” merely because a text check passed.

## Repair and stop

1. Mark the exact timestamp, word, or turn that fails.
2. Form one testable hypothesis and change the smallest related input.
3. Regenerate or re-edit that section, keeping accepted neighbors.
4. Compare against the previous take and source text.
5. Check the repaired boundaries and final export.

Keep a baseline and a small candidate set. After repeated failures, change the voice/route or request a missing pronunciation/performance reference. Do not keep lowering stability, adding cues, or spending credits without a hypothesis. Once the result meets the brief and checks, stop optional experimentation.

Suggested delivery note:

```text
Model/voice: recorded in the generation manifest.
Changed: one pronunciation and the pause before the final question.
Verified: full clip heard, source values checked, ending intact.
Remaining: exact regional pronunciation of one name awaits its supplied reference.
```

Use only statements supported by work actually performed. Omit irrelevant lines rather than inventing evidence.
