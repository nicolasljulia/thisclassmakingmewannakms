# -*- coding: utf-8 -*-
# Generates the Lesson 4 Exam practice exam (Wednesday, Nov 11) and its answer key, in the same format as the other practice exams.
# Run: python3 practice-exams/build_lesson4_exam.py   (needs PyMuPDF and Google Chrome). PDFs are written to practice-exams/build/.
import build_practice as BP
from build_practice import sec, ar, en, wl, prepare, render_exam, render_key
from build_exam import to_pdf

def tr(items, start=1):
    return [('<div class="enl">%d- %s &nbsp; ------------------------------------------</div>' % (i, e), a) for i, (e, a) in enumerate(items, start)]

def arw(items, extra=''):
    """Arabic prompt with a writing line under it."""
    return [(ar(i, q + '<div class="wl"></div>'), a) for i, (q, a) in enumerate(items, 1)]

def arb(items):
    """Arabic prompt with an inline blank."""
    return [(ar(i, q + ' &nbsp; ___'), a) for i, (q, a) in enumerate(items, 1)]

E = []
# ------------------------------------------------------------------ page 1
E.append(sec('Lesson 4 vocabulary', 10, 1, [dict(
    intro='Write the Arabic for each word. (10 points)', cols=2,
    lines=[(en(i, e), a) for i, (e, a) in enumerate([
        ('primary, elementary', 'اِبْتِدائِيّ'), ('classmate (m.)', 'زَمِيل'), ('friend (f.)', 'صَدِيقة'), ('first', 'أَوَّل'),
        ('fourth', 'رابِع'), ('all, every', 'كُلّ'), ('individual, person', 'فَرْد'), ('I was', 'كُنْتُ'),
        ('traveling', 'السَّفَر'), ('he was', 'كانَ')], 1)])]))
E.append(sec('Vocabulary from Lessons 1 to 3', 10, 1, [dict(
    intro='Write the Arabic for each word. (10 points)', cols=2,
    lines=[(en(i, e), a) for i, (e, a) in enumerate([
        ('family', 'أُسْرة'), ('aunt (mother’s sister)', 'خالة'), ('law', 'الحُقُوق'), ('medicine', 'الطِّبّ'),
        ('officer', 'ضابِط'), ('grandfather', 'جَدّ'), ('culture', 'الثَّقافة'), ('translator (m.)', 'مُتَرْجِم'),
        ('always', 'دائِمًا'), ('relatives', 'أَقارِب')], 1)])]))
E.append(sec('Plurals', 10, 1, [dict(
    intro='Write the plural of each noun. (10 points)', cols=2,
    lines=[(ar(i, s + ' &nbsp; ___'), p) for i, (s, p) in enumerate([
        ('مَدْرَسة', 'مَدارِس'), ('زَمِيل', 'زُمَلاء'), ('صَدِيقة', 'صَدِيقات'), ('فَرْد', 'أَفْراد'), ('قَرِيب', 'أَقارِب'),
        ('ضابِط', 'ضُبّاط'), ('رِسالة', 'رَسائِل'), ('عائِلة', 'عائِلات'), ('جَيْش', 'جُيُوش'), ('صُورة', 'صُوَر')], 1)])]))
E.append(sec('The present tense', 10, 1, [dict(
    intro='Write the present-tense form of the verb for the pronoun. (10 points)', cols=2,
    lines=arb([('(كَتَبَ / أَنْتِ)', 'تَكْتُبِينَ'), ('(شَرِبَ / نَحْنُ)', 'نَشْرَبُ'), ('(سَكَنَ / هِيَ)', 'تَسْكُنُ'), ('(حَفِظَ / أَنا)', 'أَحْفَظُ'),
               ('(ذَهَبَ / أَنْتُمْ)', 'تَذْهَبُونَ'), ('(قَرَأَ / هُوَ)', 'يَقْرَأُ'), ('(سافَرَ / هُمْ)', 'يُسافِرُونَ'), ('(تَذَكَّرَ / أَنْتَ)', 'تَتَذَكَّرُ'),
               ('(دَرَّسَ / نَحْنُ)', 'نُدَرِّسُ'), ('(اسْتَمَعَ / هُمْ)', 'يَسْتَمِعُونَ')]))]))
