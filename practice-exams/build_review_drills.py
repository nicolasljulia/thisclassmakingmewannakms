# -*- coding: utf-8 -*-
# Generates the Review Drill worksheet (a clean copy of the class handout) and Review Drill 2 (same format, new sentences), each with an answer key.
# Run: python3 practice-exams/build_review_drills.py   (needs PyMuPDF and Google Chrome). PDFs are written to practice-exams/build/.
import re
import build_exam as BE
from build_exam import CSS, header, blanks, to_pdf

INSTR = 'Fill in the blanks with the suitable noun, verb, pronoun, etc. Use the word in parentheses, and change it where the sentence needs it.'

# (sentence with @@@ blanks and the hint after each blank, vowelled answer sentence, optional note)
DRILL1 = [
 ('يدرس @@@ (الطالب) الجامعيون في المكتبة كل يوم، ثم @@@ (يذهب) إلى @@@ (بيت+هو) في المساء.',
  'يَدْرُسُ الطُّلّابُ الجامِعِيُّونَ فِي المَكْتَبةِ كُلَّ يَوْمٍ، ثُمَّ يَذْهَبُونَ إلى بُيُوتِهِمْ فِي المَساءِ', 'A verb that comes before its subject stays singular.'),
 ('@@@ (الكتاب) الدراسية جيدة و@@@ (أنا) نحب @@@ (هي) كثيراً.', 'الكُتُبُ الدِّراسِيّةُ جَيِّدةٌ وَنَحْنُ نُحِبُّها كَثِيراً', ''),
 ('يعمل @@@ (والد+أنا) في المكتب @@@ (جديد) في شارع @@@ (واسع) وقريب من @@@ (بيت+نحن).', 'يَعْمَلُ والِدِي فِي المَكْتَبِ الجَدِيدِ فِي شارِعٍ واسِعٍ وَقَرِيبٍ مِن بَيْتِنا', ''),
 ('البنات @@@ (يذهب) إلى @@@ (مدينة) كبيرة مع @@@ (عائلة+هن).', 'البَناتُ يَذْهَبْنَ إلى مُدُنٍ كَبِيرةٍ مَعَ عائِلَتِهِنَّ', 'The plural of a thing takes a feminine singular adjective.'),
 ('يا سارة وعفاف هل @@@ (يدرس) الأدب العربي؟ نعم، نحن @@@ (يدرس+هو).', 'يا سارة وَعَفاف هَلْ تَدْرُسانِ الأَدَبَ العَرَبِيَّ؟ نَعَمْ، نَحْنُ نَدْرُسُهُ', ''),
 ('يا مريم وعادل ومايكل هل @@@ (يشاهد) التلفزيون؟ لا، نحن لا @@@ (يشاهد+هو).', 'يا مَرْيَم وَعادِل وَمايْكِل هَلْ تُشاهِدُونَ التِّلْفِزْيُونَ؟ لا، نَحْنُ لا نُشاهِدُهُ', 'A mixed group takes the masculine plural.'),
 ('غرفة @@@ (رجل) كبيرة وواسعة و@@@ (ليس) جميلة. ولكن غرفة @@@ (بنت+هو) @@@ (واسع) وجميلة أيضاً.',
  'غُرْفةُ رِجالٍ كَبِيرةٌ وَواسِعةٌ وَلَيْسَتْ جَمِيلةً. وَلَكِنْ غُرْفةُ بِنْتِهِ واسِعةٌ وَجَمِيلةٌ أَيْضاً', 'بَناتِهِ is also possible in blank 3. The predicate after لَيْسَ is accusative.'),
 ('هم لا @@@ (يعرف) الجار @@@ (جديد). هم @@@ (يسكن) في نفس @@@ (بناية).', 'هُمْ لا يَعْرِفُونَ الجارَ الجَدِيدَ. هُمْ يَسْكُنُونَ فِي نَفْسِ البِنايةِ', ''),
 ('والد @@@ (صاحب+أنا) @@@ (يدرّس) العلوم @@@ (السياسي) في الكلية @@@ (صغيرة).', 'والِدُ صاحِبِي يُدَرِّسُ العُلُومَ السِّياسِيّةَ فِي الكُلِّيّةِ الصَّغِيرةِ', ''),
 ('عندي @@@ (صورة) كثيرة لأقاربي ولكن لا أعرف @@@ (اسم+هم) كلهم.', 'عِنْدِي صُوَرٌ كَثِيرةٌ لِأَقارِبِي وَلَكِنْ لا أَعْرِفُ أَسْماءَهُمْ كُلَّهُمْ', ''),
 ('والدي @@@ (سوريا) ووالدتي @@@ (السعودية) وجدتي @@@ (اليونان) وأنا @@@ (أمريكا).', 'والِدِي سُورِيٌّ وَوالِدَتِي سُعُودِيّةٌ وَجَدَّتِي يُونانِيّةٌ وَأَنا أَمْرِيكِيٌّ', ''),
 ('أستاذ صف @@@ (لغة) الإنجليزية ممتاز وهو @@@ (يفهم) @@@ (لغة) كثيرة.', 'أُسْتاذُ صَفِّ لُغةِ الإِنْجِلِيزِيّةِ مُمْتازٌ وَهُوَ يَفْهَمُ لُغاتٍ كَثِيرةً', ''),
]

