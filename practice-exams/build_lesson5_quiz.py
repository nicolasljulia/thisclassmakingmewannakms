# -*- coding: utf-8 -*-
# Generates the Lesson 5 practice quiz (Tuesday, Nov 17) and its answer key, in the same format as the other practice exams.
# Run: python3 practice-exams/build_lesson5_quiz.py   (needs PyMuPDF and Google Chrome). PDFs are written to practice-exams/build/.
import build_practice as BP
from build_practice import sec, ar, en, wl, prepare, render_exam, render_key
from build_exam import to_pdf

def tr(items, start=1):
    return [('<div class="enl">%d- %s &nbsp; ------------------------------------------</div>' % (i, e), a) for i, (e, a) in enumerate(items, start)]
def arw(items): return [(ar(i, q + '<div class="wl"></div>'), a) for i, (q, a) in enumerate(items, 1)]
def arb(items): return [(ar(i, q + ' &nbsp; ___'), a) for i, (q, a) in enumerate(items, 1)]

Q = []
Q.append(sec('Vocabulary', 10, 1, [dict(
    intro='Write the Arabic for each word. (10 points)', cols=2,
    lines=[(en(i, e), a) for i, (e, a) in enumerate([
        ('winter', 'الشِّتاء'), ('spring', 'الرَّبِيع'), ('humidity', 'الرُّطُوبة'), ('loneliness', 'الوِحْدة'), ('crowding', 'الازْدِحام'),
        ('because of', 'بِسَبَبِ'), ('very', 'جِدّاً'), ('sometimes', 'أَحْياناً'), ('only', 'فَقَط'), ('semester', 'فَصْل دِراسِيّ')], 1)])]))
Q.append(sec('Seasons and weather', 9, 1, [
    dict(intro='1. Write the four seasons in Arabic. (4 points)', cols=2,
         lines=arb([('summer', 'الصَّيْف'), ('autumn', 'الخَرِيف'), ('winter', 'الشِّتاء'), ('spring', 'الرَّبِيع')])),
    dict(intro='2. Write the plural of <span class="ar">فَصْل</span>. (1 point)', lines=arb([('فَصْل', 'فُصُول')])),
    dict(intro='3. Write the Arabic for each word. (4 points)', cols=2,
         lines=[(en(i, e), a) for i, (e, a) in enumerate([('weather (two words)', 'الطَّقْس / الجَوّ'), ('temperature', 'دَرَجةُ الحَرارةِ'), ('humidity', 'الرُّطُوبة'), ('high (f.)', 'عالِية')], 1)])]))
Q.append(sec('Case endings', 6, 1, [dict(
    intro='Add the suitable case endings. (6 points)',
    lines=arw([('أحب الصيف كثيرا.', 'أُحِبُّ الصَّيْفَ كَثِيراً.'), ('الطقس بارد جدا في الشتاء.', 'الطَّقْسُ بارِدٌ جِدّاً فِي الشِّتاءِ.'),
               ('الرطوبة عالية في المدينة.', 'الرُّطُوبةُ عالِيةٌ فِي المَدِينةِ.'), ('كان الطقس حارا.', 'كانَ الطَّقْسُ حارّاً.'),
               ('أشعر بالوحدة أحيانا.', 'أَشْعُرُ بِالوِحْدةِ أَحْياناً.'), ('لا أحب الازدحام بسبب الطقس.', 'لا أُحِبُّ الازْدِحامَ بِسَبَبِ الطَّقْسِ.')]))]))
Q.append(sec('The accusative noun', 6, 2, [dict(
    intro='Write the underlined word in the accusative if it should be accusative; if not, write <b>no</b>. Give the reason in a few words. (6 points)',
    lines=arw([('كانَ الطَّقْسُ <u>بارِد</u> فِي الخَرِيفِ.', 'بارِداً (predicate of كان)'), ('أُحِبُّ <u>الشِّتاءُ</u> كَثِيراً.', 'الشِّتاءَ (direct object)'),
               ('الطَّقْسُ حارٌّ <u>جِدّ</u>.', 'جِدّاً (adverb)'), ('لَيْسَ <u>الطَّقْسُ</u> بارِداً.', 'no (the subject of لَيْسَ stays nominative)'),
               ('دَرَجةُ <u>الحَرارةُ</u> عالِيةٌ.', 'no, it should be genitive: الحَرارةِ (second term of the idafa)'), ('أَشْعُرُ <u>أَحْيان</u> بِالوِحْدةِ.', 'أَحْياناً (adverb)')]))]))
# ------------------------------------------------------------------ page 2
Q.append(sec('The absolute object', 6, 2, [
    dict(intro='1. Fill in the verbal noun of the verb, in the accusative. (5 points)',
         lines=arb([('أُحِبُّ الخَرِيفَ ___ كَبِيراً.', 'حُبّاً'), ('دَرَسَ أَحْمَد العَرَبِيّةَ ___ جَيِّدةً.', 'دِراسةً'), ('أَشْعُرُ بِالوِحْدةِ ___ كَبِيراً.', 'شُعُوراً'),
                    ('سافَرْتُ إِلَى القاهِرةِ ___ طَوِيلاً.', 'سَفَراً'), ('قَرَأَتْ سارة القِصّةَ ___ جَيِّدةً.', 'قِراءةً')])),
    dict(intro='2. Say it in Arabic with an absolute object: <i>She wrote the letter well.</i> (1 point)',
         lines=[(wl(), 'كَتَبَتِ الرِّسالةَ كِتابةً جَيِّدةً.')])]))
