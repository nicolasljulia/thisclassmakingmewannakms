# -*- coding: utf-8 -*-
# Generates the Lesson 3 practice quiz and Unit 2 practice exam PDFs (and keys) in the same format as the midterm.
# Run: python3 practice-exams/build_practice.py   (needs PyMuPDF and Google Chrome). PDFs are written to practice-exams/build/.
import os, re, string
import build_exam as BE
from build_exam import CSS, header, blanks, to_pdf

def sec(title, pts, page, parts): return dict(title=title, pts=pts, page=page, parts=parts)
def ar(i, text, tail=''): return '<div class="ar">%s) %s%s</div>' % (i, text, tail)
def en(i, text): return '<div class="enl">%s) %s &nbsp; <span class="blank" style="min-width:80px"></span></div>' % (i, text)
def wl(): return '<div class="wl"></div>'

# ---------------------------------------------------------------- Lesson 3 quiz
L3 = []
L3.append(sec('Family words', 8, 1, [dict(
    intro='Write the Arabic for each family word. (8 points)', cols=2,
    lines=[(en(i, e), a) for i, (e, a) in enumerate([
        ('my father’s brother', 'عَمِّي'), ('my mother’s sister', 'خالَتِي'),
        ('my father’s sister’s son', 'اِبْن عَمَّتِي'), ('my mother’s brother', 'خالِي'),
        ('my paternal uncle’s wife', 'زَوْجة عَمِّي'), ('my grandfather', 'جَدِّي'),
        ('my relatives', 'أَقارِبِي'), ('my aunt’s (maternal) husband', 'زَوْج خالَتِي')], 1)])]))
L3.append(sec('Plurals', 10, 1, [dict(
    intro='Write the plural of each noun. (10 points)', cols=2,
    lines=[(ar(i, s + ' &nbsp; ___'), p) for i, (s, p) in enumerate([
        ('اِبْن', 'أَبْناء'), ('رِسالة', 'رَسائِل'), ('ضابِط', 'ضُبّاط'), ('قَرِيب', 'أَقارِب'), ('صُورة', 'صُوَر'),
        ('عَمّ', 'أَعْمام'), ('كُلِّيّة', 'كُلِّيّات'), ('زَوْج', 'أَزْواج'), ('عائِلة', 'عائِلات'), ('جَيْش', 'جُيُوش')], 1)])]))
L3.append(sec('The idafa', 6, 1, [dict(
    intro='Put the nouns together to make an idafa. Use <span class="ar">ال</span> only where it belongs. (6 points)',
    lines=[(ar(i, q + ' &nbsp; ___'), a) for i, (q, a) in enumerate([
        ('(رسالة / الأستاذ)', 'رِسالةُ الأُسْتاذِ'), ('(ضابط / الجيش)', 'ضابِطُ الجَيْشِ'), ('(كلية / الطب)', 'كُلِّيّةُ الطِّبِّ'),
        ('(أقارب / والدي)', 'أَقارِبُ والِدِي'), ('(زوجة / ضابط / الجيش)', 'زَوْجةُ ضابِطِ الجَيْشِ'),
        ('(بنت / عمة / والدتي)', 'بِنْتُ عَمّةِ والِدَتِي')], 1)])]))
L3.append(sec('Fix the mistake', 4, 1, [dict(
    intro='Each idafa breaks a rule. Rewrite it correctly. (4 points)',
    lines=[(ar(i, q + ' &nbsp; ___'), a) for i, (q, a) in enumerate([
        ('الرسالة الأستاذ', 'رِسالةُ الأُسْتاذِ (no ال on the first word)'),
        ('بيت العمي', 'بَيْتُ عَمِّي (no ال when the last word has a possessive ending)'),
        ('صورتي الأسرة', 'صُورةُ أُسْرَتِي (the possessive goes on the last word only)'),
        ('الكلية العلوم', 'كُلِّيّةُ العُلُومِ (no ال on the first word)')], 1)])]))
L3.append(sec('Whose?', 8, 2, [dict(
    intro='Turn each pair into one word with a possessive ending. (8 points)', cols=2,
    lines=[(ar(i, q + ' &nbsp; ___'), a) for i, (q, a) in enumerate([
        ('(رسالة / أنتَ)', 'رِسالَتُكَ'), ('(جيش / هي)', 'جَيْشُها'), ('(أقارب / أنتم)', 'أَقارِبُكُمْ'), ('(كلية / نحن)', 'كُلِّيَّتُنا'),
        ('(زوج / أنتِ)', 'زَوْجُكِ'), ('(عم / هم)', 'عَمُّهُمْ'), ('(صور / هو)', 'صُوَرُهُ'), ('(ابن / أنا)', 'اِبْنِي')], 1)])]))