DRILL2 = [
 ('تدرس @@@ (الطالبة) الجديدات في الكلية كل يوم، ثم @@@ (يذهب) إلى @@@ (بيت+هن) في المساء.',
  'تَدْرُسُ الطّالِباتُ الجَدِيداتُ فِي الكُلِّيّةِ كُلَّ يَوْمٍ، ثُمَّ يَذْهَبْنَ إلى بُيُوتِهِنَّ فِي المَساءِ', 'The verb before its subject stays singular; the second verb has no stated subject, so it agrees.'),
 ('@@@ (الرسالة، جمع) الطويلة جميلة ونحن @@@ (يقرأ+هي) كل مساء.', 'الرَّسائِلُ الطَّوِيلةُ جَمِيلةٌ وَنَحْنُ نَقْرَؤُها كُلَّ مَساءٍ', 'A plural of things takes a feminine singular adjective.'),
 ('@@@ (عم+أنا) @@@ (ضابط) في الجيش الأردني وهو يسكن في بيت @@@ (واسع) و@@@ (قريب) من @@@ (بيت+نحن).',
  'عَمِّي ضابِطٌ فِي الجَيْشِ الأُرْدُنِّيِّ وَهُوَ يَسْكُنُ فِي بَيْتٍ واسِعٍ وَقَرِيبٍ مِن بَيْتِنا', ''),
 ('البنات @@@ (يسكن) في @@@ (مدينة، جمع) كبيرة مع @@@ (أخت+هن).', 'البَناتُ يَسْكُنَّ فِي مُدُنٍ كَبِيرةٍ مَعَ أُخْتِهِنَّ', 'The ة turns into ت before the suffix.'),
 ('يا ليلى ومنى هل @@@ (يشاهد) الأخبار؟ نعم، نحن @@@ (يشاهد+هي).', 'يا لَيْلى وَمُنَى هَلْ تُشاهِدانِ الأَخْبارَ؟ نَعَمْ، نَحْنُ نُشاهِدُها', ''),
 ('يا أحمد وسامر وكريم هل @@@ (يعرف) أقارب @@@ (صاحب+أنا)؟ لا، نحن لا @@@ (يعرف+هم).', 'يا أَحْمَد وَسامِر وَكَرِيم هَلْ تَعْرِفُونَ أَقارِبَ صاحِبِي؟ لا، نَحْنُ لا نَعْرِفُهُمْ', ''),
 ('بيت @@@ (جد+أنا) كبير وقديم، ولكنه @@@ (ليس) @@@ (جميل).', 'بَيْتُ جَدِّي كَبِيرٌ وَقَدِيمٌ، وَلَكِنَّهُ لَيْسَ جَمِيلاً', 'The predicate after لَيْسَ is accusative.'),
 ('هم لا @@@ (يعرف) الأستاذ @@@ (جديد). هم @@@ (يدرس) في نفس @@@ (كلية).', 'هُمْ لا يَعْرِفُونَ الأُسْتاذَ الجَدِيدَ. هُمْ يَدْرُسُونَ فِي نَفْسِ الكُلِّيّةِ', ''),
 ('والدة @@@ (صديقة+أنا) @@@ (يدرّس) @@@ (تاريخ) في الكلية @@@ (كبيرة).', 'والِدةُ صَدِيقَتِي تُدَرِّسُ التّارِيخَ فِي الكُلِّيّةِ الكَبِيرةِ', 'The subject is feminine, so the verb is تُدَرِّسُ.'),
 ('عندي @@@ (رسالة، جمع) كثيرة من @@@ (خالة+أنا) ولكن لا @@@ (يقرأ+هي) كلها.', 'عِنْدِي رَسائِلُ كَثِيرةٌ مِن خالَتِي وَلَكِنْ لا أَقْرَؤُها كُلَّها', ''),
 ('جدي @@@ (مصر) وجدتي @@@ (اليمن) وأخواتي @@@ (الجزائر) وأنا @@@ (الأردن).', 'جَدِّي مِصْرِيٌّ وَجَدَّتِي يَمَنِيّةٌ وَأَخَواتِي جَزائِرِيّاتٌ وَأَنا أُرْدُنِّيٌّ', ''),
 ('أستاذ صف @@@ (لغة) الفرنسية ممتاز وهو @@@ (يفهم) @@@ (لغة، جمع) كثيرة.', 'أُسْتاذُ صَفِّ لُغةِ الفَرَنْسِيّةِ مُمْتازٌ وَهُوَ يَفْهَمُ لُغاتٍ كَثِيرةً', ''),
 ('@@@ (كان) جدي @@@ (مهندس) وجدتي @@@ (كان) @@@ (موظفة).', 'كانَ جَدِّي مُهَنْدِساً وَجَدَّتِي كانَتْ مُوَظَّفةً', 'The predicate after كانَ is accusative.'),
 ('في الكلية @@@ (12) @@@ (أستاذ) و@@@ (30) @@@ (موظف).', 'فِي الكُلِّيّةِ اِثْنا عَشَرَ أُسْتاذاً وَثَلاثُونَ مُوَظَّفاً', 'After 11 to 99 the counted noun is singular and accusative.'),
]

