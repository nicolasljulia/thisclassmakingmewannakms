# CLAUDE.md

Guide for working on this repo. Read this before making changes.

## What this is

A single-page, self-contained HTML web app: a study companion for Georgetown's Arabic 1011 course (Fall 2026, Dr. Elham Alzoubi's section), covering **two textbooks**: Alif Baa (units 1-9, weeks 1-5 of the semester) and Al-Kitaab Part One (lessons 1-5, weeks 5-16).

Live at: `https://<username>.github.io/thisclassmakingmewannakms/` (GitHub Pages, deployed from the `main` branch root).

The whole app is one file: **`index.html`**. There is no build step, no package.json, no bundler. Everything (HTML, CSS, JavaScript, vocab data, lesson content) lives in that one file. Keep it that way unless there's a strong reason to split it up; the person maintaining this values being able to open one file and see everything.

## The most important rule in this codebase: keep the two books separated

This is not a stylistic preference, it's a hard requirement the site was explicitly rebuilt around. Alif Baa and Al-Kitaab are two different textbooks with two independent numbering schemes ("Unit 4" of Alif Baa and "Lesson 4" of Al-Kitaab are unrelated), and every piece of content on the site needs to make it obvious, at a glance, which book it's from.

**How this is implemented, and how to extend it correctly:**

