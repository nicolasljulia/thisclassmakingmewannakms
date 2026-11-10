# -*- coding: utf-8 -*-
# Generates practice-exams/Arabic011_Lesson4_Exam_Study_Guide.pdf (Lesson 4 plus review of Lessons 1 to 3) from the lessons and data in index.html.
# Run: python3 practice-exams/build_lesson4_exam_guide.py   (needs PyMuPDF and Google Chrome). Output is written to practice-exams/build/.
import re, json, html as H, subprocess, fitz
from build_study_guide import BUILD, CHROME, INDEX, CSS, vocab_html, plural_html, world_html, review_html
from build_lesson4_guide import conj_html

LESSON_TITLES = ["The Verbal Sentence", "Present-Tense Verb Conjugation", "Verb Forms (al-Awzaan)", "Hamza and Alif Madda",
    "Hollow and Irregular Verbs", "Kaana and Laysa: Full Paradigms", "Verbs with a Fixed Preposition",
    "Family Terms", "Idafa: the Possessive (Construct) Phrase", "Idafa, Continued", "Subject Pronouns and Possessive Suffixes",
    "Plurals: Sound and Broken", "Adjectives and Agreement", "Nisba Adjectives", "The Nominal Sentence, Reviewed and Negated",
    "Case Endings (iʿraab)", "Question Words", "Numbers 11 to 100"]