Q.append(sec('The verbal noun', 6, 3, [dict(
    intro='Write the verbal noun (masdar) of each verb. (6 points)', cols=2,
    lines=arb([('سافَرَ', 'السَّفَر'), ('دَرَسَ', 'الدِّراسة'), ('كَتَبَ', 'الكِتابة'), ('قَرَأَ', 'القِراءة'), ('دَرَّسَ', 'التَّدْرِيس'), ('عَمِلَ', 'العَمَل')]))]))
Q.append(sec('Adverbs', 4, 3, [dict(
    intro='Write each word with its accusative ending (tanween fatha). (4 points)', cols=2,
    lines=arb([('كَثِير', 'كَثِيراً'), ('أَحْيان', 'أَحْياناً'), ('قَلِيل', 'قَلِيلاً'), ('مَدْرَسة (indefinite)', 'مَدْرَسةً (no alif after a taa marbuuTa)')]))]))
Q.append(sec('Phrases', 6, 3, [dict(
    intro='Say it in Arabic with the correct case endings. (6 points)',
    lines=[(en(i, e), a) for i, (e, a) in enumerate([
        ('because of the crowding', 'بِسَبَبِ الازْدِحامِ'), ('as far as I am concerned', 'بِالنِّسْبةِ لِي'), ('the best season', 'أَحْسَنُ فَصْلٍ'),
        ('I feel loneliness', 'أَشْعُرُ بِالوِحْدةِ'), ('I am of Egyptian descent', 'أَنا مِن أَصْلٍ مِصْرِيٍّ'), ('a high temperature', 'دَرَجةُ حَرارةٍ عالِيةٌ')], 1)])]))
PASSAGE = ('أُحِبُّ الخَرِيفَ كَثِيراً. الطَّقْسُ فِي الخَرِيفِ جَمِيلٌ. فِي الصَّيْفِ الطَّقْسُ حارٌّ جِدّاً وَالرُّطُوبةُ عالِيةٌ، وَلا أُحِبُّ الصَّيْفَ بِسَبَبِ الحَرارةِ. '
           'بِالنِّسْبةِ لِي، أَحْسَنُ فَصْلٍ هُوَ الرَّبِيعُ. أَشْعُرُ أَحْياناً بِالوِحْدةِ فِي الشِّتاءِ.')
Q.append(sec('Reading comprehension', 12, 4, [
    dict(intro='Read the paragraph and answer the questions below.', raw='<div class="ar passage">%s</div>' % PASSAGE, lines=[]),
    dict(intro='1. Answer each question in a full written Arabic sentence. (10 points: 2 points each)', lines=[
        ('<div class="ar q">1) كَيْفَ الطَّقْسُ فِي الخَرِيفِ؟</div>' + wl(), 'الطَّقْسُ جَمِيلٌ فِي الخَرِيفِ.'),
        ('<div class="ar q">2) كَيْفَ الطَّقْسُ فِي الصَّيْفِ؟</div>' + wl(), 'الطَّقْسُ حارٌّ جِدّاً وَالرُّطُوبةُ عالِيةٌ.'),
        ('<div class="ar q">3) لِماذا لا يُحِبُّ الكاتِبُ الصَّيْفَ؟</div>' + wl(), 'لا يُحِبُّ الصَّيْفَ بِسَبَبِ الحَرارةِ.'),
        ('<div class="ar q">4) ما أَحْسَنُ فَصْلٍ بِالنِّسْبةِ لِلْكاتِبِ؟</div>' + wl(), 'أَحْسَنُ فَصْلٍ هُوَ الرَّبِيعُ.'),
        ('<div class="ar q">5) مَتى يَشْعُرُ الكاتِبُ بِالوِحْدةِ؟</div>' + wl(), 'يَشْعُرُ بِالوِحْدةِ أَحْياناً فِي الشِّتاءِ.')]),
    dict(intro='2. Write one example of each from the paragraph. (2 points)', lines=[
        ('<div class="enl">An adverb in the accusative &nbsp; ---------------------------------------</div>', 'كَثِيراً / جِدّاً / أَحْياناً'),
        ('<div class="enl">A noun in the genitive after a preposition &nbsp; --------------------</div>', 'الخَرِيفِ / الصَّيْفِ / الشِّتاءِ / الحَرارةِ')])]))
Q.append(sec('Translation', 6, 4, [dict(
    intro='Translate the following sentences. (6 points)',
    lines=tr([
        ('I like autumn a lot.', 'أُحِبُّ الخَرِيفَ كَثِيراً'), ('The weather was very cold.', 'كانَ الطَّقْسُ بارِداً جِدّاً'),
        ('The humidity is high in summer.', 'الرُّطُوبةُ عالِيةٌ فِي الصَّيْفِ'), ('I don’t like crowding.', 'لا أُحِبُّ الازْدِحامَ'),
        ('As far as I am concerned, winter is the best season.', 'بِالنِّسْبةِ لِي، الشِّتاءُ أَحْسَنُ فَصْلٍ'), ('I studied Arabic well.', 'دَرَسْتُ العَرَبِيّةَ دِراسةً جَيِّدةً')]))]))
Q.sort(key=lambda s: s['page'])
NOTES = ('The reading answers can be worded in more than one correct way; a good answer is a complete sentence with correct agreement and sensible case endings. '
         'The absolute object is a masdar of the same verb, accusative and indefinite, followed by an accusative adjective that agrees with it. '
         'Adverbs such as <span class="ar">جِدّاً، كَثِيراً، أَحْياناً</span> are accusative with tanween fatha; the alif is not added after a taa marbuuTa.')
if __name__ == '__main__':
    title = 'Lesson 5 Practice Quiz'
    total = prepare(Q)
    p, n = to_pdf(render_exam(Q, title, total, (), '.wl{height:14.5pt}'), 'l5q_exam')
    p2, n2 = to_pdf(render_key(Q, title, total, NOTES), 'l5q_key')
    print(title, '| points', total, '| exam pages', n, '| key pages', n2)
