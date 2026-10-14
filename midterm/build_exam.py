# Generates midterm/Arabic011_Midterm_Practice_Exam.pdf and ..._Key.pdf (run: python3 midterm/build_exam.py, then copy the two PDFs from midterm/build/)
# -*- coding: utf-8 -*-
import html as H, subprocess, sys, os, fitz  # needs PyMuPDF and Google Chrome

SP = os.path.dirname(os.path.abspath(__file__)) + '/build/'
os.makedirs(SP, exist_ok=True)
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

B = '<span class="blank"></span>'
def blanks(s): return s.replace('@@@', '<span class="blank wide"></span>').replace('___', B)
def A(s): return '<span class="ar">%s</span>' % s

# Each section: dict(letter, title, points, intro(html), items=[(prompt_html, answer_html)], kind)
# kind: 'ar' (RTL item lines), 'en' (LTR item lines), 'raw' (prompt is full html block)
S = []

S.append(dict(letter='A', title='Letters and connections', pts=8, page=1, parts=[
  dict(intro='1. Write the six letters that never connect to the letter that follows them. (3 points)',
       lines=[('<div class="wl"></div>', 'ا &nbsp; د &nbsp; ذ &nbsp; ر &nbsp; ز &nbsp; و')]),
  dict(intro='2. Connect the letters to form words. (3 points)',
       lines=[('<div class="ar">ك + ت + ا + ب = ___</div>', 'كتاب'),
              ('<div class="ar">م + د + ر + س + ة = ___</div>', 'مدرسة'),
              ('<div class="ar">ص + د + ي + ق = ___</div>', 'صديق')]),
  dict(intro='3. Rewrite each word with all of its short vowels and shadda. (2 points)',
       lines=[('<div class="ar">شباك = ___</div>', 'شُبَّاك'),
              ('<div class="ar">بنت = ___</div>', 'بِنْت')]),
]))

S.append(dict(letter='B', title='Numbers', pts=7, page=1, parts=[
  dict(intro='1. Count from one to ten in Arabic. Spell out each number. (5 points)',
       lines=[('<div class="wl"></div><div class="wl"></div>', 'واحد، اثنان، ثلاثة، أربعة، خمسة، ستة، سبعة، ثمانية، تسعة، عشرة')]),
  dict(intro='2. Write each numeral as a word. (2 points)',
       lines=[('<div class="ar">1) ٣ &nbsp; ___</div>', 'ثلاثة'), ('<div class="ar">2) ٧ &nbsp; ___</div>', 'سبعة')]),
]))

S.append(dict(letter='C', title='Dictation', pts=6, page=1, parts=[
  dict(intro='Write each word in Arabic with correct spelling. (In class these are read aloud; for this practice version the words are given in transliteration.) (6 points)',
       lines=[('<div class="enl">1) bayt &nbsp;&nbsp; @@@ &nbsp;&nbsp;&nbsp; 2) jaamiʿa &nbsp;&nbsp; @@@</div>', 'بَيْت &nbsp;&nbsp;&nbsp; ، &nbsp;&nbsp;&nbsp; جامِعة'),
              ('<div class="enl">3) madiina &nbsp;&nbsp; @@@ &nbsp;&nbsp;&nbsp; 4) Taaliba &nbsp;&nbsp; @@@</div>', 'مَدينة &nbsp;&nbsp;&nbsp; ، &nbsp;&nbsp;&nbsp; طالِبة'),
              ('<div class="enl">5) usra &nbsp;&nbsp; @@@ &nbsp;&nbsp;&nbsp; 6) maktaba &nbsp;&nbsp; @@@</div>', 'أُسْرة &nbsp;&nbsp;&nbsp; ، &nbsp;&nbsp;&nbsp; مَكْتَبة')]),
]))

S.append(dict(letter='D', title='Greetings', pts=5, page=1, parts=[
  dict(intro='Write an appropriate response to each greeting. (5 points)',
       lines=[('<div class="ar">1) مرحباً &nbsp; ___</div>', 'مرحباً / أهلاً'),
              ('<div class="ar">2) صباح الخير &nbsp; ___</div>', 'صباح النور'),
              ('<div class="ar">3) مساء الخير &nbsp; ___</div>', 'مساء النور'),
              ('<div class="ar">4) السلام عليكم &nbsp; ___</div>', 'وعليكم السلام'),
              ('<div class="ar">5) أهلاً وسهلاً &nbsp; ___</div>', 'أهلاً بك / أهلاً بكَ')]),
]))

