# Pronunciation and localization

Verified against official sources on **2026-11-18**. Use this reference for names, brands, abbreviations, numbers, multilingual speech, and accent requirements. Keep pronunciation decisions separate from rewriting the underlying content.

## Preserve meaning before optimizing speech

Maintain two representations when pronunciation changes are needed:

1. **Canonical text:** approved wording for captions, transcripts, factual comparison, and future edits.
2. **Synthesis text:** model-compatible directions and explicitly approved spoken renderings.

Keep a small mapping from each changed expression to its intended spoken form and reason. Default to preserving original numbers and wording. Expand or respell only when the intended reading is known and the change improves delivery. Do not transform every abbreviation or number with a broad regular expression.

For exact-word tasks, keep the canonical wording intact and prefer a pronunciation dictionary. Never claim verbatim speech when lexical substitutions were introduced without authorization. Do not strip meaningful parentheses from source material merely because parenthetical stage directions are unsuitable.

## Choose a pronunciation method

| Problem | First action | Escalation |
|---|---|---|
| Personal or place name | Obtain a trusted pronunciation or supplied recording | Test verified IPA or an approved alias |
| Repeated brand or technical term | Add a versioned dictionary rule | Audition in several sentence contexts |
| Acronym | Determine whether it is letters, a word, or an expansion | Store the chosen reading explicitly |
| Unambiguous numeric content | Test the original expression | Introduce a verified spoken rendering only if needed |
| Ambiguous date or abbreviation | Resolve meaning from the source or ask narrowly | Do not guess from the model's reading |

The [pronunciation guide](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices) documents v4 native IPA with forward slashes and quoted notation, such as `"/IPA_transcription/"`. Use real validated phonetics, including stress where needed. This placeholder describes syntax; it is not generation text. Do not manufacture confident IPA for an unfamiliar name. Test the actual voice and phrase.

[Dictionary documentation](https://elevenlabs.io/docs/eleven-agents/customization/voice/pronunciation-dictionary) supports phoneme rules on v4, v4 Turbo, v3, and Flash v2; other models need aliases. Inline XML phoneme tags have narrower support. For non-English phonemes, prefer v4: the [programmatic guide](https://elevenlabs.io/docs/eleven-api/guides/how-to/text-to-speech/pronunciation-dictionaries) names v4/v4 Turbo, while the agent guide also names v3. Verify a required v3 workflow instead of assuming parity.

The PLS tutorial uses case-sensitive matching. API rules also expose `case_sensitive` and `word_boundaries` flags, documented on [2 March 2026](https://elevenlabs.io/docs/changelog/2026/3/2). Inspect those flags before adding capitalization variants. Preserve dictionary versions. The [TTS endpoint](https://elevenlabs.io/docs/api-reference/text-to-speech/convert) permits three locators, applied in order. Listen to verify the result.

## Check numbers and symbols deliberately

The following are original workflow examples, not ElevenLabs guarantees:

| Source | Possible intended reading | Verification |
|---|---|---|
| `R1,250.50` | one thousand two hundred and fifty rand and fifty cents | Preserve currency, magnitude, and cents |
| `0018` as a code | zero zero one eight | Preserve both leading zeros |
| `0.25` as a decimal | zero point two five | Do not turn it into twenty-five |
| `03/04/2026` | unresolved until locale or source is known | Do not assume March or April |
| `14:30` | fourteen thirty, or half past two in the afternoon | Preserve the time and follow context |
| `API` | A P I | Confirm letters are intended rather than an expansion |

These examples assume the stated meanings. Do not apply them automatically to unrelated contexts. Keep quantities, percentages, currencies, units, contact details, URLs, and reference codes on a pronunciation checklist. Compare important values against the source after every rewrite.

The [normalization help](https://elevenlabs.io/docs/help-center/product/core-capabilities/text-to-speech/how-do-i-select-the-language-and-accent) explains that a supported `language_code` can help with short or numeric-only input. The endpoint offers normalization modes; do not assume automatic normalization selects the correct business meaning.

## Select language and accent explicitly

The current [model catalog](https://elevenlabs.io/docs/overview/models) lists English (`en`), Afrikaans (`af`), and Zulu (`zu`) for v4. Do not infer support for every South African official language. Check the actual target language, rather than relying on a broad multilingual claim. Preserve accents and diacritics in text. Use the endpoint's documented language identifiers, not an assumed `en-ZA` or `zu-ZA` locale value.

[V4 native accent handling](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/eleven-v4) changes an older assumption: cross-language generation aims for a native accent in the target language instead of carrying the recording's original-language accent across. Same-language accent preservation is documented separately. Audition any project requiring a precise regional accent or consistent cross-language identity; neither a tag nor a language code guarantees that result.

For code switching, verify every language, then audition the actual transition. Avoid forcing one language across mixed-language text without checking its effect. If transitions fail, split at complete phrases while preserving the intended flow. Never replace unsupported language with translation unless the user requested it.

## Accept the result using evidence

Listen for names, stress, language transitions, figures, spelling sequences, and unnatural pauses. Compare the synthesis mapping with the canonical text. Inspect captions independently so they retain normal spelling instead of IPA, aliases, or directions. Record unverified pronunciations as unresolved. Transcription can help detect omissions, but agreement with an automatic transcript does not establish pronunciation accuracy.

Prefer current model-specific guidance over generic accent help when they conflict. Distinguish supported language from acceptable regional delivery, and supported pronunciation syntax from a pronunciation that has actually been heard and approved.
