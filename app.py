# --- کد CSS برای افزودن پس زمینه به کل صفحه ---
def set_background_style(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ⚠️ اینجا آدرس عکس خود را جایگزین کنید:
BACKGROUND_IMAGE_URL = "img1.taw-bio.ir/2024/229313/1klrk2v8.jpeg" 
# یک آدرس تصویر مناسب بگذارید
set_background_style(https://cdn.honarechehre.ir/images/f7f5c670-a23a-11ef-a046-2bbf2a900dfa.webp)
# ----------------------------------------import streamlit as st
import google.generativeai as genai

# --- 1. تنظیمات صفحه ---
st.set_page_config(page_title="برنامه هوش مصنوعی", page_icon="🤖", layout="centered")
st.title("🤖 برنامه هوش مصنوعی من")

# --- 2. کلید خود را اینجا وارد کنید ---
# --- دریافت کلید (امنیت برای سرور) ---
try:
    # این خط برای وقتی است که برنامه روی اینترنت است
    API_KEY = st.secrets["MY_GOOGLE_KEY"]
except:
    # این خط برای وقتی است که روی کامپیوتر خودتان هستید
    API_KEY = "AIzaSyBsVv_hJ5F7u2fT760E9gY0NXpHrv8Sgbs"
# --- 3. دستورات برنامه (Prompt) ---
GAME_INSTRUCTIONS = """یک برنامه واسم بساز .. تا وقتی من روی کلمه ایران کلیلک کنم عکس پرچم ایران بیاد ... وقتی روی کلمه ترکیه بزنم عکس پرچم ترکیه بیاد
"""

# --- 4. تنظیم مدل (مدل 2.5 فلش که برای شما فعال بود) ---
MODEL_NAME = 'gemini-2.5-flash'

# چک کردن کلید
if API_KEY == "کلید_خود_را_اینجا_پیست_کنید" or API_KEY == "":
    st.error("⛔ لطفا کلید API را در خط 9 وارد کنید!")
    st.stop()

# اتصال به گوگل
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(MODEL_NAME, system_instruction=GAME_INSTRUCTIONS)
except Exception as e:
    st.error(f"خطا در اتصال: {e}")
    st.stop()

# --- 5. حافظه چت ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    # پیام اولیه
    st.session_state.messages.append({"role": "assistant", "content": "سلام! من در خدمتم."})

# نمایش پیام‌های قبلی در صفحه
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. دریافت ورودی و حل مشکل ارور 400 ---
if prompt := st.chat_input("پیام خود را بنویسید..."):
    # نمایش پیام کاربر
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # آماده‌سازی تاریخچه برای گوگل (تبدیل assistant به model)
    history_for_google = []
    for m in st.session_state.messages:
        role = m["role"]
        if role == "assistant":
            role = "model"  # گوگل فقط model را می‌شناسد
        history_for_google.append({"role": role, "parts": [m["content"]]})

    # دریافت پاسخ
    with st.chat_message("assistant"):
        with st.spinner("در حال نوشتن..."):
            try:
                chat = model.start_chat(history=history_for_google)
                response = chat.send_message(prompt)
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:

                st.error(f"خطا: {e}")

