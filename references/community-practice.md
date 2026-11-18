# Community reports and controlled auditions

Research reviewed **18 November 2026**. Use this reference when evaluating a creator's recipe or solving a delivery problem that the ordinary workflow has not resolved. Do not reload or repeat this research for every generation.

These are firsthand reports, demonstrations, and implementation histories. Their authors' listening judgments have not been independently reproduced here. Public text, settings, code, screenshots, and descriptions were inspected; linked audio/video was not auditioned. Treat reported improvements as candidates for the selected voice, language, model, and task. Keep [model capabilities](model-capabilities.md) authoritative for supported controls.

## Contents

- [Choose a useful experiment](#choose-a-useful-experiment)
- [Keep the comparison interpretable](#keep-the-comparison-interpretable)
- [Handle experimental workarounds](#handle-experimental-workarounds)
- [Source register](#source-register)
- [Assess evidence before reuse](#assess-evidence-before-reuse)

## Choose a useful experiment

| Problem | Candidate method | Decision rule |
|---|---|---|
| Correct words, wrong vocal character | Compare suitable voices on the same representative passage and in the target language. [C1, C10] | Keep other inputs constant; a creator's preferred voice or clone type is not a universal winner. |
| Overacted narration | Remove unintended excitement cues where editing is allowed; compare plain, lightly directed, and, only if needed, line-directed versions. [C6, C7, C8] | Genre, cue type, and voice differ across reports. Do not prescribe a tag quota or assume more emotion is more natural. |
| Precise cadence remains elusive | Perform or reuse a clean source recording and audition [Voice Changer](performance-alternatives.md). [C5] | Evaluate the actual converted timing and identity; conversion does not supply missing acting. |
| Good take has awkward gaps or pace | Preserve it and test a local timeline edit. [C2] | Measure silence; use pitch-preserving time adjustment cautiously and check artifacts. Do not copy one author's percentage. |
| Drama sounds like consecutive readings | Test small, intentional overlaps between separately editable character lines. [C6] | Preserve intelligibility and key words. This is scripted drama editing, not permission for a live agent to interrupt its user. |
| Names or abbreviations are wrong | Hear the default reading in its full sentence, then repair the confirmed error and recheck neighboring words. [C4] | Keep canonical spelling and values; do not build speculative dictionary entries before hearing a problem. |
| A tagged live answer fails on its backup voice | Apply the configured fallback's supported text format and keep cues out of ordinary captions. [C9] | See [realtime agents](realtime-agents.md#handle-cues-across-output-surfaces); do not silently switch models or erase literal bracketed content. |
| Transcript looks correct but the greeting is silent | Reproduce on the actual device and inspect SDK, playback, and connection state. [C12] | A voice-setting change cannot establish that client audio played. Read an issue through its resolution. |

## Keep the comparison interpretable

Use this small protocol only when a comparison will resolve a concrete uncertainty:

1. Save the canonical excerpt, selected voice, model/route, language, settings, dictionaries, and intended effect. Include the hardest name or transition.
2. Create a plain baseline and one changed candidate. For an unresolved direction-density question, add a third candidate with brief line-level directions. Preserve all spoken words when rewriting is not authorized.
3. Hold other inputs constant. If budget permits, use a second take for each condition rather than comparing one lucky take against another condition's first attempt. Record how takes were selected. A seed does not establish determinism.
4. Match playback level and hide candidate labels when practical. Judge content fidelity, naturalness, emotion, identity, pronunciation, and timing separately. Use a fluent listener for the target language. [C1]
5. Keep the accepted clip, record the observed improvement and limitation, and stop when the brief is met. Do not turn a small audition into an unbounded search.

For live agents, also measure first audible sound and first useful spoken content separately. A filler may move the first timestamp while delaying the actual answer. Test a thinking pause, correction, and session opening on the target device. These are evaluation recommendations, not published v4 benchmark results.

## Handle experimental workarounds

**Trailing context:** C3 reports adding a disposable final sentence and cutting it away to improve a terse ending. Its model is unknown. First check complete response consumption, real truncation, and supported context/stitching. Try padding only in an authorized editable offline production, with the extra sentence tracked separately and removed completely. Recheck the desired final phonemes, captions, and export. Never add disposable content to a live response or leave it in an exact-wording deliverable.

**Numeric recipes:** C2's particular stability/similarity values, C6's whisper limit, and showcase claims about tag duration or scope are project observations. Keep current documented defaults as the baseline. Do not promote these into defaults, validator rules, guaranteed milliseconds, or a reason to add unsupported v4 Speed/Style fields.

**Final sound:** Level matching, a targeted de-esser, or local editing can repair technical defects. They do not demonstrate correct emotion. Preserve an unprocessed master and compare the final encoding. Use [listening QA](troubleshooting-qa.md) to decide whether the repair actually helped.

## Source register

Dates below are explicit publication/test dates where visible. A relative forum/social timestamp is left approximate. All sources were reviewed on 18 November 2026. Sources may promote an author's product or services; that does not erase useful detail, but it limits claims of independence.

| ID and original source | Model, date, and reported result | Evidence and transfer limits |
|---|---|---|
| C1. [Lukas Huttis: clone comparison](https://lukashuettis.de/en/videos/elevenlabs-v4-voice-clone-test/) | 19 Oct 2026; v4 instant/professional and Multilingual v2 professional clones of one speaker. His preferred clone differed between English and German. | Same sentences, default settings, matched levels, shuffled playback, linked samples. Affiliate disclosed. One speaker's judgments; clone type, source duration, training state, and model are confounded. |
| C2. [Tools in Production: product voiceover](https://toolsinproduction.com/elevenlabs-v4-voiceover/) | Oct 2026; v4. Reports using a warm cue, selective word emphasis, and export speed/pause edits for a product video. | Specific voice and settings, but no controlled comparison or exposed listening samples in the article. Its numeric pause wording is not a supported timing API. |
| C3. [Tom Rozek: client-production review](https://rozekwrites.com/is-elevenlabs-worth-subscribing-to-a-users-review/) | Model unspecified; 2025-26 article. Reports multiple takes for exact cadence, inconsistent short lines, and the disposable-tail workaround. | States no ElevenLabs affiliation; links contrasting takes and failure examples. Do not apply its historical UI limits or spoken-tag failure to every v4 voice. |
| C4. [Kevin Knauss: audiobook diary](https://insuremekevin.com/i-created-an-ai-audiobook-with-elevenlabs/) | 8 Sep 2026; model unspecified. Reports proof-listening, correcting speaker assignments, expanding an abbreviation, and repairing surname pronunciation. | Finished-project account, screenshots, video link. No controlled error-rate study. Its clone-recording duration and account observations are not current requirements. |
| C5. [Julian Franklin: performed audiobook](https://ai-included.co.uk/writing-how-the-falsehood-was-made) | Undated; `eleven_multilingual_sts_v2`. Reports personally performing chapters, converting voices, and assembling/mastering the results. | Production diary and finished-book link; no paired source/conversion audition here. His categorical dismissal of TTS acting is opinion. Use current endpoint and segment guidance, not historical API or account workarounds. |
| C6. [u/MaTeZZ: v4 radio-drama production](https://www.reddit.com/r/ElevenLabs/comments/1x4b1fu/using_eleven_v4_sfx_and_music_to_make_28minute/) | Approximately Oct 2026; v4. Reports line directions, limiting excessive whispering, checking endings, matching levels, and mixing slight interruptions. | Published production links; also promotes the channel. No controlled ablation. Voice consistency remains an open problem in the author's own questions. |
| C7. [u/Accomplished-Soft821: v4/v3 comparison](https://www.reddit.com/r/ElevenLabs/comments/1wt27e7/elevenlabs_v4_torture_test_v3_comparison/) | Approximately Oct 2026; v4/v3. Same-prompt/speaker showcase; follow-up recommends reducing exclamation marks and full capitals for excessive intensity. | Public comparison media and discussion. Separate demonstrated effects from suggestions. Slider explanations in comments are speculative and do not supersede current documentation. |
| C8. [v4 audiobook quality thread](https://www.reddit.com/r/ElevenLabs/comments/1x9oohj/voice_quality_issues_on_audiobook_narration_in_v4/) | Oct 2026; v4. u/Imchristianjoel reports repeats/glitches with many sound cues. OP u/DarranSmith_author separately reports a service-quality problem and later marks it resolved. | No supplied audio or controlled tag-removal test. Preserve the distinction between two reports; neither establishes an optimal sparse-tag count or an ongoing outage. |
| C9. [Godefroy de Compreignac / Micdrop: live audio tags](https://micdrop.dev/blog/elevenlabs-audio-tags-voice-agent) | 30 Sep 2026; v4 Turbo/Flash v2.5. Reports cue leakage into fallback speech and transcripts; provides stream-handling code and a demo. | Implementer's own product guide. The quoted duration comparison changes both model and tags, so it cannot isolate tag cost. Its regex example is unsafe as a blanket rule for literal bracketed content. |
| C10. [RaftLabs: Czech survey-agent case study](https://www.raftlabs.com/portfolio/voice-ai-survey-agent-for-perfume-brand) | Project Apr-Aug 2026; TTS model unspecified. Team reports improved client acceptance after changing voice with script, model, and latency held constant. | Commercial alpha case study, no published blinded audio scores. Test the real target language; an English or AI-to-AI test cannot establish Czech listener naturalness. |
| C11. [u/ComfyTorpedo: turn-taking discussion](https://www.reddit.com/r/ElevenLabs/comments/1l76nc1/any_conversational_turn_taking_fixes/) | Approximately 2025; model unspecified. OP confirms that enabling `skip_turn` helped their unwanted-interruption problem. | Direct user confirmation without recordings or exact configuration. Use the current supported tool for appropriate waiting behavior; it does not replace endpointing/eagerness controls. |
| C12. [ElevenLabs packages issue 777](https://github.com/elevenlabs/packages/issues/777) | May 2026; TTS model unspecified. A real-iPhone greeting appeared in events but was inaudible; maintainer fix and reporter confirmation follow. | Reproduction, exact SDK versions, and resolution. Earlier workarounds were disproven. A historical client bug is not a reason to pin old SDKs or assume every silence has the same cause. |
| C13. [Angela Tran: character-voice experiment](https://www.linkedin.com/posts/angela-kieuhanh-tran_ai-voices-are-so-obvious-its-always-the-activity-7511525160089436160-CaM2) | 2026, relative date only; v4. Reports successful character cues, but a yawn did not transfer well to a lip-sync system. | Public first-person post and transcript; showcase, not repeated trial. Speech performance and downstream avatar animation require separate evaluation. |
| C14. [Wouter van Haaften: directed voice showcase](https://www.linkedin.com/posts/wouter-van-haaften_generativeai-elevenlabs-voiceai-activity-7512170246493954048-SsUC) | 2026, relative date only; v4. Reports one-script delivery, accent, language, and stress changes in a single take. | Public post/transcript promoting his team's workflow. No full reproducible settings or reliability study. Do not generalize claims about persistent tag scope or guaranteed accents. |

## Assess evidence before reuse

Record whether a source provides a suggestion, a claimed success, a reproducible input, linked examples, repeated comparisons, or an independently confirmed fix. These are different evidence types. Promotion, upvotes, confident prose, and an impressive selected take do not supply missing controls or unsuccessful attempts.

Reject unavailable-page snippets as the basis for a firm technique. During this review, a sparse-tag narration recipe could not be fully opened, so its quota and unspecified punctuation trick were not adopted. Likewise, vendor launch reposts and generic review lists were not treated as independent user experiments.

For each retained project result, save the source, model/route, exact input changes, selected take, listening evidence, and failure conditions. Promote a method into that project's reusable preset only after it works on that project's audio. Keep public experience distinct from verified platform capabilities and from your own results.