S.append(dict(letter='E', title='Conversation', pts=12, page=2, parts=[
  dict(intro='Fill in the blanks of this conversation between Sara and Khalid with appropriate words. (12 points)',
       lines=[('<div class="ar">سارة: &nbsp; ___ الخير.</div>', 'صباح'),
              ('<div class="ar">خالد: &nbsp; صباح ___.</div>', 'النور'),
              ('<div class="ar">سارة: &nbsp; كيف ___؟</div>', 'الحال'),
              ('<div class="ar">خالد: &nbsp; بخير، ___ لله. وأنتِ؟</div>', 'الحمد'),
              ('<div class="ar">سارة: &nbsp; بخير. أنا ___ سارة.</div>', 'اسمي'),
              ('<div class="ar">خالد: &nbsp; أهلاً وسهلاً. من ___ أنتِ؟</div>', 'أين'),
              ('<div class="ar">سارة: &nbsp; أنا ___ مصر، ___ مدينة القاهرة. وأنتَ؟</div>', 'من ، من'),
              ('<div class="ar">خالد: &nbsp; أنا ___ في ___ جورجتاون.</div>', 'طالب ، جامعة'),
              ('<div class="ar">سارة: &nbsp; وأين ___؟</div>', 'تسكن'),
              ('<div class="ar">خالد: &nbsp; ___ في بيت صغير قريب من الجامعة.</div>', 'أسكن')]),
]))

S.append(dict(letter='F', title='Interrogative particles', pts=7, page=2, parts=[
  dict(intro='Complete each of these mini-dialogues with the correct interrogative particle. (7 points)',
       lines=[('<div class="ar">1) ___ تسكن؟ &nbsp; - &nbsp; أسكن في واشنطن.</div>', 'أين'),
              ('<div class="ar">2) ___ هذا؟ &nbsp; - &nbsp; هذا قلم.</div>', 'ما'),
              ('<div class="ar">3) ___ هو؟ &nbsp; - &nbsp; هو خالد.</div>', 'مَن'),
              ('<div class="ar">4) ___ تأكلين؟ &nbsp; - &nbsp; آكل الدجاج.</div>', 'ماذا'),
              ('<div class="ar">5) ___ الحال؟ &nbsp; - &nbsp; بخير، الحمد لله.</div>', 'كيف'),
              ('<div class="ar">6) ___ أنتِ؟ &nbsp; - &nbsp; أنا من لبنان.</div>', 'من أين'),
              ('<div class="ar">7) ___ أخ عندك؟ &nbsp; - &nbsp; عندي ثلاثة إخوة.</div>', 'كم')]),
]))

S.append(dict(letter='G', title='The definite article', pts=6, page=2, parts=[
  dict(intro='Add the definite article (ال) to each noun. Then circle <b>S</b> if the ل is silent (sun letter) or <b>M</b> if the ل is pronounced (moon letter). (6 points)',
       lines=[('<div class="ar">1) شمس &nbsp;&nbsp; ___ &nbsp;&nbsp;&nbsp; <span class="en">S &nbsp; M</span></div>', 'الشمس (S)'),
              ('<div class="ar">2) قمر &nbsp;&nbsp; ___ &nbsp;&nbsp;&nbsp; <span class="en">S &nbsp; M</span></div>', 'القمر (M)'),
              ('<div class="ar">3) دجاج &nbsp;&nbsp; ___ &nbsp;&nbsp;&nbsp; <span class="en">S &nbsp; M</span></div>', 'الدجاج (S)'),
              ('<div class="ar">4) كتاب &nbsp;&nbsp; ___ &nbsp;&nbsp;&nbsp; <span class="en">S &nbsp; M</span></div>', 'الكتاب (M)'),
              ('<div class="ar">5) رجل &nbsp;&nbsp; ___ &nbsp;&nbsp;&nbsp; <span class="en">S &nbsp; M</span></div>', 'الرجل (S)'),
              ('<div class="ar">6) جامعة &nbsp;&nbsp; ___ &nbsp;&nbsp;&nbsp; <span class="en">S &nbsp; M</span></div>', 'الجامعة (M)')]),
]))

