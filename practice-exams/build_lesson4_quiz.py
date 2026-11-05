# -*- coding: utf-8 -*-
# Generates the Lesson 4 practice quiz (Thursday, Nov 5) and its answer key, in the same format as the other practice exams.
# Run: python3 practice-exams/build_lesson4_quiz.py   (needs PyMuPDF and Google Chrome). PDFs are written to practice-exams/build/.
import build_practice as BP
from build_practice import sec, ar, en, wl, prepare, render_exam, render_key
from build_exam import to_pdf

def line(label):
    return '<div class="enl">%s &nbsp; ------------------------------------------------------------</div>' % label

def tr(items, start=1):
    return [('<div class="enl">%d- %s &nbsp; ------------------------------------------</div>' % (i, e), a) for i, (e, a) in enumerate(items, start)]

Q = []
# ------------------------------------------------------------------ page 1
Q.append(sec('Vocabulary', 8, 1, [dict(
    intro='Write the Arabic for each word. (8 points)', cols=2,
    lines=[(en(i, e), a) for i, (e, a) in enumerate([
        ('school', 'مَدْرَسة'), ('classmate (f.)', 'زَمِيلة'), ('friend (m.)', 'صَدِيق'), ('childhood', 'الطُّفُولة'),
        ('before', 'قَبْلَ'), ('I memorize', 'أَحْفَظ'), ('I remember', 'أَتَذَكَّر'), ('she travels', 'تُسافِر (إِلَى)')], 1)])]))
Q.append(sec('Plurals', 6, 1, [dict(
    intro='Write the plural of each noun. (6 points)', cols=2,
    lines=[(ar(i, s + ' &nbsp; ___'), p) for i, (s, p) in enumerate([
        ('مَدْرَسة', 'مَدارِس'), ('زَمِيل', 'زُمَلاء'), ('صَدِيقة', 'صَدِيقات'), ('فَرْد', 'أَفْراد'), ('صَدِيق', 'أَصْدِقاء'), ('زَمِيلة', 'زَمِيلات')], 1)])]))
Q.append(sec('The present tense', 8, 1, [dict(
    intro='Write the present-tense form of the verb for the pronoun. (8 points)', cols=2,
    lines=[(ar(i, q + ' &nbsp; ___'), a) for i, (q, a) in enumerate([
        ('(كَتَبَ / هِيَ)', 'تَكْتُبُ'), ('(قَرَأَ / أَنا)', 'أَقْرَأُ'), ('(دَرَسَ / نَحْنُ)', 'نَدْرُسُ'), ('(شاهَدَ / أَنا)', 'أُشاهِدُ'),
        ('(ذَهَبَ / هُمْ)', 'يَذْهَبُونَ'), ('(حَفِظَ / أَنْتَ)', 'تَحْفَظُ'), ('(سافَرَ / نَحْنُ)', 'نُسافِرُ'), ('(عَرَفَ / أَنْتِ)', 'تَعْرِفِينَ')], 1)])]))
Q.append(sec('Negation', 5, 1, [dict(
    intro='Make each sentence negative. (5 points)',
    lines=[(ar(i, q + '<div class="wl"></div>'), a) for i, (q, a) in enumerate([
        ('أَنا أَشْرَبُ القَهْوةَ.', 'أَنا لا أَشْرَبُ القَهْوةَ.'),
        ('هُوَ يَقْرَأُ الرِّسالةَ.', 'هُوَ لا يَقْرَأُ الرِّسالةَ.'),
        ('تَسْكُنُ زَمِيلَتِي فِي القاهِرةِ.', 'لا تَسْكُنُ زَمِيلَتِي فِي القاهِرةِ.'),
        ('نَحْنُ نَدْرُسُ فِي المَكْتَبةِ.', 'نَحْنُ لا نَدْرُسُ فِي المَكْتَبةِ.'),
        ('يَعْمَلُ والِدِي فِي بَنْكٍ.', 'لا يَعْمَلُ والِدِي فِي بَنْكٍ.')], 1)])]))
# ------------------------------------------------------------------ page 2
Q.append(sec('The verbal sentence', 6, 2, [dict(
    intro='Rewrite each nominal sentence as a verbal sentence: put the verb first. (6 points)',
    lines=[(ar(i, q + '<div class="wl"></div>'), a) for i, (q, a) in enumerate([
        ('الأَصْدِقاءُ يَسْكُنُونَ فِي القاهِرةِ.', 'يَسْكُنُ الأَصْدِقاءُ فِي القاهِرةِ.'),
        ('الطّالِبةُ تَحْفَظُ الأَسْماءَ.', 'تَحْفَظُ الطّالِبةُ الأَسْماءَ.'),
        ('الزُّمَلاءُ يَدْرُسُونَ فِي المَكْتَبةِ.', 'يَدْرُسُ الزُّمَلاءُ فِي المَكْتَبةِ.'),
        ('البَناتُ يَشْرَبْنَ القَهْوةَ.', 'تَشْرَبُ البَناتُ القَهْوةَ.'),
        ('أُخْتِي تُسافِرُ إِلَى القاهِرةِ.', 'تُسافِرُ أُخْتِي إِلَى القاهِرةِ.'),
        ('الأُسْتاذُ يَقْرَأُ الرِّسالةَ.', 'يَقْرَأُ الأُسْتاذُ الرِّسالةَ.')], 1)])]))