L3.append(sec('The ة in an idafa', 4, 2, [dict(
    intro='Write how the <span class="ar">ة</span> of the first word is pronounced: <b>t</b> or <b>a</b>. (4 points)',
    lines=[(ar(i, q + ' &nbsp; ___'), a) for i, (q, a) in enumerate([
        ('صورة العائلة', 't'), ('كلية الطب', 't'), ('عائلة كبيرة', 'a (noun + adjective, not an idafa)'), ('رسالة الضابط', 't')], 1)])]))
L3.append(sec('Fields of study', 6, 2, [dict(
    intro='Write the Arabic for each word. (6 points)', cols=2,
    lines=[(en(i, e), a) for i, (e, a) in enumerate([
        ('history', 'التّارِيخ'), ('medicine', 'الطِّبّ'), ('law', 'الحُقُوق'), ('engineering', 'الهَنْدَسة'),
        ('psychology', 'عِلْم النَّفْس'), ('grandmother', 'جَدّة')], 1)])]))
L3_PASSAGE = ('عائِلةُ والِدَتِي كَبِيرةٌ. أَعْرِفُ أَقارِبِي مِنَ الصُّوَرِ وَالرَّسائِلِ. هَذا خالِي سامِي وَأُسْرَتُهُ، وَخالِي سامِي ضابِطٌ فِي الجَيْشِ. '
              'وَهَذِهِ خالَتِي مُنَى وَزَوْجُها وَاِبْنُها وَبَناتُها. وَابْنُ خالِي طالِبٌ فِي كُلِّيّةِ الطِّبِّ بِجامِعةِ القاهِرةِ.')
L3.append(sec('Reading comprehension', 11, 3, [
    dict(intro='Read the paragraph and answer the questions below.', raw='<div class="ar passage">%s</div>' % L3_PASSAGE, lines=[]),
    dict(intro='1. Answer each question in a full written Arabic sentence. (8 points)', lines=[
        ('<div class="ar q">1) كَيْفَ يَعْرِفُ الكاتِبُ أَقارِبَهُ؟</div>' + wl(), 'يَعْرِفُ أَقارِبَهُ مِنَ الصُّوَرِ وَالرَّسائِلِ.'),
        ('<div class="ar q">2) مَن سامِي؟ ماذا يَعْمَلُ؟</div>' + wl(), 'سامِي خالُ الكاتِبِ، وَهُوَ ضابِطٌ فِي الجَيْشِ.'),
        ('<div class="ar q">3) مَن فِي أُسْرةِ مُنَى؟</div>' + wl(), 'زَوْجُها وَابْنُها وَبَناتُها.'),
        ('<div class="ar q">4) أَيْنَ يَدْرُسُ ابْنُ الخالِ؟</div>' + wl(), 'يَدْرُسُ فِي كُلِّيّةِ الطِّبِّ بِجامِعةِ القاهِرةِ.')]),
    dict(intro='2. Write one example of each from the paragraph. (3 points)', lines=[
        ('<div class="enl">Idafa &nbsp; ------------------------------------------------------------------</div>', 'عائِلةُ والِدَتِي / كُلِّيّةِ الطِّبِّ / جامِعةِ القاهِرةِ / أُسْرةِ مُنَى'),
        ('<div class="enl">Possessive ending &nbsp; ------------------------------------------------------</div>', 'أَقارِبِي / أُسْرَتُهُ / زَوْجُها / اِبْنُها / بَناتُها / خالِي'),
        ('<div class="enl">Plural noun &nbsp; ---------------------------------------------------------------</div>', 'أَقارِب / الصُّوَر / الرَّسائِل / بَنات')])]))
