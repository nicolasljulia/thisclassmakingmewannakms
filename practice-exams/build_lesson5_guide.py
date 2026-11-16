# -*- coding: utf-8 -*-
# Generates practice-exams/Arabic011_Lesson5_Study_Guide.pdf from the lessons and data in index.html, so the PDF stays in sync with the site.
# Run: python3 practice-exams/build_lesson5_guide.py   (needs PyMuPDF and Google Chrome). Output is written to practice-exams/build/.
import re, json, html as H, subprocess, fitz
from build_study_guide import BUILD, CHROME, INDEX, CSS, vocab_html, review_html

LESSON_TITLES = ["Weather, Seasons and Feelings (Lesson 5)", "The Absolute Object (al-Mafʿuul al-MuTlaq)", "The Accusative Noun (al-Ism al-ManSuub)",
                 "The Verbal Noun (al-Masdar)", "Case Endings (iʿraab)"]

def extract():
    src = open(INDEX, encoding='utf-8').read()
    inj = '''<script>(function(){
 const want=%s;
 const out={lessons:want.map(t=>{const l=LESSONS.find(x=>x.title===t);return {title:l.title,body:l.body}}),
  vocab:VOCAB.filter(v=>v.book==='alkitaab'&&v.unit===5),
  masdars:masdarCards().map(m=>({verb:m.verb,verbEn:m.verbEn,masdar:m.masdar,en:m.en,src:m.src,form:m.form})),
  review:REVIEW_SETS.lesson5};
 const pre=document.createElement('pre'); pre.id='DATA'; pre.textContent=JSON.stringify(out);
 document.body.innerHTML=''; document.body.appendChild(pre);})();</script></body>''' % json.dumps(LESSON_TITLES)
    i = src.rindex('</body>')
    tmp = BUILD + 'dump6.html'
    open(tmp, 'w', encoding='utf-8').write(src[:i] + inj + src[i + 7:])
    dom = subprocess.run([CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--virtual-time-budget=5000', '--dump-dom', 'file://' + tmp],
                         capture_output=True, timeout=120).stdout.decode('utf-8')
    return json.loads(H.unescape(re.search(r'<pre id="DATA">(.*?)</pre>', dom, re.S).group(1)))

SCOPE = ['Lesson 5 vocabulary: weather, seasons, feelings', 'Describing the weather, agreement of the adjective', 'بِسَبَبِ، بِالنِّسْبةِ لِـ، أَشْعُرُ بِـ، مِن أَصْلٍ، أَحْسَنُ',
         'The accusative noun and the tanween fatha', 'The absolute object (al-mafʿuul al-muTlaq)', 'The verbal noun (masdar)', 'Case endings']
RULES = [
    'Weather: <span class="arabic">الطَّقْس</span> and <span class="arabic">الجَوّ</span> are masculine (<span class="arabic">بارِدٌ، حارٌّ</span>); <span class="arabic">دَرَجةُ الحَرارةِ</span> and <span class="arabic">الرُّطُوبة</span> are feminine (<span class="arabic">عالِيةٌ</span>).',
    '<span class="arabic">بِسَبَبِ</span>, <span class="arabic">بِالنِّسْبةِ لِـ</span>, <span class="arabic">أَشْعُرُ بِـ</span> and <span class="arabic">مِن أَصْلٍ</span> are followed by the <b>genitive</b>; <span class="arabic">أَحْسَنُ</span> is the first term of an idafa: <span class="arabic">أَحْسَنُ فَصْلٍ</span>.',
    'An accusative noun is the direct object, the predicate of <span class="arabic">كانَ</span> or <span class="arabic">لَيْسَ</span>, an adverb (<span class="arabic">جِدّاً، كَثِيراً، أَحْياناً</span>), or an absolute object.',
    'Indefinite accusative: tanween fatha plus an alif (<span class="arabic">كَثِيراً</span>); no alif on a taa marbuuTa (<span class="arabic">مَدْرَسةً</span>); definite accusative: <span class="arabic">ـَ</span> (<span class="arabic">الرَّبِيعَ</span>); diptotes keep fatha without tanween (<span class="arabic">الأَسْماءَ</span>); the sound feminine plural takes kasra (<span class="arabic">الكَلِماتِ</span>).',
    'The absolute object is a masdar of the <b>same verb</b>, accusative and indefinite, with an accusative adjective that agrees with it: <span class="arabic">أُحِبُّ الرَّبِيعَ حُبّاً كَبِيراً</span>, <span class="arabic">دَرَسْتُ دِراسةً جَيِّدةً</span>.',
    'Form I verbal nouns are learned verb by verb; derived forms are regular: Form II <span class="arabic">تَفْعِيل</span>, Form IV <span class="arabic">إِفْعال</span>, Form V <span class="arabic">تَفَعُّل</span>, Form VIII <span class="arabic">اِفْتِعال</span>.',
]
def masdar_table(ms):
    return '<table><tr><th>Verb</th><th class="ar">Verb</th><th class="ar">Verbal noun</th><th>Meaning</th></tr>%s</table><p class="note">Rows marked * are standard forms added for the other course verbs; the others appear in the lesson or the vocabulary.</p>' % ''.join(
        '<tr><td>%s</td><td class="ar big-ar">%s</td><td class="ar big-ar">%s%s</td><td>%s</td></tr>' % (H.escape(m['verbEn']), m['verb'], m['masdar'], ' *' if m['src'] == 's' else '', H.escape(m['en'])) for m in ms)
def build(d):
    L = {l['title']: l['body'].strip() for l in d['lessons']}
    ul = '<ul>%s</ul>' % ''.join('<li>%s</li>' % r for r in RULES)
    parts = ['<h1>Arabic 011: Lesson 5 Study Guide</h1><div class="sub">Everything for the Tuesday, Nov 17 quiz in one place.</div>',
             '<h3>Contents</h3><ul class="scope">%s</ul>' % ''.join('<li>%s</li>' % s for s in SCOPE),
             '<h2>The Rules at a Glance</h2>' + ul,
             '<h2>Lesson 5 Vocabulary</h2>' + vocab_html(d['vocab'])]
    for t, h in [("Weather, Seasons and Feelings (Lesson 5)", 'Weather, Seasons and Feelings'), ("The Accusative Noun (al-Ism al-ManSuub)", 'The Accusative Noun'),
                 ("The Absolute Object (al-Mafʿuul al-MuTlaq)", 'The Absolute Object'), ("The Verbal Noun (al-Masdar)", 'The Verbal Noun')]:
        parts.append('<h2>%s</h2>%s' % (h, L[t]))
        if t.startswith('The Verbal Noun'): parts.append('<h3>Verbal nouns of the course verbs</h3>' + masdar_table(d['masdars']))
    parts.append('<h2>Case Endings</h2>' + L["Case Endings (iʿraab)"])
    parts.append('<h2>Self-Check</h2><p class="muted">Cover the right column and answer, then check.</p>' + review_html(d['review']))
    return '<!doctype html><html><head><meta charset="utf-8"><title>Lesson 5 Study Guide</title><style>%s</style></head><body>%s</body></html>' % (CSS, ''.join(parts))
if __name__ == '__main__':
    d = extract(); hp = BUILD + 'guide6.html'; pp = BUILD + 'guide6.pdf'
    open(hp, 'w', encoding='utf-8').write(build(d))
    subprocess.run([CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer', '--print-to-pdf=' + pp, 'file://' + hp], check=True, capture_output=True, timeout=180)
    print('pages', len(fitz.open(pp)), pp)