S.append(dict(letter='H', title='Gender and agreement', pts=6, page=3, parts=[
  dict(intro='Circle the adjective that agrees with the noun. (6 points)',
       lines=[('<div class="ar">1) هذه سيارة &nbsp; (جديد / جديدة)</div>', 'جديدة'),
              ('<div class="ar">2) أخي &nbsp; (طويل / طويلة)</div>', 'طويل'),
              ('<div class="ar">3) صديقتي &nbsp; (لطيف / لطيفة)</div>', 'لطيفة'),
              ('<div class="ar">4) هذا الكتاب &nbsp; (كبير / كبيرة)</div>', 'كبير'),
              ('<div class="ar">5) المدينة &nbsp; (جميل / جميلة)</div>', 'جميلة'),
              ('<div class="ar">6) الأستاذ &nbsp; (مشغول / مشغولة)</div>', 'مشغول')]),
]))

S.append(dict(letter='I', title='Nisba adjectives', pts=8, page=3, parts=[
  dict(intro='Form nisba adjectives from the nouns below. (8 points)',
       lines=[('<div class="ar">1) هذه القهوة من تركيا &nbsp; ___</div>', 'القهوة التركيّة'),
              ('<div class="ar">2) أحمد من مصر &nbsp; ___</div>', 'أحمد مصريّ'),
              ('<div class="ar">3) مها من لبنان &nbsp; ___</div>', 'مها لبنانيّة'),
              ('<div class="ar">4) هذا الطالب من العراق &nbsp; ___</div>', 'هذا الطالب عراقيّ'),
              ('<div class="ar">5) هذه الأستاذة من سوريا &nbsp; ___</div>', 'هذه الأستاذة سوريّة'),
              ('<div class="ar">6) خالد من السعودية &nbsp; ___</div>', 'خالد سعوديّ'),
              ('<div class="ar">7) هي من الأردن &nbsp; ___</div>', 'هي أردنيّة'),
              ('<div class="ar">8) والدي من المغرب &nbsp; ___</div>', 'والدي مغربيّ')]),
]))

S.append(dict(letter='J', title='Possessive pronouns', pts=6, page=3, parts=[
  dict(intro='Add the correct possessive pronoun to each noun to match the English in parentheses. (6 points)',
       lines=[('<div class="ar">1) كتاب + (my) &nbsp; ___</div>', 'كتابي'),
              ('<div class="ar">2) بيت + (his) &nbsp; ___</div>', 'بيته'),
              ('<div class="ar">3) جامعة + (her) &nbsp; ___</div>', 'جامعتها'),
              ('<div class="ar">4) سيارة + (our) &nbsp; ___</div>', 'سيارتنا'),
              ('<div class="ar">5) صديق + (your, m. sing.) &nbsp; ___</div>', 'صديقك'),
              ('<div class="ar">6) أستاذ + (their, m. pl.) &nbsp; ___</div>', 'أستاذهم')]),
]))

S.append(dict(letter='K', title='Case endings', pts=8, page=4, parts=[
  dict(intro='Add the suitable case endings to the following: (8 points)',
       lines=[('<div class="ar">1) الطالب يقرأ الكتاب في المكتبة</div>', 'الطالبُ يقرأُ الكتابَ في المكتبةِ'),
              ('<div class="ar">2) أنا أشرب القهوة في الصباح</div>', 'أنا أشربُ القهوةَ في الصباحِ'),
              ('<div class="ar">3) هذه سيارة جديدة</div>', 'هذه سيارةٌ جديدةٌ'),
              ('<div class="ar">4) الأستاذة تسكن في بيت كبير</div>', 'الأستاذةُ تسكنُ في بيتٍ كبيرٍ'),
              ('<div class="ar">5) كتاب الأستاذ جديد</div>', 'كتابُ الأستاذِ جديدٌ'),
              ('<div class="ar">6) في صفي طالبة جديدة</div>', 'في صفّي طالبةٌ جديدةٌ'),
              ('<div class="ar">7) أحب المدينة الجديدة</div>', 'أحبُّ المدينةَ الجديدةَ'),
              ('<div class="ar">8) يذهب الولد إلى الجامعة مع صديقه</div>', 'يذهبُ الولدُ إلى الجامعةِ مع صديقِه')]),
]))