# ------------------------------------------------------------------ page 2
E.append(sec('Negation', 6, 2, [dict(
    intro='Make each sentence negative. (6 points)',
    lines=arw([('أَنا أَفْهَمُ الدَّرْسَ.', 'أَنا لا أَفْهَمُ الدَّرْسَ.'), ('هُوَ يَعْرِفُ زَمِيلِي.', 'هُوَ لا يَعْرِفُ زَمِيلِي.'),
               ('نَحْنُ نَسْكُنُ فِي بَيْتٍ كَبِيرٍ.', 'نَحْنُ لا نَسْكُنُ فِي بَيْتٍ كَبِيرٍ.'), ('تُسافِرُ أُمِّي إِلَى القاهِرةِ.', 'لا تُسافِرُ أُمِّي إِلَى القاهِرةِ.'),
               ('يَأْكُلُ الأَوْلادُ فِي المَدْرَسةِ.', 'لا يَأْكُلُ الأَوْلادُ فِي المَدْرَسةِ.'), ('أَنْتِ تَشْرَبِينَ الشّايَ.', 'أَنْتِ لا تَشْرَبِينَ الشّايَ.')]))]))
E.append(sec('Nominal and verbal sentences', 6, 2, [
    dict(intro='1. Rewrite each nominal sentence as a verbal sentence. (3 points)',
         lines=arw([('الطُّلّابُ يَقْرَأُونَ القِصّةَ.', 'يَقْرَأُ الطُّلّابُ القِصّةَ.'), ('البَناتُ يَعْمَلْنَ فِي البَنْكِ.', 'تَعْمَلُ البَناتُ فِي البَنْكِ.'),
                    ('الزَّمِيلةُ تَحْفَظُ الأَسْماءَ.', 'تَحْفَظُ الزَّمِيلةُ الأَسْماءَ.')])),
    dict(intro='2. Rewrite each verbal sentence with the subject first. (3 points)',
         lines=arw([('يَسْكُنُ الطُّلّابُ فِي القاهِرةِ.', 'الطُّلّابُ يَسْكُنُونَ فِي القاهِرةِ.'), ('تَدْرُسُ الطّالِباتُ العَرَبِيّةَ.', 'الطّالِباتُ يَدْرُسْنَ العَرَبِيّةَ.'),
                    ('يَذْهَبُ الأَصْدِقاءُ إِلَى المَدْرَسةِ.', 'الأَصْدِقاءُ يَذْهَبُونَ إِلَى المَدْرَسةِ.')]))]))
E.append(sec('Nominal or verbal?', 6, 2, [dict(
    intro='Write <b>N</b> for a nominal sentence or <b>V</b> for a verbal sentence. (6 points)', cols=2,
    lines=arb([('كانَ الطَّقْسُ بارِداً.', 'V'), ('أُخْتِي طالِبةٌ.', 'N'), ('تَدْرُسُ أُخْتِي العَرَبِيّةَ.', 'V'),
               ('هَذِهِ مَدْرَسةٌ كَبِيرةٌ.', 'N'), ('لا يَعْمَلُ والِدِي اليَوْمَ.', 'V'), ('والِدِي لا يَعْمَلُ اليَوْمَ.', 'N (it starts with the noun والِدِي)')]))]))
