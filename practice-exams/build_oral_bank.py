# -*- coding: utf-8 -*-
# Generates practice-exams/Arabic011_Oral_Exam_Question_Bank.pdf from ORAL_TOPICS in index.html, so the PDF stays in sync with the Oral Exam tab.
# Run: python3 practice-exams/build_oral_bank.py   (needs PyMuPDF and Google Chrome). Output is written to practice-exams/build/.
import re, json, html as H, subprocess, fitz
from build_study_guide import BUILD, CHROME, INDEX, CSS

def extract():
    src = open(INDEX, encoding='utf-8').read()
    inj = '''<script>(function(){
 const out={topics:ORAL_TOPICS, plan:ORAL_PLAN};
 const pre=document.createElement('pre'); pre.id='DATA'; pre.textContent=JSON.stringify(out);
 document.body.innerHTML=''; document.body.appendChild(pre);})();</script></body>'''
    i = src.rindex('</body>')
    tmp = BUILD + 'dump7.html'
    open(tmp, 'w', encoding='utf-8').write(src[:i] + inj + src[i + 7:])
    dom = subprocess.run([CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--virtual-time-budget=5000', '--dump-dom', 'file://' + tmp],
                         capture_output=True, timeout=120).stdout.decode('utf-8')
    return json.loads(H.unescape(re.search(r'<pre id="DATA">(.*?)</pre>', dom, re.S).group(1)))

def fmt(t):
    # {m|f} -> m / f ; [..] -> bold
    t = H.escape(t, quote=False)
    t = re.sub(r'\{([^{}|]*)\|([^{}]*)\}', lambda m: '%s / %s' % (m.group(1), m.group(2)), t)
    return re.sub(r'\[([^\]]*)\]', r'<b>[\1]</b>', t)

EXTRA = '''
.q{break-inside:avoid;border-bottom:1px solid #ccc;padding:5pt 0}
.q .n{color:#555;font-size:9pt}
.q .qa{font-family:Arial,'Geeza Pro',sans-serif;direction:rtl;text-align:right;font-size:14pt}
.q .a{font-family:Arial,'Geeza Pro',sans-serif;direction:rtl;text-align:right;font-size:13pt;color:#222}
.q .e{font-size:9.5pt;color:#444;margin-top:1pt}
.lines{height:20pt;border-bottom:1px solid #999;margin-top:6pt}
'''
def build(d):
    parts = ['<h1>Arabic 011: Oral Exam Question Bank</h1><div class="sub">Every question and model answer from the Oral Exam tab. Male and female forms are shown with a slash. Words in [brackets] are replaced with your own details. Cover the answer, say yours aloud, then check.</div>']
    parts.append('<h2>Contents</h2><ul class="scope">%s</ul>' % ''.join('<li>%s (%d)</li>' % (t['title'], len(t['qs'])) for t in d['topics']))
    for t in d['topics']:
        parts.append('<h2>%s</h2><p class="muted">%s</p>' % (H.escape(t['title']), H.escape(t['desc'])))
        for i, q in enumerate(t['qs'], 1):
            parts.append('<div class="q"><div class="n">%d</div><div class="qa">%s</div><div class="e">%s</div><div class="a" style="margin-top:4pt">%s</div><div class="e">%s</div></div>' % (
                i, fmt(q['q']), fmt(q['qe']), fmt(q['a']), fmt(q['ae'])))
    return '<!doctype html><html><head><meta charset="utf-8"><title>Oral Exam Question Bank</title><style>%s%s</style></head><body>%s</body></html>' % (CSS, EXTRA, ''.join(parts))
if __name__ == '__main__':
    d = extract(); hp = BUILD + 'oral.html'; pp = BUILD + 'oral.pdf'
    open(hp, 'w', encoding='utf-8').write(build(d))
    subprocess.run([CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer', '--print-to-pdf=' + pp, 'file://' + hp], check=True, capture_output=True, timeout=180)
    print('pages', len(fitz.open(pp)), pp)