L3.append(sec('Translation', 5, 3, [dict(
    intro='Translate the following sentences. (5 points)',
    lines=[('<div class="enl">%d- %s &nbsp; ------------------------------------------</div>' % (i, e), a) for i, (e, a) in enumerate([
        ('Her husband is an officer in the army.', 'زَوْجُها ضابِطٌ فِي الجَيْشِ'),
        ('This is my paternal aunt and her daughters.', 'هَذِهِ عَمَّتِي وَبَناتُها'),
        ('I know my relatives from the pictures.', 'أَعْرِفُ أَقارِبِي مِنَ الصُّوَرِ'),
        ('His family is big.', 'أُسْرَتُهُ كَبِيرةٌ'),
        ('My cousin (my uncle’s son) studies in the college of engineering.', 'اِبْنُ عَمِّي يَدْرُسُ فِي كُلِّيّةِ الهَنْدَسةِ')], 1)])]))

# ---------------------------------------------------------------- Unit 2 exam
U2 = []
U2.append(sec('Lesson 2 vocabulary', 10, 1, [dict(
    intro='Write the Arabic for each word. (10 points)', cols=2,
    lines=[(en(i, e), a) for i, (e, a) in enumerate([
        ('family', 'أُسْرة'), ('translator (m.)', 'مُتَرْجِم'), ('aunt (mother’s sister)', 'خالة'), ('always', 'دائِمًا'),
        ('really, truly', 'فِعْلًا'), ('language', 'لُغة'), ('evening', 'المَساء'), ('busy (f.)', 'مَشْغُولة'),
        ('employee (f.)', 'مُوَظَّفة'), ('admission(s)', 'القَبُول')], 1)])]))
U2.append(sec('Lesson 1 review', 5, 1, [dict(
    intro='Write the meaning of each word in English. (5 points)',
    lines=[(ar(i, q + ' &nbsp; ___________________'.replace('_' * 19, '@@@')), a) for i, (q, a) in enumerate([
        ('قِسْم', 'department'), ('مَبْرُوك', 'congratulations'), ('الثَّقافة', 'culture'), ('القَواعِد', 'grammar'), ('مِنْطَقة', 'area, region')], 1)])]))
U2.append(sec('Subject pronouns', 7, 1, [dict(
    intro='Fill in the correct subject pronoun. (7 points)',
    lines=[(ar(i, q), a) for i, (q, a) in enumerate([
        ('مَن أَنْتَ؟ ___ طالِب جَدِيد.', 'أَنا'), ('هَل ___ مَشْغُولة يا لَيْلَى؟', 'أَنْتِ'), ('مَن سامِي؟ ___ مُتَرْجِم.', 'هُوَ'),
        ('مِن أَيْن ___ يا شَباب؟ ___ مِن مِصْر.', 'أَنْتُمْ ، نَحْنُ'), ('أَحْمَد وَسارة؟ ___ طُلّاب.', 'هُمْ (a mixed group takes the masculine plural)'),
        ('مَن لَيْلَى؟ ___ مُوَظَّفة فِي بَنْك.', 'هِيَ')], 1)])]))
U2.append(sec('Plurals', 10, 2, [dict(
    intro='Write the plural of each noun. (10 points)', cols=2,
    lines=[(ar(i, s + ' &nbsp; ___'), p) for i, (s, p) in enumerate([
        ('رَجُل', 'رِجال'), ('طالِبة', 'طالِبات'), ('مَدِينة', 'مُدُن'), ('جامِعة', 'جامِعات'), ('أَخ', 'إِخْوة'),
        ('بَيْت', 'بُيُوت'), ('لُغة', 'لُغات'), ('مِصْرِيّ', 'مِصْرِيُّون / مِصْرِيِّين'), ('اِسْم', 'أَسْماء'), ('غُرْفة', 'غُرَف')], 1)])]))
U2.append(sec('Plural agreement', 6, 2, [dict(
    intro='Use the plural of the words in parentheses and make them agree. (6 points)',
    lines=[(ar(i, q + ' &nbsp; ___'), a) for i, (q, a) in enumerate([
        ('نَحْنُ (طالِبة، عِراقِيّ)', 'نَحْنُ طالِباتٌ عِراقِيّاتٌ'), ('هَذِهِ (مَدِينة، كَبِير)', 'هَذِهِ مُدُنٌ كَبِيرةٌ'),
        ('هُمْ (مُتَرْجِم، لُبْنانِيّ)', 'هُمْ مُتَرْجِمُونَ لُبْنانِيُّونَ'), ('هَذِهِ (جامِعة، أَمْرِيكِيّ)', 'هَذِهِ جامِعاتٌ أَمْرِيكِيّةٌ'),
        ('أَنْتُمْ (مُوَظَّف، مَشْغُول)', 'أَنْتُمْ مُوَظَّفُونَ مَشْغُولُونَ'), ('هَذِهِ (بَيْت، قَدِيم)', 'هَذِهِ بُيُوتٌ قَدِيمةٌ')], 1)])]))