S.append(dict(letter='L', title='Verb conjugation', pts=9, page=4, parts=[
  dict(intro='Fill in the following chart translating from English to Arabic. (9 points)',
       chart=[('I go', 'أنا أذهبُ'), ('You (sing. M.) live', 'أنتَ تسكنُ'), ('She studies', 'هي تدرسُ'),
              ('We eat', 'نحن نأكلُ'), ('They (plural M.) work', 'هم يعملونَ'), ('You (sing. F.) drink', 'أنتِ تشربينَ'),
              ('They (dual M.) watch', 'هما يشاهدانِ'), ('You (plural M.) write', 'أنتم تكتبونَ'), ('They (F.) go', 'هنَّ يذهبنَ')]),
]))

S.append(dict(letter='M', title='Nominal and verbal sentences', pts=15, page=5, parts=[
  dict(intro='Identify which sentences are <span class="ar">جملة اسمية</span> by placing a check next to it. Then, identify <span class="ar">المبتدأ والخبر</span> in the <span class="ar">جمل اسمية</span> above by underlining <span class="ar">المبتدأ</span> once and underlining <span class="ar">الخبر</span> twice. (15 points: 1 point for each sentence classified correctly, 5 points for the underlining)',
       lines=[('<div class="ar">1) سارة طالبة في جامعة جورجتاون</div>', 'جملة اسمية. المبتدأ: سارة. الخبر: طالبة في جامعة جورجتاون'),
              ('<div class="ar">2) يدرس خالد الأدب العربي</div>', 'ليست اسمية (جملة فعلية: تبدأ بفعل)'),
              ('<div class="ar">3) هذا الكتاب جديد</div>', 'جملة اسمية. المبتدأ: هذا الكتاب. الخبر: جديد'),
              ('<div class="ar">4) عندي أخت كبيرة</div>', 'جملة اسمية (خبر مقدّم). الخبر: عندي. المبتدأ: أخت كبيرة'),
              ('<div class="ar">5) تشرب مها القهوة كل صباح</div>', 'ليست اسمية (جملة فعلية)'),
              ('<div class="ar">6) أحمد يعمل في مكتب</div>', 'جملة اسمية. المبتدأ: أحمد. الخبر: يعمل في مكتب (جملة فعلية)'),
              ('<div class="ar">7) في المكتبة طالب جديد</div>', 'جملة اسمية (خبر مقدّم). الخبر: في المكتبة. المبتدأ: طالب جديد'),
              ('<div class="ar">8) هي من لبنان</div>', 'جملة اسمية. المبتدأ: هي. الخبر: من لبنان'),
              ('<div class="ar">9) أسكن في بيروت</div>', 'ليست اسمية (جملة فعلية)'),
              ('<div class="ar">10) والدة أحمد أستاذة</div>', 'جملة اسمية. المبتدأ: والدة أحمد (إضافة، تُحسب مبتدأً واحداً). الخبر: أستاذة')]),
]))

S.append(dict(letter='N', title='Idafa and noun-adjective phrases', pts=10, page=5, parts=[
  dict(intro='1. Write <b>I</b> next to each <span class="ar">إضافة</span> (idafa) and <b>A</b> next to each noun-adjective phrase. (6 points)',
       lines=[('<div class="ar">1) كتابُ الطالبِ &nbsp; ___</div>', 'I'),
              ('<div class="ar">2) الكتابُ الجديدُ &nbsp; ___</div>', 'A'),
              ('<div class="ar">3) بيتُ الأستاذةِ &nbsp; ___</div>', 'I'),
              ('<div class="ar">4) مدينةٌ كبيرةٌ &nbsp; ___</div>', 'A'),
              ('<div class="ar">5) جامعةُ جورجتاون &nbsp; ___</div>', 'I'),
              ('<div class="ar">6) الطالبةُ اللطيفةُ &nbsp; ___</div>', 'A')]),
  dict(intro='2. Write each phrase in Arabic. (4 points)',
       lines=[('<div class="enl">1) the teacher’s book &nbsp; @@@ &nbsp;&nbsp; 2) a big house &nbsp; @@@</div>', 'كتابُ الأستاذِ &nbsp;&nbsp;&nbsp; ، &nbsp;&nbsp;&nbsp; بيتٌ كبيرٌ'),
              ('<div class="enl">3) the new student (f.) &nbsp; @@@ &nbsp;&nbsp; 4) Ahmad’s car &nbsp; @@@</div>', 'الطالبةُ الجديدةُ &nbsp;&nbsp;&nbsp; ، &nbsp;&nbsp;&nbsp; سيارةُ أحمدَ')]),
]))

