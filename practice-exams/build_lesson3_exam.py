# -*- coding: utf-8 -*-
# Generates the Lesson 3 Exam practice exam (Thursday, Oct 29) and its answer key, in the same format as the other practice exams.
# Run: python3 practice-exams/build_lesson3_exam.py   (needs PyMuPDF and Google Chrome). PDFs are written to practice-exams/build/.
import build_practice as BP
from build_practice import sec, ar, en, wl, prepare, render_exam, render_key
from build_exam import to_pdf

def line(label, width=''):
    return '<div class="enl">%s &nbsp; ------------------------------------------------------------</div>' % label

E = []
# ------------------------------------------------------------------ page 1
E.append(sec('Word bank', 8, 1, [dict(
    intro='Fill in each blank with the best word from the word bank. Two words are not used. (8 points)',
    raw='<div class="ar" style="text-align:center;border:1px solid #444;padding:4pt 6pt;margin:4pt 0;word-spacing:6pt;">'
        'عائِلة &nbsp; أَقارِب &nbsp; أَعْرِف &nbsp; الصُّوَر &nbsp; الرَّسائِل &nbsp; ضابِط &nbsp; الجَيْش &nbsp; أَيْضاً &nbsp; الكُلِّيّة &nbsp; زَوْج</div>',
    lines=[('<div class="ar passage">اسمي يوسف وأنا من الأردن. أنا من @@@ (1) كبيرة وعندي @@@ (2) كثيرون في مصر. لا @@@ (3) كل أقاربي '
            'ولكن أعرفهم من @@@ (4) و@@@ (5) فقط. والدي @@@ (6) في @@@ (7) الأردني وأخي @@@ (8) ضابط.</div>',
            'عائِلة، أَقارِب، أَعْرِف، الصُّوَر، الرَّسائِل، ضابِط، الجَيْش، أَيْضاً')])]))
E.append(sec('Family relationships', 6, 1, [dict(
    intro='Nada’s parents are Hassan and Mona. Hassan’s parents are Ali and Sawsan, and his sister is Rima. Mona’s brother is Tarek. Nada’s siblings are Omar and Dina. '
          'Write each person’s relationship to Nada as an idafa, e.g. <span class="ar">والِدُ نادا</span>. (6 points)', cols=2,
    lines=[(ar(i, q + ' &nbsp; ___'), a) for i, (q, a) in enumerate([
        ('ريما', 'عَمّةُ نادا'), ('طارق', 'خالُ نادا'), ('علي', 'جَدُّ نادا'), ('سوسن', 'جَدّةُ نادا'), ('عمر', 'أَخُو نادا'), ('دينا', 'أُخْتُ نادا')], 1)])]))
E.append(sec('Pronouns and possessive endings', 8, 1, [dict(
    intro='Fill in each blank with the correct subject pronoun or possessive ending, adjusting the spelling where needed. (8 points)',
    lines=[('<div class="ar passage">اسم@@@ (1) ليلى و@@@ (2) أسكن في بيروت مع والد@@@ (3) ووالدة@@@ (4). بيت@@@ (5) كبير وجميل. '
            'لي أخ اسم@@@ (6) سامي، و@@@ (7) يدرس في الجامعة. وعندي عمّ في إربد، بيت@@@ (8) صغير.</div>',
            'اسْمِي، أَنا، والِدِي، والِدَتِي، بَيْتُنا، اسْمُهُ، هُوَ، بَيْتُهُ')])]))