Q.append(sec('Verb agreement', 5, 2, [dict(
    intro='Choose the verb that agrees with the subject. (5 points)',
    lines=[(ar(i, q), a) for i, (q, a) in enumerate([
        ('___ الطُّلّابُ فِي المَكْتَبةِ. &nbsp; (يَدْرُسُ / يَدْرُسُونَ)', 'يَدْرُسُ (the verb comes first, so it is singular)'),
        ('الطُّلّابُ ___ فِي المَكْتَبةِ. &nbsp; (يَدْرُسُ / يَدْرُسُونَ)', 'يَدْرُسُونَ (the subject comes first, so the verb agrees with it)'),
        ('___ الزَّمِيلاتُ إِلَى المَدْرَسةِ. &nbsp; (تَذْهَبُ / يَذْهَبْنَ)', 'تَذْهَبُ'),
        ('الزَّمِيلاتُ ___ إِلَى المَدْرَسةِ. &nbsp; (تَذْهَبُ / يَذْهَبْنَ)', 'يَذْهَبْنَ'),
        ('___ الأَصْدِقاءُ الرَّسائِلَ. &nbsp; (يَكْتُبُ / يَكْتُبُونَ)', 'يَكْتُبُ')], 1)])]))
Q.append(sec('Verb forms', 8, 2, [
    dict(intro='1. Give the form number (<span class="ar">وَزْن</span>) of each past-tense verb. (4 points)', cols=2,
         lines=[(ar(i, q + ' &nbsp; ___'), a) for i, (q, a) in enumerate([
             ('سافَرَ', 'III'), ('أَرْسَلَ', 'IV'), ('اِسْتَمَعَ', 'VIII'), ('تَخَصَّصَ', 'V')], 1)]),
    dict(intro='2. Write the present tense for <span class="ar">هُوَ</span>. (4 points)', cols=2,
         lines=[(ar(i, q + ' &nbsp; ___'), a) for i, (q, a) in enumerate([
             ('شاهَدَ', 'يُشاهِدُ'), ('تَذَكَّرَ', 'يَتَذَكَّرُ'), ('دَرَّسَ', 'يُدَرِّسُ'), ('أَرْسَلَ', 'يُرْسِلُ')], 1)])]))
Q.append(sec('Hamza', 6, 2, [dict(
    intro='Write <b>Q</b> if the first hamza is hamzat al-qaTʿ, or <b>W</b> if it is hamzat al-waSl. (6 points)', cols=2,
    lines=[(ar(i, q + ' &nbsp; ___'), a) for i, (q, a) in enumerate([
        ('اِبْنَة', 'W'), ('أَخ', 'Q'), ('اِمْرَأة', 'W'), ('أُحِبُّ', 'Q'), ('اِثْنان', 'W'), ('أَصْدِقاء', 'Q')], 1)])]))
# ------------------------------------------------------------------ page 3
Q.append(sec('Hollow verbs', 10, 3, [dict(
    intro='Write the form asked for. (10 points)', cols=2,
    lines=[(ar(i, q + ' &nbsp; ___'), a) for i, (q, a) in enumerate([
        ('(نامَ / هُوَ، present)', 'يَنامُ'), ('(سارَ / أَنا، past)', 'سِرْتُ'), ('(قالَ / هِيَ، past)', 'قالَتْ'),
        ('(كانَ / أَنْتَ، past)', 'كُنْتَ'), ('(قالَ / أَنا، present)', 'أَقُولُ'), ('(كانَ / هُمْ، past)', 'كانُوا'),
        ('(نامَ / نَحْنُ، past)', 'نِمْنا'), ('(سارَ / هُنَّ، present)', 'يَسِرْنَ'), ('(كانَ / نَحْنُ، present)', 'نَكُونُ'),
        ('(قالَ / أَنْتَ، past)', 'قُلْتَ')], 1)])]))
Q.append(sec('Kaana', 5, 3, [dict(
    intro='Say each sentence in the past with <span class="ar">كان</span>. Add the case ending of the predicate. (5 points)',
    lines=[(ar(i, q + '<div class="wl"></div>'), a) for i, (q, a) in enumerate([
        ('المَدِينةُ كَبِيرةٌ.', 'كانَتِ المَدِينةُ كَبِيرةً.'),
        ('أَنا مَشْغُولٌ.', 'كُنْتُ مَشْغُولاً.'),
        ('الطُّلّابُ فِي الصَّفِّ.', 'كانَ الطُّلّابُ فِي الصَّفِّ.'),
        ('أَنْتِ وَحِيدةٌ.', 'كُنْتِ وَحِيدةً.'),
        ('الكِتابُ جَدِيدٌ.', 'كانَ الكِتابُ جَدِيداً.')], 1)])]))
