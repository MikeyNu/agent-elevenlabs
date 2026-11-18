# Use the right audio operation

Verified 18 November 2026. Use this route when repeated text direction does not match the required performance, or the task starts with existing audio. Do not regenerate accepted speech merely to apply a downstream effect.

## Voice Changer: preserve an acted performance

Use Voice Changer when the user supplies the desired timing, emotion, or delivery in a recording and wants another voice. The documented route is now `POST /v1/voice-changer/{voice_id}` with an audio upload and an explicit model such as `eleven_multilingual_sts_v2`. The old `/speech-to-speech` paths are deprecated even though the documentation URL retains that name. See the [current endpoint](https://elevenlabs.io/docs/api-reference/speech-to-speech/convert) and [changelog](https://elevenlabs.io/docs/changelog).

The model's documented maximum segment is five minutes, and its language coverage is narrower than v4 TTS. Verify the target language before proposing it as a solution. Preserve a clean, unprocessed performance master. Check breaths, plosives, pronunciation, voice identity, and timing after conversion; preservation is a goal to verify, not a guarantee. See the [capability guide](https://elevenlabs.io/docs/overview/capabilities/voice-changer).

Practical sequence:

1. Mark the successful performance and any lines that need rerecording.
2. Resolve a permitted target voice from the account.
3. Convert a difficult representative excerpt.
4. Compare rhythm and expression against the source, then convert the remaining sections.
5. Restore any required music and sound effects from separate tracks.

Do not ask the user to record a reference when a suitable one is already attached or available. Do not pretend TTS tags alone will reproduce an exact acted cadence.

## Dubbing: translate an existing performance

Use Dubbing when translating existing speech while retaining speaker identity and the surrounding program. Current Automatic Dubbing uses **Dubbing v2 Alpha**; Dubbing Studio editing is a different v1 workflow. Confirm that the requested editing features exist on the chosen surface. The [Dubbing overview](https://elevenlabs.io/docs/overview/capabilities/dubbing) documents this distinction and the tradeoff between cloning strength and natural target-language delivery.

Review the source transcript, speaker assignments, target-language meaning, names, and timing. Keep the original video/audio and translations. Check that the translated performance remains faithful, that code switching is intentional, and that background audio is present once rather than duplicated during mixing. Have an appropriate language reviewer resolve uncertain translations or pronunciation. Do not claim dubbing success from an upload-complete status.

## Voice isolation: clean an existing recording

Use voice isolation for unwanted background noise. First decide which sounds belong to the program. Cleaning can remove useful ambience or damage quiet speech, so compare the processed result with the original. Keep the unmodified source. When a music bed is required, mix a known bed separately after the voice is accepted. See [Voice Isolator](https://elevenlabs.io/docs/overview/capabilities/voice-isolator).

## Voice design and cloning

Search existing voices before creating another asset. Choose a voice by perceived age, accent, texture, energy, and delivery appropriate to the brief. For a new design, use the current [Voice Design workflow](https://elevenlabs.io/docs/eleven-creative/voices/voice-design) and exposed tool requirements. A request to choose a voice is not automatically a request to clone someone.

For a clone, use authorized, clean source recordings and verify the training state for the target model. Avoid changing the actor's intended identity through undocumented processing. Once selected, retain the voice ID and approved sample as project references.

## Music, singing, effects, and final mix

For precise song structure, lyrics, or accompaniment, use the current music capability and its own model guidance. A `[singing]` cue in TTS is an exploratory vocal instruction, not a reliable music-production contract. For required effects and background beds, create separate assets and mix them on a timeline.

Match perceived level before comparing takes. Apply compression, EQ, de-essing, or denoising only to an observed issue. Set final loudness and true-peak targets for the actual destination rather than applying one universal value. Verify the export after encoding. If the account exposes audio-effects nodes, apply room, distance, or phone treatment after voice conversion and cleanup so later synthesis does not erase the treatment.