S.append(dict(letter='O', title='Translation', pts=5, page=6, parts=[
  dict(intro='Translate the following sentences. (5 points)',
       lines=[('<div class="enl">1- My friend is Egyptian (m.) &nbsp; -----------------------------------------------</div>', 'صديقي مصريّ'),
              ('<div class="enl">2- Her house is big &nbsp; -----------------------------------------------------</div>', 'بيتُها كبيرٌ'),
              ('<div class="enl">3- I live in a small house &nbsp; ---------------------------------------------</div>', 'أسكنُ في بيتٍ صغيرٍ'),
              ('<div class="enl">4- Our university is in Washington &nbsp; ----------------------------------</div>', 'جامعتُنا في واشنطن'),
              ('<div class="enl">5- The teacher’s book is new &nbsp; ----------------------------------------</div>', 'كتابُ الأستاذِ جديدٌ')]),
]))

S.append(dict(letter='P', title='Expressions', pts=5, page=6, parts=[
  dict(intro='For each of the following situations, please choose the Arabic expression that best fits the context and write its corresponding number in the space provided. Some expressions may be used more than once. (5 points)',
       raw='<div class="ar exprs">1. الله &nbsp;&nbsp;&nbsp; 2. إن شاء الله &nbsp;&nbsp;&nbsp; 3. بسم الله &nbsp;&nbsp;&nbsp; 4. الحمد لله &nbsp;&nbsp;&nbsp; 5. ما شاء الله &nbsp;&nbsp;&nbsp; 6. لا إله إلا الله</div>',
       lines=[('<div class="enl">1. You are about to eat dinner with your family. &nbsp; -----</div>', '3'),
              ('<div class="enl">2. A friend asks how you are, and you are well. &nbsp; -----</div>', '4'),
              ('<div class="enl">3. You see your friend’s beautiful new house. &nbsp; -----</div>', '5'),
              ('<div class="enl">4. Your teacher asks if you will study tonight, and you hope to. &nbsp; -----</div>', '2'),
              ('<div class="enl">5. Someone asks if you will travel to Egypt next summer, and you hope so. &nbsp; -----</div>', '2')]),
]))

S.append(dict(letter='Q', title='Connectors and verbal nouns', pts=6, page=6, parts=[
  dict(intro='1. Choose the correct connector from the box: <span class="ar">و &nbsp; أو &nbsp; لكن &nbsp; ف</span> (3 points)',
       lines=[('<div class="ar">1) أحب القهوة ___ لا أحب الشاي</div>', 'لكن'),
              ('<div class="ar">2) هل تريد شاياً ___ قهوة؟</div>', 'أو'),
              ('<div class="ar">3) أشرب الشاي ___ القهوة في الصباح</div>', 'و')]),
  dict(intro='2. Change the verb which is preceded by <span class="ar">أن</span> into a verbal noun. (3 points)',
       lines=[('<div class="ar">1) أحبُّ أن أقرأَ القصةَ &nbsp; &larr; &nbsp; ___</div>', 'أحبُّ قراءةَ القصةِ'),
              ('<div class="ar">2) أريدُ أن أدرسَ العربيةَ &nbsp; &larr; &nbsp; ___</div>', 'أريدُ دراسةَ العربيةِ'),
              ('<div class="ar">3) يحبُّ أن يشاهدَ الأخبارَ &nbsp; &larr; &nbsp; ___</div>', 'يحبُّ مشاهدةَ الأخبارِ')]),
]))