E.append(sec('Verb agreement', 6, 3, [dict(
    intro='Choose the verb that agrees with the subject. (6 points)',
    lines=[(ar(i, q), a) for i, (q, a) in enumerate([
        ('___ المُوَظَّفاتُ فِي البَنْكِ. &nbsp; (تَعْمَلُ / يَعْمَلْنَ)', 'تَعْمَلُ (verb first: singular)'),
        ('المُوَظَّفاتُ ___ فِي البَنْكِ. &nbsp; (تَعْمَلُ / يَعْمَلْنَ)', 'يَعْمَلْنَ (subject first: the verb agrees)'),
        ('___ الأَوْلادُ القِصّةَ. &nbsp; (يَقْرَأُ / يَقْرَأُونَ)', 'يَقْرَأُ'),
        ('الأَوْلادُ ___ القِصّةَ. &nbsp; (يَقْرَأُ / يَقْرَأُونَ)', 'يَقْرَأُونَ'),
        ('___ الزُّمَلاءُ فِي المَدْرَسةِ. &nbsp; (كانَ / كانُوا)', 'كانَ'),
        ('الزُّمَلاءُ ___ فِي المَدْرَسةِ. &nbsp; (كانَ / كانُوا)', 'كانُوا')], 1)])]))
# ------------------------------------------------------------------ page 3
E.append(sec('Verb forms', 10, 3, [
    dict(intro='1. Give the form number (<span class="ar">وَزْن</span>) of each past-tense verb. (6 points)', cols=2,
         lines=arb([('تَزَوَّجَ', 'V'), ('شاهَدَ', 'III'), ('أَحَبَّ', 'IV'), ('دَرَسَ', 'I'), ('دَرَّسَ', 'II'), ('اِسْتَمَعَ', 'VIII')])),
    dict(intro='2. Write the past and present templates (on the root <span class="ar">فعل</span>) of each form. (4 points)',
         lines=[('<div class="enl">Form II &nbsp; ------------------------------------------------------------------</div>', 'فَعَّلَ / يُفَعِّلُ'),
                ('<div class="enl">Form V &nbsp; ------------------------------------------------------------------</div>', 'تَفَعَّلَ / يَتَفَعَّلُ')])]))
E.append(sec('Hamza', 8, 3, [dict(
    intro='Write <b>Q</b> if the first hamza is hamzat al-qaTʿ, or <b>W</b> if it is hamzat al-waSl. (8 points)', cols=2,
    lines=arb([('اِسْم', 'W'), ('أُخْت', 'Q'), ('الجامِعة', 'W'), ('أَرْسَلَ', 'Q'), ('اِسْتَمَعَ', 'W'), ('أَنْتِ', 'Q'), ('اِبْنَة', 'W'), ('إِخْوة', 'Q')]))]))
E.append(sec('Hollow verbs', 12, 4, [dict(
    intro='Write the form asked for. (12 points)', cols=2,
    lines=arb([('(نامَ / أَنْتَ، past)', 'نِمْتَ'), ('(سارَ / هُمْ، past)', 'سارُوا'), ('(قالَ / نَحْنُ، past)', 'قُلْنا'),
               ('(كانَ / أَنا، past)', 'كُنْتُ'), ('(نامَ / هِيَ، past)', 'نامَتْ'), ('(قالَ / هُنَّ، past)', 'قُلْنَ'),
               ('(سارَ / أَنا، present)', 'أَسِيرُ'), ('(نامَ / نَحْنُ، present)', 'نَنامُ'), ('(قالَ / أَنْتَ، present)', 'تَقُولُ'),
               ('(كانَ / هُمْ، present)', 'يَكُونُونَ'), ('(سارَ / هُنَّ، present)', 'يَسِرْنَ'), ('(قالَ / هُوَ، present)', 'يَقُولُ')]))]))
