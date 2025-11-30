import streamlit as st
import edge_tts
import asyncio
import io

# إعدادات الصفحة
st.set_page_config(
    page_title="محول النص إلى صوت",
    page_icon="🎙️",
    layout="wide"
)

# تنسيق عربي
st.markdown("""
<style>
    .main { direction: rtl; }
    .stTextArea textarea { 
        font-size: 18px; 
        font-family: 'Arial', sans-serif;
    }
    .success-msg {
        background-color: #d4edda;
        color: #155724;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
</style>
""", unsafe_allow_html=True)

# عنوان التطبيق
st.title("🎙️ محول النص إلى صوت")
st.write("---")

# قسم الإدخال
col1, col2 = st.columns([2, 1])

with col1:
    text = st.text_area(
        "📝 أدخل النص الذي تريد تحويله إلى صوت:",
        height=150,
        placeholder="اكتب النص هنا بالعربية أو الإنجليزية...\nType your text here in Arabic or English..."
    )

with col2:
    st.write("**⚙️ الإعدادات:**")
    
    # قائمة الأصوات الموسعة
    voices = {
        "العربية 🇸🇦": [
            "ar-SA-HamedNeural",      # ذكر - هامد
            "ar-SA-ZariyahNeural",    # أنثى - زاريا
            "ar-SA-NaayfNeural",      # ذكر - نايف
            "ar-EG-SalmaNeural",      # أنثى - سلمى (مصر)
            "ar-EG-ShakirNeural",     # ذكر - شاكر (مصر)
            "ar-AE-FatimaNeural",     # أنثى - فاطمة (الإمارات)
            "ar-AE-HamdanNeural",     # ذكر - حمدان (الإمارات)
            "ar-QA-AmalNeural",       # أنثى - أمل (قطر)
            "ar-QA-MoazNeural",       # ذكر - معاذ (قطر)
            "ar-KW-FahedNeural",      # ذكر - فاهد (الكويت)
            "ar-KW-NouraNeural"       # أنثى - نورا (الكويت)
        ],
        "الإنجليزية 🇺🇸🇬🇧": [
            "en-US-AriaNeural",       # أنثى - آريا
            "en-US-JennyNeural",      # أنثى - جيني
            "en-US-ChristopherNeural",# ذكر - كريستوفر
            "en-US-EricNeural",       # ذكر - إيريك
            "en-US-GuyNeural",        # ذكر - جاي
            "en-GB-SoniaNeural",      # أنثى - سونيا (بريطانية)
            "en-GB-RyanNeural",       # ذكر - ريان (بريطانية)
            "en-GB-LibbyNeural",      # أنثى - ليببي (بريطانية)
            "en-AU-NatashaNeural",    # أنثى - ناتاشا (أسترالية)
            "en-AU-WilliamNeural",    # ذكر - ويليام (أسترالية)
            "en-CA-ClaraNeural",      # أنثى - كلارا (كندية)
            "en-CA-LiamNeural"        # ذكر - ليام (كندية)
        ],
        "الفرنسية 🇫🇷": [
            "fr-FR-DeniseNeural",     # أنثى - دينيس
            "fr-FR-HenriNeural",      # ذكر - هنري
            "fr-CA-SylvieNeural",     # أنثى - سيلفي (كندية)
            "fr-CA-AntoineNeural",    # ذكر - أنطوان (كندية)
            "fr-CH-ArianeNeural",     # أنثى - أريان (سويسرية)
            "fr-CH-FabriceNeural"     # ذكر - فابريس (سويسرية)
        ],
        "الإسبانية 🇪🇸": [
            "es-ES-ElviraNeural",     # أنثى - إلفيرا
            "es-ES-AlvaroNeural",     # ذكر - ألفارو
            "es-MX-DaliaNeural",      # أنثى - داليا (مكسيكية)
            "es-MX-LibertoNeural",    # ذكر - ليبرتو (مكسيكية)
            "es-AR-ElenaNeural",      # أنثى - إلينا (أرجنتينية)
            "es-AR-TomasNeural",      # ذكر - توماس (أرجنتينية)
            "es-CO-SalomeNeural",     # أنثى - سالومي (كولومبية)
            "es-CO-GonzaloNeural"     # ذكر - غونزالو (كولومبية)
        ]
    }

    # اختيار اللغة أولاً
    language_group = st.selectbox(
        "مجموعة اللغة:",
        list(voices.keys())
    )

    # ثم اختيار الصوت بناءً على اللغة المختارة
    voice = st.selectbox(
        "الصوت:",
        voices[language_group]
    )
    
    speed = st.slider("السرعة:", 0.5, 2.0, 1.0)

# زر التحويل
if st.button("▶️ تحويل إلى صوت", type="primary", use_container_width=True):
    if text and text.strip():
        with st.spinner("جاري تحويل النص إلى صوت... يرجى الانتظار"):
            try:
                # دالة التحويل
                async def generate_speech():
                    communicate = edge_tts.Communicate(text, voice, rate=f"+{int((speed-1)*100)}%")
                    audio_data = b""
                    
                    async for chunk in communicate.stream():
                        if chunk["type"] == "audio":
                            audio_data += chunk["data"]
                    
                    return audio_data
                
                # تنفيذ التحويل
                audio_bytes = asyncio.run(generate_speech())
                
                # عرض النتيجة
                st.success("✅ تم التحويل بنجاح!")
                
                # مشغل الصوت
                st.audio(audio_bytes, format="audio/mp3")
                
                # زر التحميل
                st.download_button(
                    label="📥 تحميل الملف الصوتي",
                    data=audio_bytes,
                    file_name="speech.mp3",
                    mime="audio/mpeg",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"❌ حدث خطأ: {str(e)}")
    else:
        st.warning("⚠️ يرجى إدخال النص أولاً")

# معلومات إضافية
st.write("---")
st.markdown("### ℹ️ معلومات:")
st.write("- **+30 صوت مختلف** بجودة عالية")
st.write("- يدعم اللهجات العربية المختلفة (مصر، الإمارات، قطر، الكويت)")
st.write("- أصوات إنجليزية بلهجات مختلفة (أمريكية، بريطانية، أسترالية، كندية)")
st.write("- الجودة عالية باستخدام تقنية Microsoft Neural Voices")
st.write("- يمكنك تحميل الملف الصوتي بصيغة MP3")