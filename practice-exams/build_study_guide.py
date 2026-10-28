# -*- coding: utf-8 -*-
# Generates practice-exams/Arabic011_Lesson3_Study_Guide.pdf from the lessons and data in index.html, so the PDF stays in sync with the site.
# Run: python3 practice-exams/build_study_guide.py   (needs PyMuPDF and Google Chrome). Output is written to practice-exams/build/.
import os, re, json, html as H, subprocess, fitz

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = HERE + '/build/'
os.makedirs(BUILD, exist_ok=True)
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
INDEX = os.path.join(HERE, '..', 'index.html')

LESSON_TITLES = ["Family Terms", "Culture Notes", "Idafa: the Possessive (Construct) Phrase", "Idafa, Continued",
    "Subject Pronouns and Possessive Suffixes", "Plurals: Sound and Broken", "Adjectives and Agreement", "Nisba Adjectives",
    "The Nominal Sentence, Reviewed and Negated", "Case Endings (i\u02BFraab)", "Present-Tense Verb Conjugation", "Question Words",
    "Numbers 11 to 100", "Kaana and Laysa: Full Paradigms", "Verbs with a Fixed Preposition"]

def extract():
    """Load index.html in headless Chrome and dump the data the guide needs as JSON."""
    src = open(INDEX, encoding='utf-8').read()
    inj = '''<script>(function(){
 const want=%s;
 const out={lessons:want.map(t=>{const l=LESSONS.find(x=>x.title===t);return {title:l.title,body:l.body}}),
  vocab:VOCAB.filter(v=>v.book==='alkitaab'&&v.unit===3), plurals:PLURAL_LISTS, review:REVIEW_SETS.lesson3,
  world:REVIEW_SETS.arabworld, story:READING_PASSAGES[4]};
 const pre=document.createElement('pre'); pre.id='DATA'; pre.textContent=JSON.stringify(out);
 document.body.innerHTML=''; document.body.appendChild(pre);})();</script></body>''' % json.dumps(LESSON_TITLES)
    i = src.rindex('</body>')
    tmp = BUILD + 'dump.html'
    open(tmp, 'w', encoding='utf-8').write(src[:i] + inj + src[i + 7:])
    dom = subprocess.run([CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--virtual-time-budget=5000', '--dump-dom', 'file://' + tmp],
                         capture_output=True, timeout=120).stdout.decode('utf-8')
    m = re.search(r'<pre id="DATA">(.*?)</pre>', dom, re.S)
    return json.loads(H.unescape(m.group(1)))

CSS = """
@page { size: Letter; margin: 0.6in 0.7in; }
*{box-sizing:border-box}
body{font-family:'Times New Roman',Times,serif;font-size:10.5pt;line-height:1.35;color:#000;margin:0}
h1{font-size:20pt;margin:0 0 2pt 0}
.sub{font-size:11pt;color:#444;margin:0 0 10pt 0}
h2{font-size:14pt;margin:16pt 0 4pt 0;padding-bottom:2pt;border-bottom:1.5px solid #000;break-after:avoid}
h3{font-size:11.5pt;margin:9pt 0 2pt 0;break-after:avoid}
p{margin:3pt 0}
ul{margin:3pt 0 3pt 16pt;padding:0} li{margin:1.5pt 0}
.arabic,.ar{font-family:Arial,'Geeza Pro',sans-serif;direction:rtl;unicode-bidi:isolate}
.arabic{font-size:12.5pt}
td.ar,th.ar{text-align:right;font-size:12pt}
.big-ar{font-size:13.5pt}
table{border-collapse:collapse;width:100%;margin:4pt 0}
tr{break-inside:avoid}
th,td{border:1px solid #888;padding:2.5pt 6pt;text-align:left;vertical-align:middle}
th{background:#eee}
.muted{color:#444}
.tr-toggle{color:#444;font-style:italic}
.scope{columns:2;column-gap:24pt;margin:0 0 4pt 16pt}
.vgrid{columns:2;column-gap:22pt}
.v{display:flex;justify-content:space-between;align-items:baseline;gap:8pt;border-bottom:1px solid #ccc;padding:2pt 0;break-inside:avoid}
.v .e{direction:ltr}.v .e i{color:#555;font-size:9.5pt}
.v .a{font-family:Arial,'Geeza Pro',sans-serif;direction:rtl;font-size:13pt;white-space:nowrap}
.passage{border:1px solid #000;padding:6pt 9pt;margin:4pt 0;line-height:1.9;direction:rtl;text-align:right;font-family:Arial,'Geeza Pro',sans-serif;font-size:13pt}
.qa td:first-child{width:46%}
.note{font-size:9.5pt;color:#444}
"""

def clean(body):
    # keep the lesson markup, drop nothing but strip stray template whitespace
    return body.strip()

def vocab_html(vocab):
    groups = [('noun', 'Nouns'), ('verb', 'Verbs'), ('adjective', 'Adjectives'), ('number', 'Numbers'), ('phrase', 'Phrases and particles')]
    seen = set(); out = []
    for key, label in groups:
        items = [v for v in vocab if v['type'] == key]
        if not items: continue
        seen.update(id(v) for v in items)
        out.append('<h3>%s</h3><div class="vgrid">%s</div>' % (label, ''.join(
            '<div class="v"><span class="e">%s <i>%s</i></span><span class="a">%s</span></div>' % (H.escape(v['en']), H.escape(v['tr']), v['ar']) for v in items)))
    rest = [v for v in vocab if id(v) not in seen]
    if rest:
        out.append('<h3>Other</h3><div class="vgrid">%s</div>' % ''.join(
            '<div class="v"><span class="e">%s <i>%s</i></span><span class="a">%s</span></div>' % (H.escape(v['en']), H.escape(v['tr']), v['ar']) for v in rest))
    return ''.join(out)

def plural_html(groups):
    out = []
    for g in groups:
        out.append('<h3>%s</h3><table><tr><th class="ar">Singular</th><th class="ar">Plural</th><th>Meaning</th></tr>%s</table>' % (
            H.escape(g['group']), ''.join('<tr><td class="ar big-ar">%s</td><td class="ar big-ar">%s</td><td>%s</td></tr>' % (a, b, H.escape(c)) for a, b, c in g['items'])))
    return ''.join(out)

def review_html(sections):
    out = []
    for sec in sections:
        rows = ''
        for q, a in sec['items']:
            m = re.match(r'^(.*?)\s+\((.*)\)\s*$', a) if re.match(r'^[؀-ۿ]', a.strip()) else None
            ans = ('<span class="arabic big-ar">%s</span> <span class="note">(%s)</span>' % (m.group(1), m.group(2))) if m else \
                  ('<span class="arabic big-ar">%s</span>' % a if re.match(r'^[؀-ۿ]', a.strip()) else a)
            qh = '<span class="arabic big-ar">%s</span>' % q if sec['qlang'] == 'ar' else q
            isar = bool(re.match(r'^[\u0600-\u06FF]', a.strip()))
            cell = '<td class="ar">%s</td>' % ans if isar else '<td style="direction:ltr;unicode-bidi:isolate">%s</td>' % a
            rows += '<tr><td>%s</td>%s</tr>' % (qh, cell)
        out.append('<h3>%s</h3>%s<table class="qa">%s</table>' % (sec['title'], ('<p class="muted">%s</p>' % sec['instr']) if sec['instr'] else '', rows))
    return ''.join(out)

def world_html(sections):
    countries = sections[0]['items']; nisba = sections[1]['items']
    rows = ''.join('<tr><td>%s</td><td class="ar big-ar">%s</td><td class="ar big-ar">%s</td></tr>' % (e, a, n[1]) for (e, a), n in zip(countries, nisba))
    return '<table><tr><th>Country</th><th class="ar">Arabic</th><th class="ar">Nisba (m. / f.)</th></tr>%s</table>' % rows

SCOPE = ['Vocabulary: family, work, study, and the words below', 'Family terms and in-laws', 'The idafa and the ة in an idafa',
    'Possessive endings, all eight', 'Plurals: sound and broken, and agreement', 'Adjectives and agreement', 'Nisba adjectives and the Arab world',
    'The nominal sentence and negation with لَيْسَ', 'Case endings', 'Present-tense verbs, including يَشْعُرُ بِـ', 'Question words',
    'Numbers 11 to 100', 'كانَ in all 13 persons', 'Reading: Maha’s story']

def build(data):
    L = {l['title']: l['body'] for l in data['lessons']}
    def lesson(title, heading=None):
        return '<h2>%s</h2>%s' % (heading or title, clean(L[title]))
    parts = ['<h1>Arabic 011: Lesson 3 Study Guide</h1><div class="sub">Everything for the Lesson 3 exam in one place.</div>',
             '<h3>Contents</h3><ul class="scope">%s</ul>' % ''.join('<li><span class="arabic">%s</span></li>' % s if re.search(r'[؀-ۿ]', s) and False else '<li>%s</li>' % s for s in SCOPE)]
    parts.append('<h2>Vocabulary</h2>' + vocab_html(data['vocab']))
    parts.append(lesson('Family Terms'))
    parts.append(lesson('Culture Notes'))
    parts.append(lesson('Idafa: the Possessive (Construct) Phrase', 'The Idafa'))
    parts.append(lesson('Idafa, Continued', 'The Idafa, Continued'))
    parts.append(lesson('Subject Pronouns and Possessive Suffixes', 'Pronouns and Possessive Endings'))
    parts.append(lesson('Plurals: Sound and Broken'))
    parts.append('<h3>Plurals in the vocabulary</h3>' + plural_html(data['plurals']))
    parts.append(lesson('Adjectives and Agreement'))
    parts.append(lesson('Nisba Adjectives'))
    parts.append('<h3>Countries of the Arab world</h3>' + world_html(data['world']))
    parts.append(lesson('The Nominal Sentence, Reviewed and Negated', 'The Nominal Sentence and Negation'))
    parts.append(lesson('Case Endings (i\u02BFraab)', 'Case Endings'))
    parts.append(lesson('Present-Tense Verb Conjugation'))
    parts.append(lesson('Verbs with a Fixed Preposition'))
    parts.append(lesson('Question Words'))
    parts.append(lesson('Numbers 11 to 100'))
    parts.append(lesson('Kaana and Laysa: Full Paradigms', 'Kaana and Laysa'))
    st = data['story']
    parts.append('<h2>Reading: Maha’s Story</h2><div class="passage">%s</div><p class="muted">%s</p>' % (st['text'], st.get('translation', '')))
    parts.append('<h2>Self-Check</h2><p class="muted">Cover the right column and answer, then check.</p>' + review_html(data['review']))
    return '<!doctype html><html><head><meta charset="utf-8"><title>Lesson 3 Study Guide</title><style>%s</style></head><body>%s</body></html>' % (CSS, ''.join(parts))

if __name__ == '__main__':
    data = extract()
    hp = BUILD + 'guide.html'; pp = BUILD + 'guide.pdf'
    open(hp, 'w', encoding='utf-8').write(build(data))
    subprocess.run([CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer', '--print-to-pdf=' + pp, 'file://' + hp],
                   check=True, capture_output=True, timeout=120)
    print('pages', len(fitz.open(pp)), pp)