PASSAGE = ('اسمي كريم. أنا طالبٌ في جامعةِ جورجتاون في مدينةِ واشنطن. أدرسُ اللغةَ العربيةَ والأدبَ. '
           'أسكنُ في بيتٍ صغيرٍ قريبٍ من الجامعةِ مع صديقي جون. والدي دكتورٌ في الجامعةِ الأمريكيةِ في بيروت، '
           'ووالدتي أستاذةٌ في مدرسةٍ كبيرةٍ. عندي أختٌ صغيرةٌ اسمُها ليلى، وهي طالبةٌ. '
           'في الصباحِ أشربُ القهوةَ وأذهبُ إلى الجامعةِ. في المساءِ أشاهدُ الأخبارَ وأقرأُ كتاباً جديداً.')

S.append(dict(letter='R', title='Reading comprehension', pts=21, page=7, parts=[
  dict(intro='Read the following paragraph and answer the questions below.',
       raw='<div class="ar passage">%s</div>' % PASSAGE,
       lines=[]),
  dict(intro='1. Answer each question in a full written Arabic sentence. (10 points)',
       lines=[('<div class="ar q">1) أين يدرس كريم؟</div><div class="wl"></div>', 'يدرسُ كريم في جامعة جورجتاون.'),
              ('<div class="ar q">2) ماذا يدرس؟</div><div class="wl"></div>', 'يدرسُ اللغةَ العربيةَ والأدبَ.'),
              ('<div class="ar q">3) مع مَن يسكن؟</div><div class="wl"></div>', 'يسكنُ مع صديقه جون.'),
              ('<div class="ar q">4) ماذا يعمل والد كريم؟ أين؟</div><div class="wl"></div>', 'والدُه دكتورٌ في الجامعةِ الأمريكيةِ في بيروت.'),
              ('<div class="ar q">5) ماذا يشاهد كريم في المساء؟</div><div class="wl"></div>', 'يشاهدُ كريم الأخبارَ في المساء.')]),
  dict(intro='2. Identify the following. Write one example from the paragraph. (7 points)',
       lines=[('<div class="enl">Pronoun &nbsp; -----------------------------------------------------------------</div>', 'هي'),
              ('<div class="enl">Verb &nbsp; ---------------------------------------------------------------------</div>', 'أدرسُ / أسكنُ / أشربُ / أذهبُ / أشاهدُ / أقرأُ'),
              ('<div class="enl">Noun-adjective phrase &nbsp; ----------------------------------------------</div>', 'بيتٍ صغيرٍ / أختٌ صغيرةٌ / مدرسةٍ كبيرةٍ / كتاباً جديداً'),
              ('<div class="enl">Idafa &nbsp; ------------------------------------------------------------------</div>', 'جامعةِ جورجتاون / مدينةِ واشنطن'),
              ('<div class="enl">Preposition &nbsp; -----------------------------------------------------------</div>', 'في / من / إلى / مع'),
              ('<div class="enl">Possessive pronoun &nbsp; ---------------------------------------------------</div>', 'اسمي / صديقي / والدي / والدتي / اسمُها'),
              ('<div class="enl">Verbal sentence &nbsp; -------------------------------------------------------</div>', 'أدرسُ اللغةَ العربيةَ / أسكنُ في بيتٍ صغيرٍ / أذهبُ إلى الجامعةِ')]),
  dict(intro='3. Identify the root (<span class="ar">الجذر</span>) of the following words. (4 points)',
       lines=[('<div class="ar">يدرس &nbsp; ___ &nbsp;&nbsp;&nbsp;&nbsp; أسكن &nbsp; ___ &nbsp;&nbsp;&nbsp;&nbsp; صغير &nbsp; ___ &nbsp;&nbsp;&nbsp;&nbsp; طالب &nbsp; ___</div>', 'د ر س &nbsp; ، &nbsp; س ك ن &nbsp; ، &nbsp; ص غ ر &nbsp; ، &nbsp; ط ل ب')]),
]))


