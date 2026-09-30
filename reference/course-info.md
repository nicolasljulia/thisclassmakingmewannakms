# Course Info (reference)

## The course
Georgetown University, Arabic and Islamic Studies Department.
Intensive 1st Year Modern Standard Arabic, Arabic 1011-03, Fall 2026.
Instructor: Dr. Elham Alzoubi. Teaching Assistant: Halim Khoiri.
Class meets MTWR, in person, no virtual attendance option.

## Two textbooks, two halves of the course
- **Alif Baa: Introduction to Arabic Letters and Sounds**, 3rd edition (Brustad, Al-Batal, Al-Tonsi). Covers weeks 1-5 of the semester (Aug 26 through Sep 23), units 1 through 10. The site currently covers units 1-9 in full; unit 10 (definite endings deep dive) is not yet on the site.
- **Al-Kitaab fii Ta'allum al-'Arabiyya, Part One**, 2nd edition (same authors). Picks up in week 5 (Sep 24) and runs through week 16 (Dec 8), lessons 1 through 5, followed by the final exam on Thursday, December 17, 7:00-9:00 PM.

**This distinction matters for how the site is built.** Alif Baa and Al-Kitaab are two different books with two different numbering schemes (Alif Baa has "units," Al-Kitaab has "lessons," both numbered 1 upward, so "Unit 4" and "Lesson 4" are two completely different things from two different books). Every piece of site content, vocabulary, lessons, flashcards, conjugations, homework, is tagged with a `book` field (`'alifbaa'` or `'alkitaab'`) for exactly this reason. See CLAUDE.md for the specifics of how that separation is implemented and why it has to stay that way.

## Where grammar content came from

**From the Alif Baa textbook directly:** the alphabet and letter forms, vowels, sukuun, shadda, tanwiin, hamzat al-wasl vs. hamzat al-qat', alif madda, sun letters and moon letters, gender (taa marbuuta), roots and patterns, case endings (i'raab), covered in Unit 10's "Formal Arabic" section.

**From Dr. Alzoubi's supplementary Alif Baa handouts (not in the Alif Baa textbook itself):** question words, the full possessive/subject pronoun paradigm, object pronoun suffixes, full present-tense verb conjugation paradigms, idafa rules, nominal sentence structure.

**From the Al-Kitaab textbook and its own daily schedule:** all Al-Kitaab vocabulary (lessons 1-5), the nominal sentence's negation with laysa, the verbal sentence and its word-order/agreement quirks, idafa in more depth, sound and broken plurals, the ten verb forms (al-awzaan), hollow and irregular verbs (nama, saara, qaala, kaana), active and passive participles, the verbal noun (masdar), and sentence connectors (wa/aw/laakin/fa).

## A real problem in the Al-Kitaab textbook scan

The specific scanned copy of Al-Kitaab used to pull lesson vocabulary (a pdfcoffee.com copy) has its **pages out of physical order** in the range covering the end of Lesson 3 through the start of Lesson 4. Printed pages jump from 50 to 67 to 68 and then back to 51 before continuing normally. The content itself is all present, it's just shuffled. If anyone re-derives vocabulary or grammar from that PDF again, don't trust sequential page order in that range; search for the actual "المفردات" vocabulary header images instead. This is already worked around, Lesson 4's vocabulary on the site was pulled from the correct (if out-of-sequence) pages, but it's worth knowing about if the source file comes up again.

## Verb conjugation accuracy notes
The site's verb data (`CONJUGATIONS` in index.html, the single source of truth used by both the Conjugations tab and the Verb Conjugation quiz) intentionally limits itself to forms that are directly confirmable:
- All 12 Alif Baa verbs and all 12 Al-Kitaab verbs (from the class's own fill-in-the-blank worksheets) have full, verified 13-person paradigms. This includes araada and aHabba, which were briefly split into a separate, less-complete quiz-only data structure (`VERBS_FULL`/`VERBS_PARTIAL`, capped at 5 confirmed persons) during an earlier point in this project; that structure has since been removed and both verbs now use their full paradigms everywhere, matching `CONJUGATIONS`.
- Six of the 24 verbs are genuinely irregular within their own form's template (aHabba, araada, akala, qara'a, sakana, and the quadriliteral tarjama); see the "Notes on irregular forms" section in `conjugations.md` for what makes each one worth being careful about (hollow-verb vowel shortening, doubled-verb consonant unfolding, hamza placement, and so on) before extending any of them further.

## Vocabulary source
- Alif Baa: 225 entries, pulled from the "New Vocabulary" tables in Alif Baa units 1-9, cross-checked against the student's own class study guide and handout photos. Some masculine/feminine adjective pairs that the textbook lists on one row are split into two separate flashcard entries on the site, for finer-grained drilling, which is why the site's count is higher than a simple textbook line count would suggest.
- Al-Kitaab: 100 entries, pulled directly from the "المفردات" vocabulary tables at the start of each of the 5 lessons (see the page-order note above for lesson 4's caveat).

## Grading structure (for context, not used on the site)
- Attendance, participation, class exercises: 20%
- Written daily homework: 10%
- Exams/quizzes: 45% (4 term exams, highest 3 count; several quizzes, highest 7 count)
- Final exam: 25% (oral 5%, writing 5%, computerized 15%) for the Alif Baa portion; Al-Kitaab's own term exams, a midterm, and a final oral/writing/computerized exam follow the pattern described in the homework schedule.