def render(items, title, key=False):
    out = ['<div class="page">' + header(title + (': Answer Key' if key else ''))]
    out.append('<div class="intro" style="margin-bottom:8pt;">%s</div>' % INSTR if not key else '<div class="keynote">Short vowels and case endings are shown in full. Where more than one answer fits, any grammatical one earns credit.</div>')
    for i, (q, a, note) in enumerate(items, 1):
        if key:
            out.append('<div class="ansrow" style="display:flex;gap:8pt;align-items:baseline;margin:5pt 0;"><span class="num" style="min-width:20pt;">%d)</span><div style="flex:1"><div class="ans">%s</div>%s</div></div>' % (
                i, a, ('<div class="keynote" style="margin:0">%s</div>' % note) if note else ''))
        else:
            out.append('<div class="ar" style="margin:4pt 0;line-height:1.55;">%d) %s</div>' % (i, blanks(q)))
    if not key:
        out.append('<div class="goodluck"><div class="ar">بالتوفيق إن شاء الله</div><div>Good Luck</div></div>')
    out.append('</div>')
    return '<!doctype html><html><head><meta charset="utf-8"><title>%s</title><style>%s .blank{min-width:62px}.ar{font-size:13pt}.goodluck{margin-top:4pt}</style></head><body>%s</body></html>' % (title, CSS, ''.join(out))

if __name__ == '__main__':
    for key, items, title in (('rd1', DRILL1, 'Review Drill'), ('rd2', DRILL2, 'Review Drill 2')):
        _, n1 = to_pdf(render(items, title), key + '_ws')
        _, n2 = to_pdf(render(items, title, True), key + '_key')
        print(title, '| worksheet pages', n1, '| key pages', n2)