U2.append(sec('Subject and predicate', 12, 2, [dict(
    intro='Find the <span class="ar">مُبْتَدَأ</span> and the <span class="ar">خَبَر</span>. Underline the subject once and the predicate twice, or write them. (12 points)',
    lines=[(ar(i, q), a) for i, (q, a) in enumerate([
        ('الطالبات مشغولات.', 'مُبْتَدَأ: الطّالِباتُ / خَبَر: مَشْغُولاتٌ'), ('أخي مترجم في بنك.', 'مُبْتَدَأ: أَخِي / خَبَر: مُتَرْجِمٌ فِي بَنْكٍ'),
        ('هذه المدينة قديمة.', 'مُبْتَدَأ: هَذِهِ المَدِينةُ / خَبَر: قَدِيمةٌ'), ('نحن في الجامعة.', 'مُبْتَدَأ: نَحْنُ / خَبَر: فِي الجامِعةِ'),
        ('أمي تعمل في مكتب القبول.', 'مُبْتَدَأ: أُمِّي / خَبَر: تَعْمَلُ فِي مَكْتَبِ القَبُولِ'),
        ('في المكتب موظفة جديدة.', 'خَبَر (مُقَدَّم): فِي المَكْتَبِ / مُبْتَدَأ: مُوَظَّفةٌ جَدِيدةٌ')], 1)])]))
U2.append(sec('Phrase or sentence?', 6, 3, [dict(
    intro='Write <b>P</b> for a phrase or <b>S</b> for a sentence, then translate. (6 points)',
    lines=[(ar(i, q + ' &nbsp; ___'), a) for i, (q, a) in enumerate([
        ('البيت القديم', 'P: the old house'), ('البيت قديم', 'S: The house is old.'), ('مدينة عربية', 'P: an Arab city'),
        ('المدينة عربية', 'S: The city is Arab.'), ('الطالبة الجديدة', 'P: the new student'), ('الأساتذة مشغولون', 'S: The professors are busy.')], 1)])]))
U2.append(sec('Connectors', 5, 3, [dict(
    intro='Choose the correct connector: <span class="ar">وَ &nbsp; أَو &nbsp; أَم &nbsp; لَكِن &nbsp; فَـ</span> (5 points)',
    lines=[(ar(i, q), a) for i, (q, a) in enumerate([
        ('هَل أَنْتَ عِراقِيّ ___ سُورِيّ؟', 'أَم (a question)'), ('أَدْرُس العَرَبِيّة ___ الفَرَنْسِيّة.', 'وَ'),
        ('أُرِيد قَهْوة ___ شايًا.', 'أَو (a statement)'), ('البَيْت جَمِيل ___ قَدِيم.', 'وَلَكِن'),
        ('أَنا مَشْغُول، ___ أَنا لا أَدْرُس الآن.', 'فَـ ← فَأَنا')], 1)])]))
U2.append(sec('Case endings', 6, 3, [dict(
    intro='Add the suitable case endings. (6 points)',
    lines=[(ar(i, q), a) for i, (q, a) in enumerate([
        ('المترجم يعمل في مكتب القبول.', 'المُتَرْجِمُ يَعْمَلُ فِي مَكْتَبِ القَبُولِ'), ('أنا أدرس اللغة العربية.', 'أَنا أَدْرُسُ اللُّغةَ العَرَبِيّةَ'),
        ('والدتي موظفة جديدة.', 'والِدَتِي مُوَظَّفةٌ جَدِيدةٌ'), ('هذا الكتاب في المكتبة.', 'هَذا الكِتابُ فِي المَكْتَبةِ'),
        ('تقرأ الطالبة الرسالة.', 'تَقْرَأُ الطّالِبةُ الرِّسالةَ'), ('أسكن في بيت كبير.', 'أَسْكُنُ فِي بَيْتٍ كَبِيرٍ')], 1)])]))
