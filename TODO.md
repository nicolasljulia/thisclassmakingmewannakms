# TODO for Claude Code

Outstanding work on the Arabic 1011 Companion site, handed off from here. Read `CLAUDE.md` first, everything below assumes you already know the architecture, the book-separation rule, and the testing workflow described there. Nothing here is code, just a description of what's missing or worth adding; how to build it is up to you.

## 1. More Al-Kitaab-specific quiz categories

The Quiz tab has 10 categories right now, two of them (Sentence Type, Plural Type) written specifically for Al-Kitaab grammar. The Al-Kitaab lessons cover several more grammar points that would make good quiz material but don't have a quiz yet:

- **Verb forms (al-awzaan).** Given a verb (either its dictionary form or its present-tense form), ask which of the ten forms (I through X) it belongs to. The Verb Forms lesson already has the full past/present template table for all ten forms, and the Conjugations tab's 12 Al-Kitaab verbs span Forms I, II, III, IV, and V plus one quadriliteral, real, sourced examples to build questions from rather than needing new ones.
- **Idafa.** Given a two- or three-noun idafa phrase, ask which noun is genitive, or which noun could take ال, or which noun the whole phrase's definiteness comes from. The Idafa lesson (both the Alif Baa one and the Al-Kitaab "Idafa, Continued" one) and the Case Endings lesson have several worked examples already.
- **Active vs. passive participle.** Given a participle, ask whether it's ism al-faa'il or ism al-maf'uul, or given a verb, ask for its participle. The Participles lesson has a small table of examples; it would need to be extended with more entries to make a real quiz bank (5-6 pairs is thin for a quiz, aim for at least 12-15).
- **Hollow and irregular verbs.** Given نام / سار / قال / كان, ask for the present-tense stem vowel, or ask which letter is the weak middle radical. Keep this one modest, there are only four verbs in the Hollow and Irregular Verbs lesson and no full conjugation paradigms for them (see the accuracy note in `reference/course-info.md` about not guessing at unconfirmed hollow-verb forms), so don't build questions that require forms beyond what's already in that lesson.

Follow the same pattern as the existing quiz categories: a data bank constant, a `genXQuestions(n)` function, an entry in `QUIZ_CATEGORIES`, a case in the `genQuestions()` switch. Keep English translations out of the pre-answer prompt for any of these (same reasoning as the existing Gender/Definiteness/Case/Sentence Type quizzes: English can give away a grammar answer that should come from reading the Arabic).

## 2. Crossword needs more content

The crossword is still the original 6-word grid from early in the project (KITAB, KALB, BINT, BAYT, DARS, BAB), all Alif Baa vocabulary, all transliterated answers. With 325 vocab words now on the site, this is thin. Two reasonable directions, pick one:

- Build a second, separate crossword using Al-Kitaab vocabulary, and let the Crossword tab have its own book selector (consistent with how Flashcards, Matching, and Homework already work). This fits the book-separation rule most cleanly.
- Or build one larger, harder crossword mixing both books, clearly labeled per-clue which book each word is from.

Whichever direction, a crossword grid has to be hand-verified: pick words with real, checkable letter intersections and confirm every crossing letter matches before wiring it up (the original grid was built and checked this way; don't skip that step just because it's tedious).

## 3. Alif Baa Unit 10 is only partially covered

The Case Endings lesson already pulls from Unit 10's "Formal Arabic" section, so the main grammar content of Unit 10 is on the site. What's missing is the rest of Unit 10: the handwriting-samples exercise (Drill 2, reading three handwriting samples and writing a similar paragraph about yourself) and the transition material introducing Al-Kitaab as a textbook. Neither of these obviously wants to be a "lesson" in the same sense as the others, they're activities, not grammar content, so think about whether they belong on the site at all before building anything here. Low priority.

## 4. Al-Kitaab Lesson 4 vocabulary should be double-checked against a clean source

`reference/course-info.md` explains this in detail: the specific scanned PDF used to pull Al-Kitaab vocabulary has its pages out of physical order right around the end of Lesson 3 and the start of Lesson 4. The vocabulary that made it onto the site was traced through the scrambled pages carefully and should be correct, but it was reconstructed under worse conditions than lessons 1, 2, 3, and 5 (which came from cleanly-ordered pages). If a better copy of Al-Kitaab Part One ever becomes available, Lesson 4's vocabulary list is the one entry worth re-verifying against it.

## 5. No audio or pronunciation on the site itself

Worth knowing this exists as a gap, not necessarily worth building: earlier in this project, a standalone MP3 (vocabulary read aloud, English then Arabic at two speeds) and a slideshow-style MP4 video were generated for Alif Baa vocabulary using espeak-ng for text-to-speech, entirely separate from this website. None of that is integrated into the site itself, there's no "listen" button anywhere on Flashcards, Lessons, or Conjugations. If this ever becomes worth doing, know going in that espeak-ng produces a clearly robotic voice, fine for timing and pronunciation drilling, not something to advertise as natural-sounding audio.

## 6. Minor Homework tab polish

No current-date awareness: the tab just lists every week for whichever book is selected, with no visual marker for "this is where we are now" or "this is overdue." Given the course runs on a real calendar (Alif Baa weeks 1-5, Al-Kitaab weeks 5-16, final exam Dec 17), a simple "this week" highlight keyed off the browser's current date would be a nice, low-risk addition. Not required, just flagged as a natural next step now that the full schedule exists.

## Before shipping any of the above

Whatever you build, run through the same checks described in CLAUDE.md's testing workflow section: syntax-check the extracted script, click through the change in a headless browser and watch for `pageerror` events (not just console output), and confirm the em-dash count is still zero across the whole file. Every real bug caught in this project so far (the `mkEl` multi-element bug, the `<tr>`-outside-`<table>` bug, a mismatched-quote syntax error, a `unit` filter missing a `book` guard) was caught this way, not by reading the diff.
