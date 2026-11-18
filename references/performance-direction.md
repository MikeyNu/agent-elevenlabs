# Performance direction

Use this reference to turn approved content into a convincing spoken performance. The writing and audition process below is an editorial method, not a vendor guarantee or a mandatory house style.

## Contents

- [Preserve the content contract](#preserve-the-content-contract)
- [Build a natural spoken script](#build-a-natural-spoken-script)
- [Apply model-supported direction](#apply-model-supported-direction)
- [Control pacing and duration](#control-pacing-and-duration)
- [Audition efficiently](#audition-efficiently)

## Preserve the content contract

Decide whether the user wants a rewrite, performance annotation, or generation of the supplied words. For annotation-only work, compare canonical and synthesis text after accounting for deliberate markup. Keep quotations exact. Never turn an allegation into a fact, a possible outcome into a certainty, or a question into a confident assertion through wording or sarcastic delivery.

Move production notes into a separate field. A TTS text box contains the words to perform; it is not a prompt for a scene. A sentence such as “Read this like a friendly presenter” may become audible. Likewise, `(laughing)` is not reliable control markup. The vendor's [tag guide](https://elevenlabs.io/blog/elevenlabs-audio-tags-list) identifies unsupported models and incorrect brackets as causes of spoken directions.

Keep visible words and synthesis substitutions separately versioned. If the user supplies text that sounds awkward but requires exact wording, improve voice, punctuation only where allowed, and performance. Explain a wording limitation instead of quietly changing it.

## Build a natural spoken script

Apply these choices only where rewriting is authorized:

1. Establish who or what the listener is hearing about before relying on pronouns.
2. Put one principal thought in each breath-sized unit. Split dense nested clauses.
3. Prefer concrete verbs and ordinary phrasing over formal connective phrases.
4. Vary short and longer sentences according to the meaning. Avoid identical rises and falls on every line.
5. Use contractions where they fit the speaker and audience. Keep precise terminology where necessary.
6. Let contrast identify the stress word. Usually one emphasized word is enough for a sentence.
7. Make transitions serve the content. Do not insert generic commentary, moral lessons, or repeated questions merely to fill time.

Example, a fictional product walkthrough:

| Written copy | Spoken adaptation |
|---|---|
| “Upon completion of the upload process, the system will initiate analysis.” | “Once the upload finishes, analysis starts.” |
| “It is important to note that the original file will remain accessible.” | “You can still open your original file.” |

Natural speech does not require constant imperfection. Add a hesitation, laugh, breath, or self-correction only when the character or scene calls for it. Do not add fake uncertainty to important numbers. For social commentary, orient the listener, state the meaningful detail, give a grounded reaction, and close only when a closing serves the clip.

## Apply model-supported direction

V4 and v3 accept short natural-language cues in square brackets. V4 Turbo also supports tags on its real-time route. These cues are open-ended rather than a fixed API enum. See the [official tag help](https://elevenlabs.io/docs/help-center/product/core-capabilities/text-to-speech/how-do-audio-tags-work-with-eleven-v3-and-v4).

Use this small palette as a starting point, then audition:

| Intent | Candidate cue | Use carefully |
|---|---|---|
| Genuine question | `[curious]` | Do not make factual narration sound uncertain |
| Quiet reassurance | `[softly]` | Quiet need not mean slow or breathy |
| Clear contrast | Sparse CAPITALS | Repeated capitals can sound shouted |
| Discreet amusement | `[chuckles]` | Avoid during distress or serious allegations |
| A considered beat | `[short pause]` | Duration remains approximate |
| A specific vocal texture | `[low, gravelly voice]` | Check identity consistency and intelligibility |

Put the cue near the words it should influence. Start with the simplest direction, then add detail only when an observed result requires it. Avoid incompatible stacks such as excitement, whispering, rage, and laughter on the same short phrase. Do not assume a cue resets at a newline or controls the whole remaining script. Test scope. Live-agent tag behavior has separate guidance in [realtime agents](realtime-agents.md).

The [v4 prompting guide](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices) warns that ambiguous cues may become effects rather than vocal delivery. Describe a voice quality clearly when that is the intention. Put precisely timed effects on separate tracks.

Original example, contrasting two acceptable readings:

```text
Plain: We can try again tomorrow. There's still time.
Directed: [softly] We can try again tomorrow. [short pause] There's still time.
```

The directed version is a candidate, not automatically an improvement. An already gentle voice may deliver the plain line more naturally.

## Control pacing and duration

Use periods for complete thought boundaries, commas for lighter internal phrasing, and paragraph breaks for structure. Ellipses often imply hesitation. Reserve them for an intended trailing thought or uncertainty rather than adding them throughout confident narration.

V4/v3 use tags and punctuation instead of SSML pauses. Legacy Multilingual v2 and Flash models support documented break markup. See [pause support](https://elevenlabs.io/docs/help-center/product/core-capabilities/text-to-speech/how-can-i-add-pauses). A cue such as `[pause 0.75s]` is not a precise timing API.

For a duration target, estimate words from the chosen voice's measured rate, reserve room for reactions and silence, and generate. Shorten redundant wording before forcing an unnaturally fast delivery. For an exact gap, retain full word endings, insert silence on the timeline, and remeasure. Keep a little editing margin when fitting speech to picture; the amount is project-specific.

Do not use unsupported speed controls on v4. A mood change is not inherently a speed change. Ask for slower phrasing only when pace is actually the problem.

## Audition efficiently

Select an excerpt that exposes the hard parts, not a generic greeting. Compare candidates at comparable playback levels. First identify the failure: voice mismatch, awkward words, wrong emphasis, unreliable cue, or pronunciation. Change only that variable.

Keep an accepted voice and pronunciation plan across episodes. Record which example worked and the relevant model/settings, without treating one seed or take as deterministic. When text cannot express the desired rhythm efficiently, use [a performed source](performance-alternatives.md) rather than escalating the cue count.

When ordinary direction misses the brief, consult [community practice](community-practice.md). Compare direction density instead of assuming a universal count: plain text, a cue at a meaningful change, then brief line directions only if needed. Keep the spoken words fixed and judge emotion separately from naturalness. For an overacted take, examine unintended exclamation marks, full capitals, and repeated reactions before adding more cues. Source reports differ by voice, genre, and model.