# ------------------------------------------------------------------ page 4
E.append(sec('Kaana and laysa', 10, 4, [
    dict(intro='1. Say each sentence in the past with <span class="ar">كان</span>. Add the case ending of the predicate. (5 points)',
         lines=arw([('أَنا وَحِيدٌ.', 'كُنْتُ وَحِيداً.'), ('هُوَ ضابِطٌ.', 'كانَ ضابِطاً.'), ('الأَوْلادُ فِي المَدْرَسةِ.', 'كانَ الأَوْلادُ فِي المَدْرَسةِ.'),
                    ('أَنْتِ مُوَظَّفةٌ.', 'كُنْتِ مُوَظَّفةً.'), ('الطّالِبةُ مَشْغُولةٌ.', 'كانَتِ الطّالِبةُ مَشْغُولةً.')])),
    dict(intro='2. Make each sentence negative with <span class="ar">ليس</span>. (5 points)',
         lines=arw([('أَنا طالِبٌ.', 'لَسْتُ طالِباً.'), ('هِيَ مَشْغُولةٌ.', 'لَيْسَتْ مَشْغُولةً.'), ('نَحْنُ فِي الجامِعةِ.', 'لَسْنا فِي الجامِعةِ.'),
                    ('هُمْ مِصْرِيُّونَ.', 'لَيْسُوا مِصْرِيِّينَ.'), ('أَنْتُمْ عِراقِيُّونَ.', 'لَسْتُمْ عِراقِيِّينَ.')]))]))
E.append(sec('Whose?', 6, 5, [dict(
    intro='Turn each pair into one word with a possessive ending. (6 points)', cols=2,
    lines=arb([('(زَمِيلة / أَنْتِ)', 'زَمِيلَتُكِ'), ('(مَدْرَسة / نَحْنُ)', 'مَدْرَسَتُنا'), ('(أَصْدِقاء / هُوَ)', 'أَصْدِقاؤُهُ'),
               ('(صَدِيق / هُمْ)', 'صَدِيقُهُمْ'), ('(طُفُولة / أَنا)', 'طُفُولَتِي'), ('(زُمَلاء / أَنْتُمْ)', 'زُمَلاؤُكُمْ')]))]))
E.append(sec('The idafa', 6, 5, [
    dict(intro='1. Put the nouns together to make an idafa. (3 points)',
         lines=arb([('(كُلِّيّة / الطِّبّ)', 'كُلِّيّةُ الطِّبِّ'), ('(ضابِط / الجَيْش)', 'ضابِطُ الجَيْشِ'), ('(أَقارِب / زَمِيلِي)', 'أَقارِبُ زَمِيلِي')])),
    dict(intro='2. Each idafa breaks a rule. Rewrite it correctly. (3 points)',
         lines=arb([('الصَّدِيقة الأُسْتاذ', 'صَدِيقةُ الأُسْتاذِ (no ال on the first word)'),
                    ('مَدْرَسةُ الطّالِبِي', 'مَدْرَسةُ طالِبِي (no ال when the last word has a possessive ending)'),
                    ('زَمِيلَتِي المَدْرَسة', 'زَمِيلةُ مَدْرَسَتِي (the possessive goes on the last word only)')]))]))
E.append(sec('Case endings', 6, 5, [dict(
    intro='Add the suitable case endings. (6 points)',
    lines=arw([('المدرسة الابتدائية كبيرة.', 'المَدْرَسةُ الاِبْتِدائِيّةُ كَبِيرةٌ'), ('زميلي يحفظ الأسماء.', 'زَمِيلِي يَحْفَظُ الأَسْماءَ'),
               ('أسافر إلى القاهرة قبل الجامعة.', 'أُسافِرُ إِلَى القاهِرةِ قَبْلَ الجامِعةِ'), ('كانت صديقتي في المدرسة.', 'كانَتْ صَدِيقَتِي فِي المَدْرَسةِ'),
               ('لست طالبا جديدا.', 'لَسْتُ طالِباً جَدِيداً'), ('يدرس الأفراد في كلية كبيرة.', 'يَدْرُسُ الأَفْرادُ فِي كُلِّيّةٍ كَبِيرةٍ')]))]))