- `BOOKS` is the single source of truth for book metadata: `[{id:'alifbaa', label:'Alif Baa', unitLabel:'Unit', unitCount:9}, {id:'alkitaab', label:'Al-Kitaab', unitLabel:'Lesson', unitCount:5}]`.
- Every vocab entry, lesson, conjugation verb, and homework entry carries a `book` field (`'alifbaa'` or `'alkitaab'`). Vocab additionally carries `unit`, which means "unit number" for Alif Baa entries and "lesson number" for Al-Kitaab entries, scoped by the `book` field, not a global counter. **Never filter or display vocab, lessons, or conjugations by `unit` alone without also checking `book`.** Unit 4 of Alif Baa and Lesson 4 of Al-Kitaab are both `unit:4` in the data; only the `book` field tells them apart. (This bit us once already: the Numbers 0-10 lesson used to filter `VOCAB` by `unit===4` with no book check, which would have silently pulled in Al-Kitaab Lesson 4 vocabulary too. Now fixed with a `v.book==='alifbaa'` guard, don't remove it.)
- Vocab also carries `type` (one of `noun, verb, adjective, pronoun, question, number, particle, phrase`, see `WORD_TYPES` / `WORD_TYPE_LABELS`), independent of `book`. Every entry in both `ALIFBAA_VOCAB` and `KITAAB_VOCAB` has one.
- **Lessons**: `addLesson(title, body)` tags whatever book was last set with `setLessonBook('alifbaa' | 'alkitaab')`. All 18 Alif Baa lessons are added first (book defaults to `'alifbaa'`), then `setLessonBook('alkitaab')` is called once before the 10 Al-Kitaab lessons. If you add more lessons, make sure `setLessonBook` has been called with the right value before your `addLesson` calls, the function doesn't take a book argument itself.
- **The Lessons tab** (`renderLessonsList`) loops over `BOOKS` and renders a separate `<h2>` heading and grid for each book's lessons. Don't collapse this back into one flat grid. The per-book sequential numbering shown here ("Lesson N") is a tab-scoped position counter, not the vocab `unit` field, both books use the word "Lesson" for it regardless of a book's `unitLabel`; don't conflate the two.
- **Flashcards and Matching** both have a book `<select>` that's queried first; the unit/lesson dropdown in Flashcards is repopulated based on the chosen book's `unitCount` and `unitLabel`. Flashcards additionally filters by word `type` and by known/unknown `status`, independent of book and unit (all four must match); see "Flashcard known-word tracking" below. If you add a new practice mode with a unit filter, give it the same two-step (book, then unit) selection, not a flat 1-14 unit list.
- **Site-wide transliteration toggle**: a button in the header (`#translitToggle`, next to the tab nav) controls `globalShowTranslit`, persisted via `loadProgress`/`saveProgress` under the `ar1011_showTranslit` key. It works via a single CSS rule, `body.hide-translit .tr-toggle{display:none;}`, toggled by `applyTranslitVisibility()` adding/removing a `hide-translit` class on `<body>`. Any transliteration you add anywhere on the site (flashcards, quiz prompts and explains, lesson reference tables) needs a `tr-toggle` class on the element that wraps it (or an ancestor) to participate; this CSS approach is what lets it work on lesson content that's built once as a static string at load time, not just on dynamically re-rendered views. It deliberately does not touch inline transliteration mentioned in lesson prose paragraphs (as opposed to a dedicated table column or a quiz prompt/explain), since untangling that from the surrounding sentence isn't worth the churn; if you add a new lesson table with a transliteration column, tag it the same way.
- **Conjugations** groups the picker grid by book the same way Lessons does. The 12 Alif Baa verbs and 12 Al-Kitaab verbs live in one `CONJUGATIONS` array, distinguished only by `book`, keep that field on any verb you add. This is also the only source of truth for verb paradigms; there is no separate `VERBS_FULL`/`VERB_CITATIONS` anymore (see "Verb data" below).
- **Homework** has its own book `<select>` and filters the `HOMEWORK` array by `book` before grouping by `week`. Alif Baa is weeks 1-5, Al-Kitaab is weeks 5-16 (they share week 5, Alif Baa finishes and Al-Kitaab starts in the same week), so week numbers alone don't disambiguate either, the `book` field does.
- When you add a new quiz category, gender/definiteness/case-style data banks don't currently carry a `book` field since they draw on hand-picked example sentences rather than the full vocab pool, that's fine as-is, but if a future category pulls from `VOCAB` directly, filter by `book` the same way Flashcards does rather than pooling both books together by default. The Vocabulary and Verb Conjugation quizzes are an intentional exception: they already draw from the full pool of both books without a book filter, and that's fine to keep doing for categories where mixing books doesn't create ambiguity.
- **`book:'both'` is a deliberate third value**, reserved for content that's explicitly cumulative across both textbooks, currently only the two Practice Tests in `DRILL_SETS` (see "The Drills tab" below). It is not a loophole for being lazy about tagging, it's narrower than the Vocabulary/Verb Conjugation exception above: those quizzes draw from both books' pools without the user ever being told so, while `book:'both'` content is explicitly labeled and rendered in its own separate UI section precisely because mixing the books is the point (a mock exam covering the whole semester). Don't reach for `'both'` to avoid picking a book for ordinary new content, if it's from one book's material, tag it with that book.

If you're ever unsure whether something needs a book tag, the test is: could this fact or example sentence be confused with something from the other book if the label were removed? If yes, tag it.

## Architecture

- Plain HTML + vanilla JavaScript. No React, no frameworks, no build tools.
- One `<style>` block with CSS custom properties for theming (light/dark via `prefers-color-scheme` and a `data-theme` override).
- One `<script>` block containing:
  - **Data**: `ALIFBAA_VOCAB` + `KITAAB_VOCAB` (concatenated into `VOCAB`, 325 entries total, each with `type` and `book`), `BOOKS`, `ALPHABET` (28 letters), `PRONOUNS` (14-person paradigm, used by the Pronouns quiz and Object Pronoun Suffixes lesson), `CONJUGATIONS` (24 full worksheets, the single source of truth for verb conjugation data, see "Verb data" below), `CONJ_PRONOUNS` / `CONJ_PERSON_LABELS` (the 13-slot Arabic/English person labels `CONJUGATIONS` forms are indexed by), `GENDER_BANK` (28 entries), `DEFINITENESS_BANK` (20 entries), `CASE_BANK` (13 entries), `RECOGNITION_BANK` (sentences/phrases tagged for the Word Recognition quiz, see below), `SENTENCE_TYPE_BANK` (16 entries), `PLURAL_BANK`, `QWORDS`, `QWORD_EXAMPLES` (full-sentence fill-in-the-blank items mixed into the Question Words quiz, see `genQWordQuestions`), `CROSSWORD`, `HOMEWORK` (60 day entries), `LESSONS` (29 entries, built via `addLesson`), and the Drills-only banks `NISBA_BANK`, `POSSESSIVE_IDENTIFY_BANK`, `POSSESSIVE_PRODUCE_BANK`, `POSSESSIVE_TRANSLATE_BANK`, `SUBJECT_PREDICATE_BANK`, `READING_PASSAGES`, and `PRACTICE_TEST_BANK` (see "The Drills tab" below).
  - **A tiny router**: `go(tab, param)` swaps the contents of `#main` based on which of the nine tabs (Home, Lessons, Flashcards, Matching, Quiz, Drills, Crossword, Conjugations, Homework) is active. No URL hash routing, no history API, just direct DOM swaps.
  - **Render functions**: one per tab.
  - **Flashcard known-word tracking**: `knownWords` (an object keyed by `vocabKey(v)` = `book|en|ar`, loaded/saved via `loadProgress`/`saveProgress` under the `ar1011_knownWords` localStorage key) records which vocab the learner has marked "I know this" / "Still learning" from the Flashcards tab. It's per-browser, not synced anywhere. The key includes `en` and `ar` together (not just `en`) because a handful of `KITAAB_VOCAB` entries share an English gloss (e.g. two different entries both glossed "work"); `book+en+ar` is verified unique across all 325 entries.
  - **A generic quiz engine**: `startQuiz(main, cat)` drives all 17 quiz categories off a shared question-rendering loop. Each category has its own `genXQuestions(n)` generator function returning freshly randomized question objects (`{prompt, options, correct, explain}`). To add a category: write a `genXQuestions` function, add an entry to `QUIZ_CATEGORIES`, wire it into the `genQuestions()` switch. The six Al-Kitaab-grammar categories (Verb Forms, Idafa, Participles, Hollow Verbs, Verbal Noun, Connectors) each draw from a small, lesson-sourced bank (`VERB_FORM_HINTS`/`VERB_FORM_TEMPLATES` plus a `form` field on the relevant `CONJUGATIONS` entries, `IDAFA_BANK`, `PARTICIPLE_BANK`, `HOLLOW_VERB_BANK`, `MASDAR_BANK`, `CONNECTORS_BANK`); none of these invent content, every entry traces back to a table or sentence already in the corresponding Al-Kitaab lesson.
  - **The Drills tab**: a second, deliberately separate practice engine from the Quiz tab above. Quizzes are multiple-choice and scored; Drills are reveal-answer and unscored, prompt first, a "Reveal Answer" button that shows the answer/explanation and disappears, a "Jump to:" dropdown plus Previous/Next buttons for freely moving between items in any order (no forced sequential flow), and a progress indicator ("item N of M"). Every drill set is a flat array of generic `{prompt, reveal}` items (both HTML strings; an item may optionally carry `group`, a section label used to group the jump dropdown's options, see Practice Tests below), built by a `buildXItems()` function and registered in the `DRILL_SETS` array as `{id, book, label, desc, build}`. `renderDrills(main, setId)` shows the picker grid (grouped by `BOOKS` like Lessons/Conjugations, plus a separate un-grouped "Practice Tests" section for `book:'both'` sets) when `setId` is empty, or hands off to `startDrill(main, setId)` to run a set. `startDrill` calls `.build()` fresh each time (so randomized sets like the nisba/possessive/subject-predicate drills reshuffle per run), builds the jump dropdown from the item list, and renders whichever item `drillState.idx` points at; Previous/Next just move `idx` and re-render, the jump dropdown sets `idx` directly, nothing about the engine assumes items are visited in order. To add a new drill set: write a `buildXItems()` returning `{prompt, reveal}` objects, add an entry to `DRILL_SETS`. Current sets: Nisba Adjective Formation, three Possessive Pronoun Suffix drills (identify/produce/translate), Identify Subject and Predicate, Nominal or Verbal (reuses `SENTENCE_TYPE_BANK` plus extra items), the two reading-comprehension passages (`READING_PASSAGES`, rendered with `passageHeaderHtml`/`buildPassageItems`), and the two Practice Tests (`PRACTICE_TEST_BANK`, rendered with `buildPracticeTestItems`, which tags every item's `group` with its section label). When building a drill item's HTML, wrap only the parts that are actually Arabic in `.arabic`/`big-ar`, don't blanket-wrap a whole prompt or reveal string, several Practice Test sections mix English instructions with Arabic word banks or are English-only (e.g. "bayt (house)"), and forcing RTL on English text renders it backwards. The Practice Tests originally included two open-ended "take your own photo and describe it" sections (Picture Vocabulary, Picture Description); those were cut since there's no fixed answer to reveal in this format, so each test's sections now run I, II, III, VI, VII...XII (the gap at IV/V is intentional, it matches the instructor's real quiz numbering minus the sections that don't translate to a digital drill).
  - A helper called `mkEl(htmlString)` builds a DOM element from an HTML string via `innerHTML` and returns `firstElementChild`. **Two gotchas, both already bitten us:**
    1. If the HTML string has more than one top-level element, everything after the first is silently dropped. Always wrap multi-element HTML in a single container `<div>...</div>`.
    2. `<tr>` and `<td>` elements can't be created by setting `innerHTML` on a plain `<div>`, the browser's HTML parser silently drops table rows/cells parsed outside a `<table>` context. Build the whole `<table>...</table>` as one string (or at least wrap row HTML in a `<table>` before parsing) rather than creating `<tr>` elements one at a time with `mkEl`.
  - Data blocks that embed Arabic text inline inside a larger English sentence (like `HOMEWORK` topic titles, e.g. `"Lesson 1: <span class='arabic'>...</span> (I am Maha)"`) need the Arabic wrapped in `<span class='arabic'>` for correct right-to-left rendering. Note the **single quotes** on `class='arabic'` when the surrounding JS string itself uses double quotes, mixing quote styles there will break the string literal (this happened once already while adding the Homework tab).

## Verb data: `CONJUGATIONS` is the only source of truth

There used to be two separate, partially-overlapping verb data structures: `VERBS_FULL`/`VERBS_PARTIAL`/`VERB_CITATIONS` (backing the Verb Conjugation quiz, Alif Baa only, and two of those six verbs capped at 5 confirmed persons) and `CONJUGATIONS` (backing the Conjugations reference tab, all 24 verbs across both books, full paradigms). These have been merged: `VERBS_FULL`/`VERBS_PARTIAL`/`VERB_CITATIONS` are gone, and both the Conjugations tab and the Verb Conjugation quiz (`genVerbQuestions`) now read directly from `CONJUGATIONS`, indexed with `CONJ_PRONOUNS` (Arabic) / `CONJ_PERSON_LABELS` (English), both 13 slots long (`CONJUGATIONS[i].forms` is also 13 slots: singular x5, dual x3, plural x5; see the comment above `CONJUGATIONS` for the exact index order). Don't reintroduce a separate verb-data structure for a new feature, extend `CONJUGATIONS` instead.

Six of the 24 verbs have a `note` field (a short irregularity explanation, sourced from `reference/conjugations.md`'s "Notes on irregular forms" section): aHabba, araada, akala, qara'a, sakana (Alif Baa), and tarjama (Al-Kitaab, the one quadriliteral verb). The Conjugations tab shows this note when present; don't add a `note` to a verb that's actually regular within its own form's template.

## Content rules (non-negotiable, checked and enforced already)

1. **No em dashes anywhere on the site.** Not in lesson prose, not in quiz prompts or explanations, not in data files, not in these reference docs either. Verified to a zero count repeatedly. If you add new prose, don't use em dashes (Unicode backtick-u2014-backtick, or the `&mdash;` HTML entity); restructure the sentence instead. Check with:
   ```
   python3 -c "print(open('index.html', encoding='utf-8').read().count(chr(0x2014)))"
   ```
   should print `0`.
2. **No "AI-typical" phrasing.** Avoid robotic, formulaic sentence patterns and filler. Read new prose out loud; if it sounds like a template, rewrite it.
3. **No subtitle taglines under page headers, and no footer disclaimer.** Both were deliberately removed. Don't add them back.
4. **Definiteness, Gender, Case Endings, Sentence Type, and Word Recognition quizzes must not show the English translation in the prompt, only after the user answers.** English in the pre-answer prompt lets someone guess the grammatical answer from English word order or natural gender instead of reading the Arabic. Vocabulary, Pronouns, and Question Words quizzes are the opposite case, translation IS the thing being tested there, so English belongs in those prompts.
5. **Verb Conjugation quiz prompts show the pronoun and the unconjugated (citation-form) verb in Arabic script**, not English person labels. Use `CONJ_PRONOUNS[pIdx]` and `v.root` (from `CONJUGATIONS`).

## Accuracy rules

- This content is used alongside a real class. Don't invent vocabulary, example sentences, or grammar rules that aren't backed by either textbook or the instructor's handouts (see `reference/course-info.md` for exactly which lessons came from which source, book by book).
- If you're not sure a conjugated verb form, plural, or grammar rule is correct, don't guess. Say so, or leave it out. All 24 verbs in `CONJUGATIONS` now have complete, cross-checked 13-person paradigms; don't add a 25th without a source to confirm the exact spelling, and don't hand-type Arabic you're adding to a data bank, copy it from an already-verified source in the file instead (a single wrong diacritic is easy to introduce and hard to spot by eye).
- `RECOGNITION_BANK`'s sentences are all reused verbatim from `CASE_BANK` or from example sentences already written into the Nominal Sentence / Idafa / Demonstrative Pronouns / Pronouns lessons, not newly invented. If you add more entries, pull real sentences from those existing, already-vetted sources (or the textbook/handouts directly) rather than writing new Arabic by hand.
- The `reference/` files are portable snapshots of the site's data, useful for quick lookups without opening `index.html`. `index.html` is always the source of truth; if you edit content in it, the reference files drift out of date until someone regenerates them (no automated sync exists).

## Testing workflow

There's no test suite, but changes should be verified the same way this was built and debugged:

1. **Syntax check the extracted JS** first:
   ```
   python3 -c "
   import re
   html = open('index.html', encoding='utf-8').read()
   m = re.search(r'<script>(.*)</script>', html, re.S)
   open('/tmp/extracted.js','w',encoding='utf-8').write(m.group(1))
   "
   node --check /tmp/extracted.js
   ```
2. **Runtime-check with a headless browser**. Load the file, click through every tab, open a handful of lessons from both books, start each quiz category and answer a question, play a round of the matching game with both books selected, fill in the crossword, mark a flashcard known and confirm the count/filter update, and switch the Homework, Flashcards, Matching, and Conjugations book selectors. Watch for `pageerror` events, not just console output, several real bugs here (the `mkEl` multi-element gotcha, the `<tr>`-outside-`<table>` gotcha, a mismatched-quote syntax error, a forward-reference to a `const` declared later in the file) only showed up this way, not from reading the code.
3. Take a screenshot of anything visual you changed and actually look at it, especially Arabic text and anything involving the book selectors. Rendering bugs are easy to miss by reading code alone.

## Deployment

GitHub Pages, deployed from `main`, root folder. The live file must be named exactly `index.html` at the repo root. To update the live site: commit a new `index.html` to `main` and wait about a minute for Pages to rebuild. No CI, no actions, no review step; whatever is on `main` is what's live.

## Repo layout

```
index.html              the whole app (source of truth)
CLAUDE.md                 this file
TODO.md                   outstanding work handed off between sessions
reference/
  vocabulary.csv           325 vocab entries (both books), with book and type columns
  grammar-guide.md          all 29 lesson bodies (18 Alif Baa + 11 Al-Kitaab)
  conjugations.md           all 24 verb conjugation worksheets, grouped by book, with irregularity notes
  homework-schedule.md      the full day-by-day assignment schedule, both books
  course-info.md            what's covered, source attribution, known source-PDF issues
```
