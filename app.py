import streamlit as st
import google.generativeai as genai

# =========================================================================
# بخش CSS و پس‌زمینه (برای زیبایی) - کد اصلاح شده
# =========================================================================

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

# ⚠️ تعریف آدرس پس‌زمینه (لینک شما بین " " قرار گرفت)
BACKGROUND_IMAGE_URL = "https://cdn.honarechehre.ir/images/f7f5c670-a23a-11ef-a046-2bbf2a900dfa.webp" 
set_background_style(BACKGROUND_IMAGE_URL)
# ----------------------------------------

# =========================================================================
# بخش اصلی برنامه Streamlit و منطق هوش مصنوعی
# =========================================================================

# --- 1. تنظیمات صفحه ---
st.set_page_config(page_title="برنامه هوش مصنوعی", page_icon="🤖", layout="centered")
st.title("🤖 برنامه هوش مصنوعی من")

# --- 2. بخش کلید (امنیت برای سرور) ---
try:
    # این خط برای وقتی است که برنامه روی اینترنت است (کلید از Secrets گرفته می‌شود)
    API_KEY = st.secrets["MY_GOOGLE_KEY"]
except:
    # این خط برای وقتی است که روی کامپیوتر خودتان هستید (کلید مستقیم استفاده می‌شود)
    API_KEY = "AIzaSyBsVv_hJ5F7u2fT760E9gY0NXpHrv8Sgbs" 

# --- 3. دستورات برنامه (Prompt) ---
# توجه: این دستور یک برنامه چت می‌سازد، نه یک برنامه کلیکی پرچم
GAME_INSTRUCTIONS = """شما یک دستیار چت هستید. به سوالات کاربر پاسخ دهید.
"""

# --- 4. تنظیم مدل ---
MODEL_NAME = 'gemini-2.5-flash'

# چک کردن کلید
if "AIzaSyBsVv_hJ5F7u2fT760E9gY0NXpHrv8Sgbs" == "AIzaSyBsVv_hJ5F7u2fT760E9gY0NXpHrv8Sgbs" or API_KEY == "":
    # این چک را حذف می‌کنیم تا هنگام استفاده از Secrets ارور ندهد
    pass

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

# --- 6. دریافت ورودی و ارسال به گوگل ---
if prompt := st.chat_input("پیام خود را بنویسید..."):
    # نمایش پیام کاربر
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # آماده‌سازی تاریخچه برای گوگل (تبدیل assistant به model)
    history_for_google = []
    for m in st.session_state.messages:
        role = m["role"]
        if role == "assistant":
            role = "model" # گوگل فقط model را می‌شناسد
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