# ------------------------------------------------------------------ page 2
E.append(sec('Idafa or noun-adjective?', 6, 2, [dict(
    intro='Write the grammatical term next to each phrase: <span class="ar">إضافة</span> or <span class="ar">اسم + صفة</span>. (6 points)', cols=2,
    lines=[(ar(i, q + ' &nbsp; ___'), a) for i, (q, a) in enumerate([
        ('غرفة أخي', 'إِضافة'), ('غرفة كبيرة', 'اِسْم + صِفة'), ('مكتب الأستاذ', 'إِضافة'), ('مكتب جديد', 'اِسْم + صِفة'),
        ('صورة العائلة', 'إِضافة'), ('صور جميلة', 'اِسْم + صِفة'), ('والدة زوجي', 'إِضافة'), ('الكلية الصغيرة', 'اِسْم + صِفة'),
        ('مدينة القاهرة', 'إِضافة'), ('المدينة القديمة', 'اِسْم + صِفة'), ('ابن عم والدي', 'إِضافة'), ('الأخت الكبيرة', 'اِسْم + صِفة')], 1)])]))
E.append(sec('Plurals and agreement', 10, 2, [dict(
    intro='Fill in each blank with the plural of the words in parentheses, making the adjective agree. (10 points)',
    lines=[(ar(i, q + ' &nbsp; @@@'), a) for i, (q, a) in enumerate([
        ('فاطمة ونورا وسارة (طالبة، سعودي)', 'طالِباتٌ سُعُودِيّاتٌ'),
        ('خالد وسامي وعمر (مهندس، سوري)', 'مُهَنْدِسُونَ سُورِيُّونَ'),
        ('في هذه المدينة (جامعة، كبير)', 'جامِعاتٌ كَبِيرةٌ'),
        ('في مصر (مدينة، قديم)', 'مُدُنٌ قَدِيمةٌ'),
        ('في الصف (ولد، مشغول)', 'أَوْلادٌ مَشْغُولُونَ')], 1)])]))
E.append(sec('Nisba adjectives', 6, 2, [dict(
    intro='Write the nisba adjective for each country, with the right gender, number and definiteness. (6 points)',
    lines=[('<div class="ar passage">اسمي ريم وأسكن في مسقط. أنا @@@ (1) (عُمان) وأمي @@@ (2) (تونس) ووالدي @@@ (3) (المغرب). أدرس اللغة @@@ (4) (فرنسا). '
            'عندي أصدقاء @@@ (5) (اليمن) وصديقات @@@ (6) (السودان).</div>',
            'عُمانِيّة، تُونِسِيّة، مَغْرِبِيّ، الفَرَنْسِيّة، يَمَنِيُّونَ، سُودانِيّات')])]))
# ------------------------------------------------------------------ page 3
E.append(sec('Numbers', 10, 3, [dict(
    intro='Write each number in Arabic words. (10 points)', cols=2,
    lines=[(ar(i, q + ' &nbsp; @@@'), a) for i, (q, a) in enumerate([
        ('11', 'أَحَدَ عَشَرَ'), ('12', 'اِثْنا عَشَرَ'), ('13', 'ثَلاثةَ عَشَرَ'), ('15', 'خَمْسةَ عَشَرَ'), ('17', 'سَبْعةَ عَشَرَ'),
        ('19', 'تِسْعةَ عَشَرَ'), ('20', 'عِشْرُونَ'), ('40', 'أَرْبَعُونَ'), ('70', 'سَبْعُونَ'), ('100', 'مِئة')], 1)])]))