# ------------------------------------------------------------------ page 5
E.append(sec('Numbers and nisba adjectives', 8, 6, [
    dict(intro='1. Write each numeral as a word. (4 points)', cols=2,
         lines=arb([('١٥', 'خَمْسةَ عَشَرَ'), ('٢٠', 'عِشْرُونَ'), ('٤٠', 'أَرْبَعُونَ'), ('٩٠', 'تِسْعُونَ')])),
    dict(intro='2. Write the masculine nisba adjective for each place. (4 points)', cols=2,
         lines=arb([('مِصْر', 'مِصْرِيّ'), ('لُبْنان', 'لُبْنانِيّ'), ('العِراق', 'عِراقِيّ'), ('سُورِيا', 'سُورِيّ')]))]))
PASSAGE = ('اِسْمِي كَرِيم. كُنْتُ فِي مَدْرَسةٍ ابْتِدائِيّةٍ فِي عَمّانَ قَبْلَ الجامِعةِ. لِي صَدِيقٌ اسْمُهُ خالِد، وَكانَ زَمِيلِي فِي المَدْرَسةِ. '
           'أَتَذَكَّرُ الطُّفُولةَ، وَلَكِنْ لا أَحْفَظُ أَسْماءَ كُلِّ الأَفْرادِ. الآنَ يَسْكُنُ خالِد فِي القاهِرةِ، وَهُوَ يُسافِرُ إِلَى عَمّانَ.')
E.append(sec('Reading comprehension', 20, 6, [
    dict(intro='Read the paragraph and answer the questions below.', raw='<div class="ar passage">%s</div>' % PASSAGE, lines=[]),
    dict(intro='1. Answer each question in a full written Arabic sentence. (10 points: 2 points each)', lines=[
        ('<div class="ar q">1) أَيْنَ كانَ كَرِيم قَبْلَ الجامِعةِ؟</div>' + wl(), 'كانَ فِي مَدْرَسةٍ ابْتِدائِيّةٍ فِي عَمّانَ.'),
        ('<div class="ar q">2) مَن خالِد؟</div>' + wl(), 'خالِد صَدِيقُ كَرِيم، وَكانَ زَمِيلَهُ فِي المَدْرَسةِ.'),
        ('<div class="ar q">3) ماذا لا يَحْفَظُ كَرِيم؟</div>' + wl(), 'لا يَحْفَظُ أَسْماءَ كُلِّ الأَفْرادِ.'),
        ('<div class="ar q">4) أَيْنَ يَسْكُنُ خالِد الآنَ؟</div>' + wl(), 'يَسْكُنُ فِي القاهِرةِ.'),
        ('<div class="ar q">5) إِلَى أَيْنَ يُسافِرُ خالِد؟</div>' + wl(), 'يُسافِرُ إِلَى عَمّانَ.')]),
    dict(intro='2. Write one example of each from the paragraph. (6 points)', lines=[
        ('<div class="enl">Past-tense verb &nbsp; -------------------------------------------------------</div>', 'كُنْتُ / كانَ'),
        ('<div class="enl">Present-tense verb &nbsp; -----------------------------------------------------</div>', 'أَتَذَكَّرُ / يَسْكُنُ / يُسافِرُ'),
        ('<div class="enl">Negated verb &nbsp; ----------------------------------------------------------</div>', 'لا أَحْفَظُ'),
        ('<div class="enl">Verb before its subject &nbsp; -------------------------------------------</div>', 'يَسْكُنُ خالِد (the verb comes first)'),
        ('<div class="enl">Sentence with kaana &nbsp; ---------------------------------------------------</div>', 'كُنْتُ فِي مَدْرَسةٍ / كانَ زَمِيلِي فِي المَدْرَسةِ'),
        ('<div class="enl">Idafa &nbsp; ------------------------------------------------------------------</div>', 'أَسْماءَ كُلِّ الأَفْرادِ')]),
    dict(intro='3. Identify the root (<span class="ar">الجذر</span>) of each word. (4 points)', lines=[
        ('<div class="ar">أَحْفَظُ &nbsp; ___ &nbsp;&nbsp;&nbsp; يُسافِرُ &nbsp; ___ &nbsp;&nbsp;&nbsp; أَتَذَكَّرُ &nbsp; ___ &nbsp;&nbsp;&nbsp; يَسْكُنُ &nbsp; ___</div>',
         'ح ف ظ &nbsp; ، &nbsp; س ف ر &nbsp; ، &nbsp; ذ ك ر &nbsp; ، &nbsp; س ك ن')])]))