def extract():
    """Load index.html in headless Chrome and dump the data the guide needs as JSON."""
    src = open(INDEX, encoding='utf-8').read()
    inj = '''<script>(function(){
 const want=%s;
 const out={lessons:want.map(t=>{const l=LESSONS.find(x=>x.title===t);return {title:l.title,body:l.body}}),
  vocab:[1,2,3,4].map(u=>VOCAB.filter(v=>v.book==='alkitaab'&&v.unit===u)),
  conj:CONJUGATIONS.map(v=>({root:v.root,english:v.english,form:v.form,huwa:v.forms[3],ana:v.forms[0]})),
  plurals:PLURAL_LISTS, world:REVIEW_SETS.arabworld, story:READING_PASSAGES[4],
  review3:REVIEW_SETS.lesson3, review4:REVIEW_SETS.lesson4, exam4:REVIEW_SETS.lesson4exam};
 const pre=document.createElement('pre'); pre.id='DATA'; pre.textContent=JSON.stringify(out);
 document.body.innerHTML=''; document.body.appendChild(pre);})();</script></body>''' % json.dumps(LESSON_TITLES)
    i = src.rindex('</body>')
    tmp = BUILD + 'dump5.html'
    open(tmp, 'w', encoding='utf-8').write(src[:i] + inj + src[i + 7:])
    dom = subprocess.run([CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--virtual-time-budget=5000', '--dump-dom', 'file://' + tmp],
                         capture_output=True, timeout=120).stdout.decode('utf-8')
    m = re.search(r'<pre id="DATA">(.*?)</pre>', dom, re.S)
    return json.loads(H.unescape(m.group(1)))

SCOPE = ['Lesson 4 vocabulary, with plurals', 'The present tense and negation with لا', 'The verbal sentence',
         'Verb forms (awzaan) and the form of every verb', 'Hamzat al-qaTʿ and hamzat al-waSl', 'Hollow verbs: نام، سار، قال، كان',
         'كانَ and لَيْسَ in all persons', 'Review of Lessons 1 to 3: vocabulary and plurals', 'The idafa and possessive endings',
         'Adjectives, nisba adjectives, the Arab world', 'The nominal sentence and case endings', 'Question words and numbers 11 to 100',
         'Maha’s Lesson 3 story', 'Self-check: Lesson 3 and Lesson 4 practice questions']

RULES4 = [
    'The present tense: prefix by person (<span class="arabic">أ ت ي ن</span>) and suffix by number and gender. Negate it with <span class="arabic">لا</span> directly before the verb; the verb does not change.',
    'A verbal sentence starts with the verb. When the verb comes <b>before</b> its subject it is <b>singular</b> (agreeing only in gender), even if the subject is plural: <span class="arabic">يَدْرُسُ الطُّلّابُ</span>. When the subject comes <b>first</b> the sentence is nominal and the verb agrees fully: <span class="arabic">الطُّلّابُ يَدْرُسُونَ</span>.',
    'Nominal to verbal: move the verb to the front, make it singular, keep the gender of the subject. A sentence that starts with a noun is nominal even when its predicate is a verb.',
    'The ten verb forms (awzaan): I <span class="arabic">فَعَلَ</span>, II <span class="arabic">فَعَّلَ</span>, III <span class="arabic">فاعَلَ</span>, IV <span class="arabic">أَفْعَلَ</span>, V <span class="arabic">تَفَعَّلَ</span>, VI <span class="arabic">تَفاعَلَ</span>, VII <span class="arabic">اِنْفَعَلَ</span>, VIII <span class="arabic">اِفْتَعَلَ</span>, IX <span class="arabic">اِفْعَلَّ</span>, X <span class="arabic">اِسْتَفْعَلَ</span>. <span class="arabic">اِسْتَمَعَ</span> is Form VIII.',
    'Hamzat al-waSl is not pronounced after a vowel: <span class="arabic">ال</span>, <span class="arabic">اسْم، ابْن، ابْنة، امْرأة، اثْنان</span>, and the past of Forms VII to X. Test: put <span class="arabic">و</span> before the word. Hamzat al-qaTʿ is always heard (<span class="arabic">أُخْت، أَنا، إِلَى</span>, Form IV).',
    'Hollow verbs: the middle weak letter is a long vowel in the present (<span class="arabic">يَنامُ، يَسيرُ، يَقولُ، يَكونُ</span>) and in the past before a vowel ending (<span class="arabic">نامَتْ، قالُوا</span>). It shortens before a consonant ending: <span class="arabic">نِمْتُ، سِرْتُ، قُلْتُ، كُنْتُ، كُنَّ</span>.',
    '<span class="arabic">كانَ</span> and <span class="arabic">لَيْسَ</span>: subject nominative, predicate accusative (<span class="arabic">كانَ الطَّقْسُ بارِداً</span>, <span class="arabic">لَسْتُ طالِباً</span>). A prepositional predicate stays as it is. <span class="arabic">لَيْسَ</span> negates nominal sentences; <span class="arabic">لا</span> negates present-tense verbs.',
]
RULES_REVIEW = [
    'The idafa: no <span class="arabic">ال</span> and no tanween on the first word; the second word is genitive; the ة of the first word is read <b>t</b>. Add a possessive ending to the <b>last</b> word only, and drop <span class="arabic">ال</span> from that word.',
    'Possessive endings: <span class="arabic">ـِي، ـكَ، ـكِ، ـهُ، ـها، ـنا، ـكُمْ، ـهُمْ</span>. A final ة becomes <span class="arabic">ت</span> before an ending: <span class="arabic">صَدِيقَتِي</span>.',
    'Agreement: plural people take plural adjectives; plural things take a feminine singular adjective. A noun and its adjective agree in gender, number, definiteness and case.',
    'Case endings: nominative <span class="arabic">ـُ ـٌ</span>, accusative <span class="arabic">ـَ ـً</span>, genitive <span class="arabic">ـِ ـٍ</span>. The sound feminine plural takes kasra for both accusative and genitive. After 11 to 99 the counted noun is singular and accusative.',
    'Nisba adjectives add <span class="arabic">ـِيّ</span> (m.) and <span class="arabic">ـِيّة</span> (f.): <span class="arabic">مِصْر ← مِصْرِيّ</span>.',
    'Numbers 11 to 19 are two words (the digit, then <span class="arabic">عَشَرَ</span>). The tens end in <span class="arabic">ـُونَ</span> in the nominative and <span class="arabic">ـِينَ</span> in the accusative and genitive.',
]

def build(data):
    L = {l['title']: l['body'].strip() for l in data['lessons']}
    def lesson(title, heading=None, cut=None):
        body = L[title]
        if cut: body = body.split(cut)[0]
        return '<h2>%s</h2>%s' % (heading or title, body)
    ul = lambda items: '<ul>%s</ul>' % ''.join('<li>%s</li>' % r for r in items)
    parts = ['<h1>Arabic 011: Lesson 4 Exam Study Guide</h1><div class="sub">Everything for the Wednesday, Nov 11 exam in one place: Lesson 4, with review of Lessons 1 to 3.</div>',
             '<h3>Contents</h3><ul class="scope">%s</ul>' % ''.join('<li>%s</li>' % s for s in SCOPE),
             '<h2>The Rules at a Glance</h2><h3>Lesson 4</h3>' + ul(RULES4) + '<h3>Review of Lessons 1 to 3</h3>' + ul(RULES_REVIEW),
             '<h1 style="break-before:page;font-size:17pt;margin-top:0">Part 1: Lesson 4</h1>',
             '<h2>Lesson 4 Vocabulary</h2>' + vocab_html(data['vocab'][3]),
             lesson('The Verbal Sentence'),
             lesson('Present-Tense Verb Conjugation'),
             '<h2>The Verbs and Their Forms</h2><p class="muted">Every verb in the course, with its form number (wazn).</p>' + conj_html(data['conj']),
             lesson('Verb Forms (al-Awzaan)'),
             lesson('Hamza and Alif Madda', 'Hamza: Qatʿ and WaSl'),
             lesson('Hollow and Irregular Verbs'),
             lesson('Kaana and Laysa: Full Paradigms', 'Kaana and Laysa'),
             lesson('Verbs with a Fixed Preposition'),
             '<h1 style="break-before:page;font-size:17pt;margin-top:0">Part 2: Review of Lessons 1 to 3</h1>']
    for i, n in enumerate(['Lesson 1', 'Lesson 2', 'Lesson 3'], 0):
        parts.append('<h2>%s Vocabulary</h2>' % n + vocab_html(data['vocab'][i]))
    parts.append('<h2>Plurals in the Vocabulary</h2>' + plural_html(data['plurals']))
    for t, h in [('Family Terms', None), ('Idafa: the Possessive (Construct) Phrase', 'The Idafa'), ('Idafa, Continued', 'The Idafa, Continued'),
                 ('Subject Pronouns and Possessive Suffixes', 'Pronouns and Possessive Endings'), ('Plurals: Sound and Broken', None),
                 ('Adjectives and Agreement', None), ('Nisba Adjectives', None)]:
        parts.append(lesson(t, h))
        if t == 'Nisba Adjectives': parts.append('<h3>Countries of the Arab world</h3>' + world_html(data['world']))
    parts += [lesson('The Nominal Sentence, Reviewed and Negated', 'The Nominal Sentence and Negation'), lesson('Case Endings (iʿraab)', 'Case Endings'),
              lesson('Question Words'), lesson('Numbers 11 to 100')]
    st = data['story']
    parts.append('<h2>Reading: Maha’s Lesson 3 Story</h2><div class="passage">%s</div><p class="muted">%s</p>' % (st['text'], st.get('translation', '')))
    parts.append('<h1 style="break-before:page;font-size:17pt;margin-top:0">Part 3: Self-Check</h1><p class="muted">Cover the right column and answer, then check.</p>')
    parts.append('<h2>Lesson 4 and Review Practice</h2>' + review_html(data['exam4']))
    parts.append('<h2>Lesson 4 Vocabulary and Grammar</h2>' + review_html(data['review4']))
    parts.append('<h2>Lesson 3 Review</h2>' + review_html(data['review3']))
    return '<!doctype html><html><head><meta charset="utf-8"><title>Lesson 4 Exam Study Guide</title><style>%s</style></head><body>%s</body></html>' % (CSS, ''.join(parts))

if __name__ == '__main__':
    data = extract()
    hp = BUILD + 'guide5.html'; pp = BUILD + 'guide5.pdf'
    open(hp, 'w', encoding='utf-8').write(build(data))
    subprocess.run([CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer', '--print-to-pdf=' + pp, 'file://' + hp],
                   check=True, capture_output=True, timeout=180)
    print('pages', len(fitz.open(pp)), pp)