E.append(sec('Kaana and laysa', 18, 3, [
    dict(intro='1. Write the past tense of <span class="ar">كان</span> for each pronoun. (7 points)', cols=2,
         lines=[(ar(i, q + ' &nbsp; ___'), a) for i, (q, a) in enumerate([
             ('هو', 'كانَ'), ('هم', 'كانُوا'), ('هنّ', 'كُنَّ'), ('أنتِ', 'كُنْتِ'), ('أنتم', 'كُنْتُمْ'), ('أنا', 'كُنْتُ'), ('نحن', 'كُنّا')], 1)]),
    dict(intro='2. Negate each sentence with <span class="ar">ليس</span>, in the right form. (7 points)',
         lines=[(ar(i, q + ' &nbsp; @@@'), a) for i, (q, a) in enumerate([
             ('أنا مشغولة.', 'لَسْتُ مَشْغُولةً'), ('هي في البيت.', 'لَيْسَتْ فِي البَيْتِ'), ('هم طلاب.', 'لَيْسُوا طُلّاباً'),
             ('نحن موظفون.', 'لَسْنا مُوَظَّفِينَ'), ('أنتَ مترجم.', 'لَسْتَ مُتَرْجِماً'), ('هنّ في الصف.', 'لَسْنَ فِي الصَّفِّ'),
             ('أنتما أخوان.', 'لَسْتُما أَخَوَيْنِ')], 1)]),
    dict(intro='3. Rewrite each sentence in the past with <span class="ar">كان</span>. (4 points)',
         lines=[(ar(i, q + ' &nbsp; @@@'), a) for i, (q, a) in enumerate([
             ('الطقس جميل.', 'كانَ الطَّقْسُ جَمِيلاً'), ('أخي ضابط في الجيش.', 'كانَ أَخِي ضابِطاً فِي الجَيْشِ'),
             ('هي في المكتب.', 'كانَتْ فِي المَكْتَبِ'), ('البيوت قديمة.', 'كانَتِ البُيُوتُ قَدِيمةً')], 1)])]))
# ------------------------------------------------------------------ page 4
E.append(sec('Present-tense verbs', 16, 4, [
    dict(intro='1. Conjugate <span class="ar">يشعر بـ</span> (to feel) in the present tense for each pronoun. (6 points)', cols=2,
         lines=[(ar(i, q + ' &nbsp; ___'), a) for i, (q, a) in enumerate([
             ('أنا', 'أَشْعُرُ بِـ'), ('أنتِ', 'تَشْعُرِينَ بِـ'), ('هي', 'تَشْعُرُ بِـ'), ('نحن', 'نَشْعُرُ بِـ'), ('أنتم', 'تَشْعُرُونَ بِـ'), ('هم', 'يَشْعُرُونَ بِـ')], 1)]),
    dict(intro='2. Fill in each blank with the suitable form of the word in parentheses. (10 points)',
         lines=[(ar(i, q), a) for i, (q, a) in enumerate([
             ('البنات @@@ (يذهب) إلى @@@ (جامعة) كبيرة.', 'يَذْهَبْنَ، جامِعاتٍ'),
             ('يا أحمد وسامي، هل @@@ (يشاهد) الفيلم؟ نعم، نحن @@@ (يشاهد+هو).', 'تُشاهِدانِ، نُشاهِدُهُ'),
             ('@@@ (يعرف) أستاذ اللغة العربية @@@ (طالب+هو) كلهم.', 'يَعْرِفُ، طُلّابَهُ'),
             ('عندي @@@ (صورة) كثيرة لأخواتي، ولكن لا أعرف @@@ (اسم+هن) كلهن.', 'صُوَرٌ، أَسْماءَهُنَّ'),
             ('والدي @@@ (لبنان) ووالدتي @@@ (اليونان).', 'لُبْنانِيٌّ، يُونانِيّةٌ')], 1)])]))
E.append(sec('Case endings', 8, 4, [dict(
    intro='Add the suitable case endings. (8 points)',
    lines=[(ar(i, q), a) for i, (q, a) in enumerate([
        ('الضابط يسكن في بيت كبير.', 'الضّابِطُ يَسْكُنُ فِي بَيْتٍ كَبِيرٍ'), ('في الصف طالب وطالبة.', 'فِي الصَّفِّ طالِبٌ وَطالِبةٌ'),
        ('أقرأ رسائل الأقارب في المساء.', 'أَقْرَأُ رَسائِلَ الأَقارِبِ فِي المَساءِ'), ('أشاهد الأخبار مع والدتي.', 'أُشاهِدُ الأَخْبارَ مَعَ والِدَتِي'),
        ('هذه مدينة قديمة وجميلة.', 'هَذِهِ مَدِينةٌ قَدِيمةٌ وَجَمِيلةٌ'), ('كتاب الأستاذة جديد.', 'كِتابُ الأُسْتاذةِ جَدِيدٌ'),
        ('ابن خالتي يدرس العلوم السياسية في الكلية.', 'اِبْنُ خالَتِي يَدْرُسُ العُلُومَ السِّياسِيّةَ فِي الكُلِّيّةِ'),
        ('لا أعرف أسماء الطلاب الجدد.', 'لا أَعْرِفُ أَسْماءَ الطُّلّابِ الجُدُدِ')], 1)])]))