U2.append(sec('Translation', 6, 5, [dict(
    intro='Translate the following sentences. (6 points)',
    lines=[('<div class="enl">%d- %s &nbsp; ------------------------------------------</div>' % (i, e), a) for i, (e, a) in enumerate([
        ('I have an aunt named Layla.', 'لِي خالة اسْمُها لَيْلَى'), ('My father is always busy with work.', 'والِدِي مَشْغُولٌ دائِمًا بِالعَمَلِ'),
        ('I live in Washington, where I study Arabic.', 'أَسْكُنُ فِي واشِنْطُن، حَيْثُ أَدْرُسُ العَرَبِيّةَ'),
        ('She is a specialist in translation.', 'هِيَ مُتَخَصِّصةٌ فِي التَّرْجَمةِ'), ('I am really lonely.', 'أَنا فِعْلًا وَحِيدٌ (وَحِيدة if female)'),
        ('He is the only boy in the family.', 'هُوَ الوَلَدُ الوَحِيدُ فِي الأُسْرةِ')], 1)])]))
U2_PASSAGE = ('اِسْمِي سامِي. أَنا طالِبٌ فِي جامِعةِ القاهِرةِ وَأَسْكُنُ فِي القاهِرةِ. والِدِي مُوَظَّفٌ فِي مَكْتَبِ القَبُولِ وَهُوَ مَشْغُولٌ دائِمًا، '
              'وَوالِدَتِي مُتَرْجِمةٌ مُتَخَصِّصةٌ فِي اللُّغةِ الفَرَنْسِيّةِ. عِنْدِي أُخْتٌ صَغِيرةٌ اسْمُها سَلْمَى وَهِيَ طالِبةٌ. '
              'لِي خالةٌ اسْمُها سُعاد تَسْكُنُ فِي مَدِينةِ الإِسْكَنْدَرِيّةِ حَيْثُ تَعْمَلُ فِي بَنْكٍ. '
              'أَنا فِعْلًا مَشْغُولٌ فِي النَّهارِ، وَلَكِن فِي المَساءِ أَقْرَأُ قِصّةً جَدِيدةً.')
U2.append(sec('Reading comprehension', 20, 4, [
    dict(intro='Read the paragraph and answer the questions below.', raw='<div class="ar passage">%s</div>' % U2_PASSAGE, lines=[]),
    dict(intro='1. Answer each question in a full written Arabic sentence. (10 points)', lines=[
        ('<div class="ar q">1) أَيْنَ يَدْرُسُ سامِي؟</div>' + wl(), 'يَدْرُسُ سامِي فِي جامِعةِ القاهِرةِ.'),
        ('<div class="ar q">2) ماذا يَعْمَلُ والِدُ سامِي؟</div>' + wl(), 'والِدُهُ مُوَظَّفٌ فِي مَكْتَبِ القَبُولِ.'),
        ('<div class="ar q">3) فِي ماذا والِدةُ سامِي مُتَخَصِّصةٌ؟</div>' + wl(), 'هِيَ مُتَخَصِّصةٌ فِي اللُّغةِ الفَرَنْسِيّةِ.'),
        ('<div class="ar q">4) مَن سُعاد؟ أَيْنَ تَعْمَلُ؟</div>' + wl(), 'سُعاد خالةُ سامِي، وَهِيَ تَعْمَلُ فِي بَنْكٍ.'),
        ('<div class="ar q">5) ماذا يَقْرَأُ سامِي فِي المَساءِ؟</div>' + wl(), 'يَقْرَأُ قِصّةً جَدِيدةً.')]),
    dict(intro='2. Write one example of each from the paragraph. (7 points)', lines=[
        ('<div class="enl">Pronoun &nbsp; -----------------------------------------------------------------</div>', 'هُوَ / هِيَ / أَنا'),
        ('<div class="enl">Verb &nbsp; ---------------------------------------------------------------------</div>', 'أَسْكُنُ / تَسْكُنُ / تَعْمَلُ / أَقْرَأُ'),
        ('<div class="enl">Noun-adjective phrase &nbsp; ----------------------------------------------</div>', 'أُخْتٌ صَغِيرةٌ / قِصّةً جَدِيدةً'),
        ('<div class="enl">Idafa &nbsp; ------------------------------------------------------------------</div>', 'جامِعةِ القاهِرةِ / مَكْتَبِ القَبُولِ / مَدِينةِ الإِسْكَنْدَرِيّةِ'),
        ('<div class="enl">Preposition &nbsp; -----------------------------------------------------------</div>', 'فِي'),
        ('<div class="enl">Possessive pronoun &nbsp; ---------------------------------------------------</div>', 'والِدِي / والِدَتِي / اسْمُها'),
        ('<div class="enl">Nominal sentence (subject and predicate) &nbsp; -------------------------</div>', 'والِدِي مُوَظَّفٌ فِي مَكْتَبِ القَبُولِ (subject: والِدِي)')]),
    dict(intro='3. Identify the root (<span class="ar">الجذر</span>) of each word. (3 points)', lines=[
        ('<div class="ar">أَسْكُن &nbsp; ___ &nbsp;&nbsp;&nbsp;&nbsp; مَشْغُول &nbsp; ___ &nbsp;&nbsp;&nbsp;&nbsp; مُوَظَّف &nbsp; ___</div>', 'س ك ن &nbsp; ، &nbsp; ش غ ل &nbsp; ، &nbsp; و ظ ف')])]))