# ------------------------------------------------------------------ page 6
E.append(sec('Translation', 8, 7, [dict(
    intro='Translate the following sentences. (8 points)',
    lines=tr([
        ('My friend (m.) was in primary school.', 'كانَ صَدِيقِي فِي المَدْرَسةِ الاِبْتِدائِيّةِ'),
        ('I don’t remember all the names.', 'لا أَتَذَكَّرُ كُلَّ الأَسْماءِ'),
        ('The students travel to Jordan.', 'يُسافِرُ الطُّلّابُ إِلَى الأُرْدُنِّ'),
        ('She memorizes the names before the lesson.', 'تَحْفَظُ الأَسْماءَ قَبْلَ الدَّرْسِ'),
        ('I am not a new student (m.).', 'لَسْتُ طالِباً جَدِيداً'),
        ('My uncle’s wife was a friend of my mother.', 'كانَتْ زَوْجةُ عَمِّي صَدِيقةَ والِدَتِي'),
        ('What did you (m.) say?', 'ماذا قُلْتَ؟'),
        ('Where were you (f.)?', 'أَيْنَ كُنْتِ؟')]))]))
E.append(sec('Writing', 12, 7, [dict(
    intro='Write a short paragraph in Arabic (seven to eight sentences) about your childhood or your school. Include at least one sentence with <span class="ar">كان</span>, '
          'one present-tense verb, one negated verb, one verb before its subject, one plural noun, one idafa, and one possessive ending. '
          '(12 points: 3 for content, 4 for grammar and agreement, 3 for vocabulary, 2 for spelling)',
    lines=[(wl(), '') for _ in range(8)],
    model='كُنْتُ فِي مَدْرَسةٍ ابْتِدائِيّةٍ فِي واشِنْطُن. كانَتْ مَدْرَسَتِي كَبِيرةً وَجَمِيلةً. لِي صَدِيقةٌ اسْمُها سارة، وَكانَتْ زَمِيلَتِي فِي المَدْرَسةِ. '
          'أَتَذَكَّرُ الطُّفُولةَ، وَلَكِنْ لا أَحْفَظُ أَسْماءَ كُلِّ الزُّمَلاءِ. تَسْكُنُ سارة الآنَ فِي نِيويُورْك، وَهِيَ تُسافِرُ إِلَى واشِنْطُن. '
          'يَدْرُسُ أَصْدِقائِي فِي جامِعاتٍ مُخْتَلِفةٍ.')]))
E.sort(key=lambda s: s['page'])

NOTES = ('The reading and writing answers can be worded in more than one correct way; a good answer is a complete sentence with correct agreement and sensible case endings. '
         'When the verb comes before its subject it is singular, even if the subject is plural. After <span class="ar">كان</span> and <span class="ar">ليس</span> the predicate is accusative; '
         'a prepositional predicate stays as it is. <span class="ar">اِسْتَمَعَ</span> is Form VIII (<span class="ar">اِفْتَعَلَ</span>). '
         'In the nominal or verbal section, a sentence that starts with a noun is nominal even if its predicate is a verb.')

if __name__ == '__main__':
    title = 'Lesson 4 Exam Practice'
    total = prepare(E)
    p, n = to_pdf(render_exam(E, title, total, (), '.wl{height:14.5pt}'), 'l4e_exam')
    p2, n2 = to_pdf(render_key(E, title, total, NOTES), 'l4e_key')
    print(title, '| points', total, '| exam pages', n, '| key pages', n2)