# ------------------------------------------------------------------ page 5
E.append(sec('Question words', 5, 2, [dict(
    intro='Write the suitable question word for each question. (5 points)',
    lines=[(ar(i, q), a) for i, (q, a) in enumerate([
        ('___ تسكن؟ ــ «في واشنطن»', 'أَيْنَ'), ('___ هذا؟ ــ «هذا أخي»', 'مَن'), ('___ تدرس؟ ــ «أدرس الأدب العربي»', 'ماذا'),
        ('___ أنتِ مشغولة؟ ــ «لا»', 'هَل'), ('___ تذهبين إلى الكلية؟ ــ «بالسيارة»', 'بِماذا (also: كَيْفَ)')], 1)])]))
E.append(sec('Subject and predicate', 4, 4, [dict(
    intro='Write the subject (<span class="ar">مبتدأ</span>) and the predicate (<span class="ar">خبر</span>) of each sentence. (4 points)',
    lines=[(ar(i, q), a) for i, (q, a) in enumerate([
        ('خالتي موظفة في مكتب القبول.', 'مُبْتَدَأ: خالَتِي / خَبَر: مُوَظَّفةٌ فِي مَكْتَبِ القَبُولِ'),
        ('في الغرفة طاولة جديدة.', 'خَبَر (مُقَدَّم): فِي الغُرْفةِ / مُبْتَدَأ: طاوِلةٌ جَدِيدةٌ'),
        ('اسم أخي سامي.', 'مُبْتَدَأ: اِسْمُ أَخِي / خَبَر: سامِي'),
        ('الأولاد في الصف.', 'مُبْتَدَأ: الأَوْلادُ / خَبَر: فِي الصَّفِّ')], 1)])]))
PASSAGE = ('اِسْمِي كَرِيم. أَنا طالِبٌ فِي جامِعةِ القاهِرةِ وَأَسْكُنُ فِي بَيْتٍ كَبِيرٍ مَعَ عائِلَتِي. والِدِي ضابِطٌ فِي الجَيْشِ وَوالِدَتِي مُتَرْجِمةٌ. '
           'عِنْدِي أَخٌ كَبِيرٌ اِسْمُهُ سامِي وَأُخْتٌ صَغِيرةٌ اِسْمُها هالة. كانَ جَدِّي مُهَنْدِساً وَكانَتْ جَدَّتِي مُوَظَّفةً فِي مَكْتَبةٍ. '
           'عِنْدِي أَقارِبُ كَثِيرُونَ فِي الأُرْدُنِّ: عَمِّي أَحْمَد وَزَوْجَتُهُ مارِيا وَأَوْلادُهُما الثَّلاثةُ. أُحِبُّ مُشاهَدةَ صُوَرِ عائِلَتِي كُلَّ مَساءٍ.')