MAHA = ("والِدِي مُتَرْجِم مُتَخَصِّص فِي التَّرْجَمة مِن وَإِلَى اللُّغة العَرَبِيّة وَالإِنْجِلِيزِيّة وَالفَرَنْسِيّة، وَوالِدَتِي مُوَظَّفة فِي مَكْتَب القَبُول فِي جامِعة نِيويُورْك. "
        "والِدِي مَشْغُول دائِمًا، وَوالِدَتِي أَيْضًا مَشْغُولة بِالعَمَل فِي النَّهار وَبِشُغْل البَيْت فِي المَساء. لِي خالة اسْمُها نادِيَة تَسْكُن فِي مَدِينة لُوس أَنْجِلُوس فِي وِلاية كالِيفُورْنِيا، حَيْثُ تَعْمَل فِي بَنْك. "
        "أَنا البِنْت الوَحِيدة فِي الأُسْرة وَأَنا فِعْلًا وَحِيدة!")
U2.append(sec("Maha's story", 10, 5, [
    dict(intro='Read Maha’s story and answer the questions in Arabic. (10 points: 2 points each)', raw='<div class="ar passage">%s</div>' % MAHA, lines=[
        ('<div class="ar q">1) ماذا يَعْمَل والِد مَها؟</div>' + wl(), 'والِد مَها مُتَرْجِم مُتَخَصِّص فِي التَّرْجَمة.'),
        ('<div class="ar q">2) أَيْنَ تَعْمَل والِدة مَها؟</div>' + wl(), 'تَعْمَل فِي مَكْتَب القَبُول فِي جامِعة نِيويُورْك.'),
        ('<div class="ar q">3) مَن نادِيَة؟ أَيْنَ تَسْكُن؟</div>' + wl(), 'نادِيَة خالة مَها، تَسْكُن فِي لُوس أَنْجِلُوس فِي وِلاية كالِيفُورْنِيا.'),
        ('<div class="ar q">4) أَيْنَ تَعْمَل نادِيَة؟</div>' + wl(), 'تَعْمَل فِي بَنْك.'),
        ('<div class="ar q">5) مَن هِيَ البِنْت الوَحِيدة فِي الأُسْرة؟</div>' + wl(), 'مَها هِيَ البِنْت الوَحِيدة فِي الأُسْرة.')])]))
U2.append(sec('Writing', 10, 6, [dict(
    intro='Write a short paragraph in Arabic (five to six sentences) about yourself. Include your name, what you study, where you live, your family, and what you do in the evening. Use full sentences with correct agreement and case endings. (10 points: 2 for content, 4 for grammar and agreement, 2 for vocabulary, 2 for spelling)',
    lines=[(wl(), '') for _ in range(7)],
    model='اِسْمِي سارة. أَنا طالِبةٌ فِي جامِعةِ جورجتاون وَأَسْكُنُ فِي واشِنْطُن. والِدِي مُتَرْجِمٌ وَوالِدَتِي مُوَظَّفةٌ فِي بَنْكٍ. لِي أَخٌ صَغِيرٌ اسْمُهُ عُمَر وَخالةٌ اسْمُها مُنَى تَسْكُنُ فِي نِيويُورْك. أَنا فِعْلًا مَشْغُولةٌ فِي النَّهارِ، وَلَكِن فِي المَساءِ أَقْرَأُ قِصّةً.')]))

# ---------------------------------------------------------------- rendering
def prepare(S):
    for i, s in enumerate(S): s['letter'] = string.ascii_uppercase[i]
    return sum(s['pts'] for s in S)