S.append(dict(letter='S', title='Writing', pts=10, page=8, parts=[
  dict(intro='Write a short paragraph in Arabic (five to six sentences) introducing yourself. Include your name, where you are from, where you live, what you study, and what you like to eat and drink. Use full sentences with correct agreement and case endings. (10 points: 2 points for content, 4 for grammar and agreement, 2 for vocabulary, 2 for spelling)',
       lines=[('<div class="wl"></div>', '') for _ in range(9)]),
]))

TOTAL = sum(s['pts'] for s in S)

CSS = """
@page { size: Letter; margin: 0.5in 0.65in; }
*{box-sizing:border-box}
body{font-family:'Times New Roman',Times,serif;font-size:11.5pt;line-height:1.28;color:#000;margin:0}
.page{break-after:page;page-break-after:always}
.page:last-child{break-after:auto;page-break-after:auto}
.hdr{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:10pt;font-size:12pt}
.hdr .name{direction:rtl;font-family:Arial,'Geeza Pro',sans-serif}
.sec{margin:0 0 9pt 0}
.sec h2{font-size:11.5pt;margin:0 0 3pt 0;font-weight:bold}
.part{margin:0 0 5pt 0}
.intro{margin:0 0 3pt 0}
.ar{direction:rtl;text-align:right;font-family:Arial,'Geeza Pro',sans-serif;font-size:14pt;line-height:1.5;unicode-bidi:plaintext}
span.ar{font-size:13pt;unicode-bidi:isolate;display:inline}
.enl{direction:ltr;text-align:left;margin:3pt 0}
.en{direction:ltr;unicode-bidi:isolate;font-family:'Times New Roman',serif;font-size:11pt}
.blank.wide{min-width:170px}
.blank{display:inline-block;min-width:105px;border-bottom:1px solid #000;height:0.9em;vertical-align:baseline}
.wl{border-bottom:1px solid #000;height:17pt;margin:2pt 0}
.passage{border:1px solid #000;padding:6pt 9pt;margin:3pt 0 5pt 0;line-height:1.8}
.q{margin-top:3pt}
.spaced .ar{margin:9pt 0}
.exprs{text-align:center;margin:3pt 0 5pt 0}
table.chart{border-collapse:collapse;width:100%;margin:3pt 0}
table.chart td{border:1px solid #000;padding:3pt 8pt;height:21pt;font-size:11.5pt}
table.chart td.a{direction:rtl}
.goodluck{text-align:center;margin-top:12pt}
.goodluck .ar{text-align:center;font-size:13pt}
.keynote{font-size:10pt;margin:2pt 0 6pt 0}
.ans{direction:rtl;text-align:right;font-family:Arial,'Geeza Pro',sans-serif;font-size:13pt;line-height:1.55;margin:1pt 0}
.ans .n{direction:ltr;unicode-bidi:isolate;font-family:'Times New Roman',serif;font-size:10.5pt;color:#444}
.ansrow{display:flex;gap:8pt;align-items:baseline;margin:1pt 0}
.ansrow .num{width:28pt;flex:none;font-size:10.5pt;direction:ltr;unicode-bidi:isolate;text-align:left}
.ansrow .val{flex:1;direction:rtl;text-align:left;font-family:Arial,'Geeza Pro',sans-serif;font-size:13pt}
.ansrow .val.en{direction:ltr;text-align:left;font-family:'Times New Roman',serif;font-size:11pt}
"""

def header(title):
    return ('<div class="hdr"><div>Arabic 011</div><div>%s</div><div class="name">الإسم: ------------------</div></div>' % title)

def render_exam():
    out = []
    pages = sorted(set(s['page'] for s in S))
    for p in pages:
        out.append('<div class="page">')
        out.append(header('Midterm Practice Exam'))
        if p == 1:
            out.append('<div style="margin:0 0 8pt 0;">Total: %d points.</div>' % TOTAL)
        for s in [x for x in S if x['page'] == p]:
            out.append('<div class="sec%s"><h2>%s. %s (%d points)</h2>' % (' spaced' if s['letter'] in ('K','M') else '', s['letter'], s['title'], s['pts']))
            for part in s['parts']:
                out.append('<div class="part">')
                if part.get('intro'): out.append('<div class="intro">%s</div>' % part['intro'])
                if part.get('raw'): out.append(part['raw'])
                if part.get('chart'):
                    out.append('<table class="chart">' + ''.join('<tr><td style="width:46%%">%s</td><td class="a"></td></tr>' % e for e, a in part['chart']) + '</table>')
                for prompt, ans in part.get('lines', []):
                    out.append(blanks(prompt))
                out.append('</div>')
            out.append('</div>')
        if p == pages[-1]:
            out.append('<div class="goodluck"><div class="ar">بالتوفيق إن شاء الله</div><div>Good Luck</div></div>')
        out.append('</div>')
    return '<!doctype html><html><head><meta charset="utf-8"><title>Arabic 011 Midterm Practice Exam</title><style>%s</style></head><body>%s</body></html>' % (CSS, ''.join(out))