E.append(sec('Reading comprehension', 15, 5, [
    dict(intro='Read the paragraph and answer the questions below.', raw='<div class="ar passage">%s</div>' % PASSAGE, lines=[]),
    dict(intro='1. Answer each question in a full written Arabic sentence. (10 points)', lines=[
        ('<div class="ar q">1) أَيْنَ يَسْكُنُ كَرِيم؟</div>' + wl(), 'يَسْكُنُ كَرِيم فِي بَيْتٍ كَبِيرٍ مَعَ عائِلَتِهِ.'),
        ('<div class="ar q">2) ماذا يَعْمَلُ والِدُ كَرِيم؟</div>' + wl(), 'والِدُهُ ضابِطٌ فِي الجَيْشِ.'),
        ('<div class="ar q">3) مَن سامِي؟</div>' + wl(), 'سامِي أَخُو كَرِيم الكَبِيرُ.'),
        ('<div class="ar q">4) ماذا كانَ جَدُّ كَرِيم؟</div>' + wl(), 'كانَ جَدُّهُ مُهَنْدِساً.'),
        ('<div class="ar q">5) أَيْنَ يَسْكُنُ أَقارِبُ كَرِيم؟</div>' + wl(), 'يَسْكُنُ أَقارِبُهُ فِي الأُرْدُنِّ.')]),
    dict(intro='2. Give the meaning of each word from the paragraph. (5 points)', cols=2, lines=[
        (ar(i, q + ' &nbsp; ___'), a) for i, (q, a) in enumerate([
            ('مُتَرْجِمة', 'translator (f.)'), ('الجَيْش', 'the army'), ('أَقارِب', 'relatives'), ('كانَتْ', 'was (f.)'), ('مُهَنْدِس', 'engineer')], 1)])]))
# ------------------------------------------------------------------ page 6
E.append(sec('Translation', 6, 6, [dict(
    intro='Translate the following sentences. (6 points)',
    lines=[('<div class="enl">%d- %s &nbsp; ------------------------------------------</div>' % (i, e), a) for i, (e, a) in enumerate([
        ('My uncle’s wife was a professor.', 'كانَتْ زَوْجةُ عَمِّي أُسْتاذةً'),
        ('I am not Egyptian; I am Lebanese.', 'لَسْتُ مِصْرِيّاً؛ أَنا لُبْنانِيّ (مِصْرِيّةً / لُبْنانِيّة if female)'),
        ('There are fifteen students in the class.', 'فِي الصَّفِّ خَمْسةَ عَشَرَ طالِباً')], 1)])]))
E.append(sec('Writing', 10, 6, [dict(
    intro='Write six to eight sentences in Arabic about your family. Include at least one idafa, one noun-adjective phrase, one plural, one number, one nisba adjective, '
          'and one sentence with <span class="ar">كان</span> or <span class="ar">ليس</span>. (10 points: 2 for content, 4 for grammar and agreement, 2 for vocabulary, 2 for spelling)',
    lines=[(wl(), '') for _ in range(8)],
    model='عائِلَتِي كَبِيرةٌ. والِدِي مُتَرْجِمٌ وَوالِدَتِي مُوَظَّفةٌ فِي مَكْتَبِ القَبُولِ. عِنْدِي أَخٌ وَأُخْتانِ. جَدِّي كانَ ضابِطاً فِي الجَيْشِ. '
          'عِنْدِي عِشْرُونَ قَرِيباً فِي لُبْنانَ، لِأَنَّ عائِلَةَ والِدِي لُبْنانِيّةٌ. لَسْتُ لُبْنانِيّاً، أَنا أَمْرِيكِيٌّ. أَعْرِفُ أَقارِبِي مِنَ الصُّوَرِ.')]))

E.sort(key=lambda s: s['page'])

NOTES = ('The reading and writing answers can be worded in more than one correct way; a good answer is a complete sentence with correct agreement and sensible case endings. '
         'In the kaana and laysa section, the predicate after both verbs is accusative. In the numbers section, 11 to 19 are written as two words; counted nouns after 11 to 99 are singular and accusative (<span class="ar">خَمْسةَ عَشَرَ طالِباً</span>). '
         'Where a non-human plural takes a feminine singular adjective, either that or a feminine plural adjective is read as correct at this level.')

if __name__ == '__main__':
    title = 'Lesson 3 Exam Practice'
    total = prepare(E)
    p, n = to_pdf(render_exam(E, title, total, (), '.wl{height:14.5pt}'), 'l3e_exam')
    p2, n2 = to_pdf(render_key(E, title, total, NOTES), 'l3e_key')
    print(title, '| points', total, '| exam pages', n, '| key pages', n2)
