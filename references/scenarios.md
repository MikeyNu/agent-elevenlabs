# Scenario recipes

These are original illustrative briefs and recommended workflows, not recordings or measured performance results. Adapt the pattern to the user's content. Use [performance direction](performance-direction.md), [model capabilities](model-capabilities.md), and [QA](troubleshooting-qa.md) for the underlying rules.

## 1. Everyday commentary without forced personality

**Brief:** Explain a fictional creator's delayed video naturally. Approved facts: the upload moved from Wednesday to Saturday because the edit is unfinished.

```text
The video was meant to go up on Wednesday. It's now coming on Saturday because the edit isn't finished.
That's three more days. [curious] Would you rather wait, or see a shorter version now?
```

Use a conversational voice and test the plain question before adding `[curious]`. The reaction follows the stated facts. Do not invent a dispute, audience backlash, or a motive. If the user dislikes questions as closings, end on the information instead. Avoid canned slang, repeated “ums,” and a moral lesson.

**Acceptance:** Clear orientation, accurate timing and cause, ordinary phrasing, no forced amusement, no unsupported claim. A text-only review cannot confirm the voice sounds natural.

## 2. Advert with exact terms

**Brief:** A supplied line must remain verbatim: “The starter plan is R249 per month. Cancel any time.”

Keep those words and figures. Choose a clear voice and test the price. Add a restrained cue only if it improves delivery. Do not invent a discount, eligibility rule, annual price, guarantee, or urgency. If an explicit spoken price rendering is needed, preserve the canonical copy and verify the amount.

**Acceptance:** Correct price and billing period, no changed offer, understandable call to action if one was supplied. An energetic voice should not rush the commercial terms.

## 3. Tutorial for listeners who need time

**Brief:** Guide someone through an upload screen using approved UI labels.

```text
Choose Upload. Select the document you want to use.
[short pause] When its name appears on the screen, choose Continue.
```

Keep each action complete. Use comfortable phrasing and an appropriate voice before adding more pauses. Do not silently invent buttons or imply a screen has changed when its state is unknown. For an interactive agent, wait for the actual user or tool state rather than treating a pause cue as confirmation.

**Acceptance:** Correct UI labels, one understandable step at a time, complete word endings, enough time for the task.

## 4. Two-person conversation

**Brief:** Two fictional colleagues notice a changed meeting room.

```text
Voice A: [curious] Is the meeting still upstairs?
Voice B: They moved it to the room beside reception.
Voice A: Thanks. I'll head there now.
```

The labels above are editorial notation only. Send three `inputs` objects with actual `voice_id` values and only their text. Use REST dialogue with explicit v4, within its combined budget. Do not promise an isolated track per actor. If stems are required, plan separate takes and an edit.

**Acceptance:** Distinct consistent voices, natural handoffs, no spoken labels, complete exchange. For large casts, partition scenes without dropping speakers or exceeding the endpoint budget.

## 5. Long-form narration with one failing passage

**Brief:** A long chapter is accepted except for a middle paragraph that sounds rushed.

Retain the accepted clips. Identify whether the paragraph is overloaded, the voice setting changed, or context is missing. Repair only that paragraph using supported neighboring context. Keep model, voice, and dictionaries consistent. If request IDs have expired, use another supported continuity method rather than pretending stale IDs remain usable.

**Acceptance:** Fixed local pacing, no repeated or missing sentence, smooth neighboring joins, unchanged accepted sections. The provider's maximum input size is not a recommendation to use it for every request.

## 6. South African multilingual delivery

**Brief:** An English introduction includes an approved isiZulu phrase and a local personal name.

Verify every language on the selected model. Preserve the supplied phrase and diacritics. Obtain reliable pronunciation for the name if it is not known. Test the language transition without assuming a single enforced language code will improve it. Keep the normal spelling in subtitles.

**Acceptance:** Meaning preserved, recognizable approved name, acceptable accent, smooth switch. Do not infer support for isiXhosa or all South African languages from support for English, Afrikaans, and isiZulu. Use a qualified reviewer when pronunciation cannot be judged reliably.

## 7. Customer-support agent that interrupts

**Brief:** The agent sounds friendly but cuts in while customers spell an email address.

Read the actual mode and turn configuration. Test patient turn-taking and available spelling-patience controls. Keep email values machine-readable for tools. Verify that an acknowledgment and a correction have appropriate interruption behavior. If the caller asks for a moment, use a configured silence mechanism such as `skip_turn`.

**Acceptance:** Complete identifier captured, no repeated apology loop, correct tool argument, stale audio stops on correction. A new tone prompt alone does not solve turn detection.

## 8. Fictional character with exact physical rhythm

**Brief:** A game character must stumble through a line with precisely timed breaths and recovery.

Try an appropriate v4 voice with sparse cues if the timing is flexible. For a supplied acted performance, consider Voice Changer after checking its language and duration support. Keep gameplay effects separate. Preserve the whole word before each edit; do not cut phonemes to hit a timestamp.

**Acceptance:** Intended rhythm, intelligible words, stable character identity, no accidental background sounds. A tag is a direction, not an animation event or a guaranteed breath placement.

## 9. A measured pause inside a timed clip

**Brief:** An otherwise fixed voiceover needs exactly 750 ms of silence before its final sentence.

Use natural speech cues for performance and create the exact gap in the edit after generation. Locate the audible end of the previous phrase and beginning of the next. Preserve tails and breaths where they belong. Measure the exported timeline. Do not use a fabricated `[pause 750ms]` control or SSML on v4.

**Acceptance:** Measured gap, intact words, correct overall duration, and no unsupported timing claim.

## 10. Repairing a live model migration

**Brief:** A pipeline was changed from Flash to v4 but still sends legacy speed and style settings.

Check the actual endpoint and tool schema. Remove incompatible settings and preserve the intended pacing through voice choice and supported direction. If it incrementally streams text, change the protocol deliberately, including message shapes and finalization. Compare an accepted baseline before rollout.

**Acceptance:** Supported model/route/settings, complete audio, no silent fallback, no claim that all old controls remain equivalent.
