import streamlit as st
import re

st.title("Ask Samra Electricity Generating Company (Smart Local)")

question = st.text_input("اكتب سؤالك هنا:")

# قراءة الملف وتقسيمه لفقرات
with open("samra_info.txt", "r", encoding="utf-8") as f:
    data = f.read()

# تقسيم النص لفقرات ثم لجمل
paragraphs = [p.strip() for p in data.split("\n\n") if p.strip()]
sentences = []
for para in paragraphs:
    sentences.extend(re.split(r'[.!؟]', para))  # فصل الجمل

# قاموس الكلمات المفتاحية ومرادفاتها
synonyms = {
    "رؤية": ["رؤية", "vision"],
    "مهمة": ["مهمة", "mission"],
    "رأس المال": ["رأس المال", "capital"],
    "الملكية": ["الملكية", "ownership"],
    "وحدات الغاز": ["وحدات الغاز", "gas units"],
    "وحدات البخار": ["وحدات البخار", "steam units"],
    "وحدات الطاقة الشمسية": ["طاقة شمسية", "solar plant"],
    "وحدات الرياح": ["محطة الرياح", "wind plant"],
    "المصنعين": ["General Electric", "Fuji Electric", "DONGFANG"],
    "مواقع المحطات": ["Samra", "Al-Zatary", "Al Azraq", "South Amman", "Ma’an", "Sheikh Zayed", "Risha", "Rehab"],
    # ممكن تضيفي كلمات مفتاحية إضافية لاحقًا
}

def search_answer(question, sentences, synonyms):
    question_lower = question.lower()
    best_match = ""
    max_count = 0

    for sentence in sentences:
        count = 0
        for key, words in synonyms.items():
            for word in words:
                if word.lower() in sentence.lower() and word.lower() in question_lower:
                    count += 1
        # نزيد التقييم حسب تطابق كلمات السؤال العادية
        for word in question_lower.split():
            if word in sentence.lower():
                count += 1
        if count > max_count:
            max_count = count
            best_match = sentence

    return best_match.strip() if max_count > 0 else None

if st.button("جاوبني"):
    if question.strip() == "":
        st.write("رجاءً أدخل سؤال.")
    else:
        answer = search_answer(question, sentences, synonyms)
        if answer:
            st.write("الجواب:", answer)
        else:
            st.write("آسف، لا توجد معلومات دقيقة لهذا السؤال حالياً.")