PASSAGE = ('اِسْمِي لَيْلَى. كُنْتُ فِي مَدْرَسةٍ ابْتِدائِيّةٍ فِي القاهِرةِ قَبْلَ الجامِعةِ. لِي صَدِيقةٌ اسْمُها سَلْمَى، وَكانَتْ زَمِيلَتِي فِي المَدْرَسةِ. '
           'أَتَذَكَّرُ الطُّفُولةَ وَأَحْفَظُ أَسْماءَ كُلِّ الأَصْدِقاءِ. الآنَ لا تَسْكُنُ سَلْمَى فِي القاهِرةِ، وَهِيَ تُسافِرُ إِلَى عَمّانَ.')
Q.append(sec('Reading comprehension', 15, 4, [
    dict(intro='Read the paragraph and answer the questions below.', raw='<div class="ar passage">%s</div>' % PASSAGE, lines=[]),
    dict(intro='1. Answer each question in a full written Arabic sentence. (8 points)', lines=[
        ('<div class="ar q">1) أَيْنَ كانَتْ لَيْلَى قَبْلَ الجامِعةِ؟</div>' + wl(), 'كانَتْ فِي مَدْرَسةٍ ابْتِدائِيّةٍ فِي القاهِرةِ.'),
        ('<div class="ar q">2) مَن سَلْمَى؟</div>' + wl(), 'سَلْمَى صَدِيقةُ لَيْلَى وَزَمِيلَتُها.'),
        ('<div class="ar q">3) ماذا تَحْفَظُ لَيْلَى؟</div>' + wl(), 'تَحْفَظُ أَسْماءَ كُلِّ الأَصْدِقاءِ.'),
        ('<div class="ar q">4) إِلَى أَيْنَ تُسافِرُ سَلْمَى؟</div>' + wl(), 'تُسافِرُ سَلْمَى إِلَى عَمّانَ.')]),
    dict(intro='2. Write one example of each from the paragraph. (4 points)', lines=[
        ('<div class="enl">Past-tense verb &nbsp; -------------------------------------------------------</div>', 'كُنْتُ / كانَتْ'),
        ('<div class="enl">Present-tense verb &nbsp; -----------------------------------------------------</div>', 'أَتَذَكَّرُ / أَحْفَظُ / تُسافِرُ'),
        ('<div class="enl">Negated verb &nbsp; ----------------------------------------------------------</div>', 'لا تَسْكُنُ'),
        ('<div class="enl">Verb before its subject &nbsp; -------------------------------------------</div>', 'لا تَسْكُنُ سَلْمَى (the verb comes first)')]),
    dict(intro='3. Identify the root (<span class="ar">الجذر</span>) of each word. (3 points)', lines=[
        ('<div class="ar">أَحْفَظُ &nbsp; ___ &nbsp;&nbsp;&nbsp;&nbsp; تُسافِرُ &nbsp; ___ &nbsp;&nbsp;&nbsp;&nbsp; أَتَذَكَّرُ &nbsp; ___</div>', 'ح ف ظ &nbsp; ، &nbsp; س ف ر &nbsp; ، &nbsp; ذ ك ر')])]))
Q.append(sec('Translation', 5, 4, [dict(
    intro='Translate the following sentences. (5 points)',
    lines=tr([
        ('I was in primary school before the university.', 'كُنْتُ فِي المَدْرَسةِ الاِبْتِدائِيّةِ قَبْلَ الجامِعةِ'),
        ('My friend (f.) does not travel to Cairo.', 'صَدِيقَتِي لا تُسافِرُ إِلَى القاهِرةِ'),
        ('The students memorize the names.', 'يَحْفَظُ الطُّلّابُ الأَسْماءَ'),
        ('I remember my childhood.', 'أَتَذَكَّرُ طُفُولَتِي'),
        ('My classmates (m.) were in the library.', 'كانَ زُمَلائِي فِي المَكْتَبةِ')]))]))
Q.sort(key=lambda s: s['page'])

NOTES = ('The reading answers can be worded in more than one correct way; a good answer is a complete sentence with correct agreement and sensible case endings. '
         'When the verb comes before its subject it is singular, even if the subject is plural; when the subject comes first, the verb agrees with it in number and gender. '
         'In the kaana section the predicate is accusative. In the verb-form section, <span class="ar">اِسْتَمَعَ</span> is Form VIII (<span class="ar">اِفْتَعَلَ</span>).')

if __name__ == '__main__':
    title = 'Lesson 4 Practice Quiz'
    total = prepare(Q)
    p, n = to_pdf(render_exam(Q, title, total, (), '.wl{height:14.5pt}'), 'l4q_exam')
    p2, n2 = to_pdf(render_key(Q, title, total, NOTES), 'l4q_key')
    print(title, '| points', total, '| exam pages', n, '| key pages', n2)
