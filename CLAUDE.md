# CLAUDE.md

Guide for working on this repo. Read this before making changes.

## What this is

A single-page, self-contained HTML web app: a study companion for Georgetown's Arabic 1011 course (Fall 2026, Dr. Elham Alzoubi's section), built from the Alif Baa textbook (units 1-9) and the instructor's supplementary grammar handouts.

Live at: `https://<username>.github.io/thisclassmakingmewannakms/` (GitHub Pages, deployed from the `main` branch root).

The whole app is one file: **`index.html`**. There is no build step, no package.json, no bundler. Everything (HTML, CSS, JavaScript, vocab data, lesson content) lives in that one file. Keep it that way unless there's a strong reason to split it up; the person maintaining this values being able to open one file and see everything.

## Architecture

- Plain HTML + vanilla JavaScript. No React, no frameworks, no build tools.
- One `<style>` block with CSS custom properties for theming (light/dark via `prefers-color-scheme` and a `data-theme` override).
- One `<script>` block containing:
  - **Data**: `VOCAB` (225 entries, each `[english, arabic, transliteration, unit, type]` where `type` is one of `noun, verb, adjective, pronoun, question, number, particle, phrase`, see `WORD_TYPES` / `WORD_TYPE_LABELS`), `ALPHABET` (28 letters with all four forms), `PRONOUNS` (14-person paradigm, in a fixed order that `VERBS_FULL` indexes into: I, you-m-sg, you-f-sg, he, she, we, you-m-dual, you-f-dual, they-m-dual, they-f-dual, you-m-pl, you-f-pl, they-m-pl, they-f-pl), `VERBS_FULL` / `VERB_CITATIONS` / `VERB_GLOSSES` / `VERB_NOTES` (all 12 verbs now have complete 14-person paradigms; see Conjugations tab below), `GENDER_BANK`, `DEFINITENESS_BANK`, `CASE_BANK`, `RECOGNITION_BANK` (sentences/phrases tagged for the Word Recognition quiz, see below), `QWORDS`, `CROSSWORD` (a hand-verified 6-word grid), and `LESSONS` (built via repeated `addLesson(title, htmlBody)` calls).
  - **A tiny router**: `go(tab, param)` swaps the contents of `#main` based on which of the seven tabs (Home, Lessons, Flashcards, Matching, Quiz, Crossword, Conjugations) is active. No URL hash routing, no history API, just direct DOM swaps.
  - **Conjugations tab** (`renderConjugations` / `renderConjugationDetail`): a reference tab, not a quiz, listing all 12 verbs in `VERBS_FULL` fully conjugated (Singular/Dual/Plural tables using `PRONOUNS` indices `[0,1,2,3,4]` / `[6,8,9]` / `[5,10,11,12,13]`), plus an irregularity note from `VERB_NOTES` where one exists (aHabba, araada, akala, qara'a, sakana).
  - **Render functions**: one per tab (`renderHome`, `renderLessonsList` / `renderLessonDetail`, `renderFlashcards`, `renderMatching`, `renderQuizMenu` / quiz engine, `renderCrossword`). Flashcards filter by unit, word type, and known/unknown status independently (all three must match); `fcState` holds `unit`, `type`, and `status`, all defaulting to `'all'`.
  - **Known-word tracking**: `knownWords` (an object keyed by `v.en`, loaded/saved via `loadProgress`/`saveProgress` under the `ar1011_knownWords` localStorage key) records which vocab the learner has marked as known from the Flashcards tab. It's per-browser, not synced anywhere. `v.en` is guaranteed unique across `VOCAB` (checked when this was added), so it's safe as a stable key even if entries get reordered later; if new entries are added, keep English glosses unique or switch to an explicit id.
  - **A generic quiz engine**: `startQuiz(main, cat)` drives all 8 quiz categories off a shared question-rendering loop. Each category has its own `genXQuestions(n)` generator function that returns freshly randomized question objects (`{prompt, options, correct, explain}`) from that category's data bank. To add a new quiz category: write a `genXQuestions` function, add an entry to `QUIZ_CATEGORIES`, and wire it into the `genQuestions()` switch.
  - A helper called `mkEl(htmlString)` builds a DOM element from an HTML string via `innerHTML` and returns `firstElementChild`. **Important gotcha**: if the HTML string has more than one top-level element, everything after the first gets silently dropped. Always wrap multi-element HTML in a single container `<div>...</div>` when calling `mkEl`. This bit us twice already (see git history / past conversation); don't reintroduce it.

## Content rules (non-negotiable, checked and enforced already)

These came from explicit direction from the person this was built for. Preserve them in any edit:

1. **No em dashes anywhere on the site.** Not in lesson prose, not in quiz prompts or explanations, not in data files. This was scrubbed to a verified zero count. If you add new prose, don't use em dashes (Unicode `\u2014`, or the `&mdash;` HTML entity); restructure the sentence instead (split into two sentences, use a comma, a colon, or "since/because"). Check with:
   ```
   python3 -c "print(open('index.html', encoding='utf-8').read().count(chr(0x2014)))"
   ```
   should print `0`.
2. **No "AI-typical" phrasing.** Avoid robotic, formulaic sentence patterns and filler. Read new prose out loud; if it sounds like a template, rewrite it.
3. **No subtitle taglines under page headers.** Every tab used to have a `<p class="muted">...</p>` under its `<h1>`. These were deliberately removed. Don't add them back.
4. **No footer disclaimer.** Same story, deliberately removed.
5. **Definiteness, Gender, and Case Endings quizzes must not show the English translation in the prompt, only after the user answers.** English meaning in the pre-answer prompt would let someone guess the grammatical answer from English word order or natural gender (e.g. "sister" obviously being feminine) instead of actually reading the Arabic. The English meaning is fine, and useful, in the post-answer `explain` text. Vocabulary, Pronouns, and Question Words quizzes are the opposite case: translation IS the thing being tested there, so English belongs in those prompts.
6. **Verb Conjugation quiz prompts show the pronoun and the unconjugated (citation-form) verb in Arabic script**, not English person labels or bare transliteration. Use `PRONOUNS[pIdx].subj` for the pronoun and `VERB_CITATIONS[verb]` for the citation form. The English gloss can stay alongside in small muted text for context; it doesn't give away a conjugation.
7. **Word Recognition quiz prompts show only the Arabic sentence and its transliteration**, never the English gloss, matching the Case Endings quiz's convention; the English translation only appears afterward, in the `explain` text in parentheses. This keeps the drill testing actual sentence-structure recognition rather than translation.

## Accuracy rules

- This content is used alongside a real class. Don't invent vocabulary, example sentences, or grammar rules that aren't backed by either the Alif Baa textbook or the instructor's handouts (see `reference/course-info.md` for exactly which lessons came from which source).
- If you're not sure a conjugated verb form, plural, or grammar rule is correct, don't guess. Say so, or leave it out. All 12 verbs in `VERBS_FULL` now have complete, instructor-confirmed 14-person paradigms (see `reference/course-info.md`); araada and aHabba were previously limited to 5 confirmed persons until the full paradigms were supplied.
- `RECOGNITION_BANK`'s sentences are all reused verbatim from `CASE_BANK` or from example sentences already written into the Nominal Sentence / Idafa / Demonstrative Pronouns / Pronouns lessons, not newly invented. If you add more entries, pull real sentences from those existing, already-vetted sources (or the textbook/handouts directly) rather than writing new Arabic by hand; a target `word` should always be copy-pasted, not retyped, since a single wrong diacritic is easy to miss and hard to notice by eye.
- `reference/grammar-guide.md` and `reference/vocabulary.csv` are portable snapshots of the content, useful for quick lookups without opening the full `index.html`. `index.html` is always the source of truth; if you edit lesson content or vocab, the reference files will drift out of date until someone regenerates them (there's no automated sync).

## Testing workflow

There's no test suite, but changes should be verified the same way this was built and debugged:

1. **Syntax check the extracted JS** before doing anything else:
   ```
   python3 -c "
   import re
   html = open('index.html', encoding='utf-8').read()
   m = re.search(r'<script>(.*)</script>', html, re.S)
   open('/tmp/extracted.js','w',encoding='utf-8').write(m.group(1))
   "
   node --check /tmp/extracted.js
   ```
2. **Runtime-check with a headless browser** (Playwright is the tool used throughout this project). Load the file, click through every tab, open a handful of lessons, start each of the 8 quiz categories and answer a question, play a round of the matching game, and fill in the crossword. Watch for `pageerror` events, not just console output. This caught two real bugs during development (a bullet-list renderer that silently dropped content, and the `mkEl` multi-element gotcha above), neither of which threw an error a human skim would have caught by reading the code.
3. Take a screenshot or two of anything visual you changed and actually look at it. Rendering bugs (especially around the RTL Arabic text and the crossword grid) are easy to miss by reading code alone.

## Deployment

GitHub Pages, deployed from `main`, root folder. The live file must be named exactly `index.html` at the repo root. To update the live site: commit a new `index.html` to `main` and wait about a minute for Pages to rebuild. No CI, no actions, no review step; whatever is on `main` is what's live.

## Repo layout

```
index.html              the whole app (source of truth)
CLAUDE.md                this file
reference/
  vocabulary.csv          225 vocab entries, portable snapshot of the VOCAB array
  grammar-guide.md         all 18 lesson bodies, portable snapshot for quick reading
  course-info.md           what's covered so far, source attribution, grading context
```
