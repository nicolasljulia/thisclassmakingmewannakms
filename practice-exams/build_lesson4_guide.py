# -*- coding: utf-8 -*-
# Generates practice-exams/Arabic011_Lesson4_Study_Guide.pdf from the lessons and data in index.html, so the PDF stays in sync with the site.
# Run: python3 practice-exams/build_lesson4_guide.py   (needs PyMuPDF and Google Chrome). Output is written to practice-exams/build/.
import re, json, html as H, subprocess, fitz
from build_study_guide import BUILD, CHROME, INDEX, CSS, vocab_html, review_html

LESSON_TITLES = ["The Verbal Sentence", "Present-Tense Verb Conjugation", "Verb Forms (al-Awzaan)", "Hamza and Alif Madda",
                 "Hollow and Irregular Verbs", "Kaana and Laysa: Full Paradigms"]

def extract():
    """Load index.html in headless Chrome and dump the data the guide needs as JSON."""
    src = open(INDEX, encoding='utf-8').read()
    inj = '''<script>(function(){
 const want=%s;
 const out={lessons:want.map(t=>{const l=LESSONS.find(x=>x.title===t);return {title:l.title,body:l.body}}),
  vocab:VOCAB.filter(v=>v.book==='alkitaab'&&v.unit===4),
  conj:CONJUGATIONS.map(v=>({root:v.root,english:v.english,form:v.form,huwa:v.forms[3],ana:v.forms[0]})),
  templates:VERB_FORM_TEMPLATES, review:REVIEW_SETS.lesson4};
 const pre=document.createElement('pre'); pre.id='DATA'; pre.textContent=JSON.stringify(out);
 document.body.innerHTML=''; document.body.appendChild(pre);})();</script></body>''' % json.dumps(LESSON_TITLES)
    i = src.rindex('</body>')
    tmp = BUILD + 'dump4.html'
    open(tmp, 'w', encoding='utf-8').write(src[:i] + inj + src[i + 7:])
    dom = subprocess.run([CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--virtual-time-budget=5000', '--dump-dom', 'file://' + tmp],
                         capture_output=True, timeout=120).stdout.decode('utf-8')
    m = re.search(r'<pre id="DATA">(.*?)</pre>', dom, re.S)
    return json.loads(H.unescape(m.group(1)))

SCOPE = ['Vocabulary from p. 52, with plurals', 'The verbal sentence', 'The present tense and negation with لا',
         'Verb forms (awzaan) of three-consonant verbs', 'Hamzat al-qaTʿ and hamzat al-waSl', 'Hollow verbs: نام، سار، قال، كان',
         'كانَ in the past, all persons']

RULES = [
    'The present tense: prefix by person (<span class="arabic">أ ت ي ن</span>) and suffix by number and gender. Negate it with <span class="arabic">لا</span> directly before the verb; the verb does not change.',
    'A verbal sentence starts with the verb. When the verb comes <b>before</b> its subject it is <b>singular</b> (agreeing only in gender), even if the subject is plural: <span class="arabic">يَدْرُسُ الطُّلّابُ</span>.',
    'When the subject comes <b>first</b> the sentence is nominal and the verb agrees fully: <span class="arabic">الطُّلّابُ يَدْرُسُونَ</span>.',
    'To change a nominal sentence into a verbal one: move the verb to the front, make it singular, and keep the gender of the subject.',
    'Hamzat al-waSl is not pronounced after a vowel: <span class="arabic">ال</span>, <span class="arabic">اسْم، ابْن، ابْنة، امْرأة، اثْنان</span>, and the past of Forms VII to X. Test: put <span class="arabic">و</span> before the word. Hamzat al-qaTʿ is always heard (<span class="arabic">أُخْت، أَنا، إِلَى</span>, Form IV).',
    'Hollow verbs: the middle weak letter is a long vowel in the present (<span class="arabic">يَنامُ، يَسيرُ، يَقولُ، يَكونُ</span>) and in the past before a vowel ending (<span class="arabic">نامَتْ، قالُوا</span>). It shortens before a consonant ending: <span class="arabic">نِمْتُ، سِرْتُ، قُلْتُ، كُنْتُ، كُنَّ</span>.',
    '<span class="arabic">كانَ</span> turns a nominal sentence into the past: subject nominative, predicate accusative: <span class="arabic">كانَ الطَّقْسُ بارِداً</span>.',
]

def conj_html(conj):
    order = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']
    for v in conj: v.setdefault('form', 'quad.')  # تَرْجَمَ has four root consonants, so no form number
    rows = sorted(conj, key=lambda v: (order.index(v['form']) if v['form'] in order else 99, v['english']))
    return '<table><tr><th>Meaning</th><th>Form</th><th class="ar">Past (huwa)</th><th class="ar">Present (ana)</th><th class="ar">Present (huwa)</th></tr>%s</table>' % ''.join(
        '<tr><td>%s</td><td>%s</td><td class="ar big-ar">%s</td><td class="ar big-ar">%s</td><td class="ar big-ar">%s</td></tr>' % (
            H.escape(v['english']), v['form'], v['root'], v['ana'], v['huwa']) for v in rows)

def build(data):
    L = {l['title']: l['body'].strip() for l in data['lessons']}
    def lesson(title, heading=None):
        return '<h2>%s</h2>%s' % (heading or title, L[title])
    parts = ['<h1>Arabic 011: Lesson 4 Study Guide</h1><div class="sub">Everything for the Thursday, Nov 5 quiz in one place.</div>',
             '<h3>Contents</h3><ul class="scope">%s</ul>' % ''.join('<li>%s</li>' % s for s in SCOPE),
             '<h2>The Rules at a Glance</h2><ul>%s</ul>' % ''.join('<li>%s</li>' % r for r in RULES),
             '<h2>Vocabulary</h2>' + vocab_html(data['vocab']),
             lesson('The Verbal Sentence'),
             lesson('Present-Tense Verb Conjugation'),
             '<h2>The Verbs and Their Forms</h2><p class="muted">Every verb in the course, with its form number (wazn).</p>' + conj_html(data['conj']),
             lesson('Verb Forms (al-Awzaan)'),
             lesson('Hamza and Alif Madda', 'Hamza: Qatʿ and Waṣl'),
             lesson('Hollow and Irregular Verbs'),
             '<h2>Kaana</h2>' + L['Kaana and Laysa: Full Paradigms'].split('<h3>لَيْسَ')[0],
             '<h2>Self-Check</h2><p class="muted">Cover the right column and answer, then check.</p>' + review_html(data['review'])]
    return '<!doctype html><html><head><meta charset="utf-8"><title>Lesson 4 Study Guide</title><style>%s</style></head><body>%s</body></html>' % (CSS, ''.join(parts))

if __name__ == '__main__':
    data = extract()
    hp = BUILD + 'guide4.html'; pp = BUILD + 'guide4.pdf'
    open(hp, 'w', encoding='utf-8').write(build(data))
    subprocess.run([CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer', '--print-to-pdf=' + pp, 'file://' + hp],
                   check=True, capture_output=True, timeout=120)
    print('pages', len(fitz.open(pp)), pp)