def strip_blank(prompt):
    # prompt shown in the key with the blank left as dashes
    return blanks(prompt).replace('<div class="wl"></div>', '')

def render_key():
    import re
    out = []
    out.append('<div class="page">')
    out.append(header('Midterm Practice Exam: Answer Key'))
    out.append('<div class="keynote">Total: %d points. Where an item lists several options, any answer that is grammatical and fits the context earns credit. Short vowels and case endings are shown in full here; on the exam, give the endings the question asks for.</div>' % TOTAL)
    for s in S:
        out.append('<div class="sec"><h2>%s. %s (%d points)</h2>' % (s['letter'], s['title'], s['pts']))
        multi = len(s['parts']) > 1
        for part in s['parts']:
            m = re.match(r'\s*(\d)\.', part.get('intro', ''))
            pre = (m.group(1) + '.') if (m and multi) else ''
            if part.get('chart'):
                for i, (e, a) in enumerate(part['chart'], 1):
                    out.append('<div class="ansrow"><span class="num">%d)</span><span class="val en" style="flex:0 0 38%%">%s</span><span class="val">%s</span></div>' % (i, e, a))
                continue
            if s['letter'] == 'S':
                out.append('<div class="intro">Answers vary. Model answer (yours will differ):</div><div class="ans">اسمي ليلى. أنا من أمريكا، من مدينة نيويورك. أسكنُ في واشنطن في بيتٍ صغيرٍ قريبٍ من الجامعةِ. أنا طالبةٌ في جامعةِ جورجتاون وأدرسُ اللغةَ العربيةَ. أحبُّ القهوةَ مع الحليبِ في الصباحِ وآكلُ الدجاجَ في المساءِ.</div>')
                continue
            lines = part.get('lines', [])
            if len(lines) == 1 and s['letter'] in ('A', 'B') and 'wl' in lines[0][0]:
                out.append('<div class="ansrow"><span class="num">%s</span><span class="val">%s</span></div>' % (pre or '1.', lines[0][1]))
                continue
            for i, (prompt, ans) in enumerate(lines, 1):
                out.append('<div class="ansrow"><span class="num">%s%d)</span><span class="val">%s</span></div>' % (pre, i, ans))
        out.append('</div>')
    out.append('<div class="sec"><h2>Notes on open-ended items</h2><div class="intro">Section E and the reading questions in Section R can be answered in more than one correct way. A good reading answer is a complete sentence with correct agreement and sensible case endings. Section S is open-ended; use the point breakdown on the exam. In Section Q, some verbs have more than one verbal noun (for example <span class="ar">السكن / السكنى</span>); the one shown is the most common.</div></div>')
    out.append('</div>')
    return '<!doctype html><html><head><meta charset="utf-8"><title>Arabic 011 Midterm Practice Exam Key</title><style>%s</style></head><body>%s</body></html>' % (CSS, ''.join(out))

def to_pdf(html_text, name):
    hp = SP + name + '.html'; pp = SP + name + '.pdf'
    open(hp, 'w', encoding='utf-8').write(html_text)
    subprocess.run([CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer',
                    '--print-to-pdf=' + pp, 'file://' + hp], check=True, capture_output=True, timeout=120)
    d = fitz.open(pp)
    return pp, len(d)

if __name__ == '__main__':
    print('total points', TOTAL)
    p, n = to_pdf(render_exam(), 'exam')
    print('exam pages', n, p)
    p2, n2 = to_pdf(render_key(), 'key')
    print('key pages', n2, p2)