def render_exam(S, title, total, spaced=(), extra_css=''):
    out = []
    pages = sorted(set(s['page'] for s in S))
    for p in pages:
        out.append('<div class="page">' + header(title))
        if p == 1: out.append('<div style="margin:0 0 8pt 0;">Total: %d points.</div>' % total)
        for s in [x for x in S if x['page'] == p]:
            out.append('<div class="sec%s"><h2>%s. %s (%d points)</h2>' % (' spaced' if s['title'] in spaced else '', s['letter'], s['title'], s['pts']))
            for part in s['parts']:
                out.append('<div class="part">')
                if part.get('intro'): out.append('<div class="intro">%s</div>' % part['intro'])
                if part.get('raw'): out.append(part['raw'])
                if part.get('cols'):
                    ls = part['lines']; half = (len(ls) + 1) // 2
                    order = [x for k in range(half) for x in (ls[k], ls[k + half] if k + half < len(ls) else None) if x]
                    out.append('<div class="cols2">' + ''.join(blanks(q) for q, a in order) + '</div>')
                else:
                    # keep the passage's questions below the passage
                    for q, a in part.get('lines', []): out.append(blanks(q))
                out.append('</div>')
            out.append('</div>')
        if p == pages[-1]:
            out.append('<div class="goodluck"><div class="ar">بالتوفيق إن شاء الله</div><div>Good Luck</div></div>')
        out.append('</div>')
    return '<!doctype html><html><head><meta charset="utf-8"><title>%s</title><style>%s</style></head><body>%s</body></html>' % (title, CSS + extra_css, ''.join(out))

def render_key(S, title, total, notes):
    out = ['<div class="page">' + header(title + ': Answer Key')]
    out.append('<div class="keynote">Total: %d points. Where an item lists several options, any answer that is grammatical and fits the context earns credit. Short vowels and case endings are shown in full here; on the exam, give the endings the question asks for.</div>' % total)
    for s in S:
        out.append('<div class="sec"><h2>%s. %s (%d points)</h2>' % (s['letter'], s['title'], s['pts']))
        multi = len(s['parts']) > 1
        for part in s['parts']:
            m = re.match(r'\s*(\d)\.', part.get('intro', ''))
            pre = (m.group(1) + '.') if (m and multi) else ''
            if part.get('model'):
                out.append('<div class="intro">Answers vary. Model answer (yours will differ):</div><div class="ans">%s</div>' % part['model'])
                continue
            for i, (q, a) in enumerate(part.get('lines', []), 1):
                mm = re.match(r'^(.*?)\s+\(([A-Za-z].*)\)$', a)
                if mm: a = '%s <span style="direction:ltr;unicode-bidi:isolate;font-family:\'Times New Roman\',serif;font-size:10.5pt;color:#444;">(%s)</span>' % (mm.group(1), mm.group(2))
                out.append('<div class="ansrow"><span class="num">%s%d)</span><span class="val">%s</span></div>' % (pre, i, a))
        out.append('</div>')
    out.append('<div class="sec"><h2>Notes</h2><div class="intro">%s</div></div></div>' % notes)
    return '<!doctype html><html><head><meta charset="utf-8"><title>%s Key</title><style>%s</style></head><body>%s</body></html>' % (title, CSS, ''.join(out))

JOBS = [
    ('l3', L3, 'Lesson 3 Practice Quiz',
     'The reading answers can be worded in more than one correct way; a good answer is a complete sentence with correct agreement and sensible case endings. In the "Fix the mistake" section the reason in parentheses is the rule that was broken.', ()),
    ('u2', U2, 'Unit 2 Practice Exam',
     'The reading and story answers can be worded in more than one correct way; a good answer is a complete sentence with correct agreement and sensible case endings. The writing section is open-ended; use the point breakdown on the exam. Either plural ending is acceptable for the men’s sound plural (<span class="ar">ـُون</span> or <span class="ar">ـِين</span>).', ('Case endings', 'Subject and predicate')),
]
if __name__ == '__main__':
    for key, S, title, notes, spaced in JOBS:
        total = prepare(S)
        p, n = to_pdf(render_exam(S, title, total, spaced, '.wl{height:14.5pt}' if key == 'u2' else ''), key + '_exam')
        p2, n2 = to_pdf(render_key(S, title, total, notes), key + '_key')
        print(title, '| points', total, '| exam pages', n, '| key pages', n2)
