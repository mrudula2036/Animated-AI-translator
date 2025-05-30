import streamlit as st
import os
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS

# File to save translations
TRANSLATION_FILE = "translations.txt"

# AI Assistant Video File (Ensure you have an assistant video)
ASSISTANT_VIDEO_PATH = "girl.gif.mp4"

def save_translation(original, translated, src_lang, tgt_lang):
    """Save translations to a file"""
    with open(TRANSLATION_FILE, "a", encoding="utf-8") as file:
        file.write(f"{src_lang} -> {tgt_lang} | {original} => {translated}\n")

def load_translation_history():
    """Load translation history with newest entries on top"""
    if os.path.exists(TRANSLATION_FILE):
        with open(TRANSLATION_FILE, "r", encoding="utf-8") as file:
            history = file.readlines()
            return history[::-1]  # Reverse list to show newest entries first
    return []

def speech_to_text():
    """Convert speech to text"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            st.error("❌ Could not understand the speech.")
        except sr.RequestError:
            st.error("❌ Network error. Check your connection.")
        except sr.WaitTimeoutError:
            st.error("❌ No speech detected. Try again.")
    return None

def text_to_speech(text, language):
    """Convert text to speech and play AI Assistant Video"""
    tts = gTTS(text, lang=language)
    audio_file = "output.mp3"
    tts.save(audio_file)

    # Show AI Assistant Video while speaking
    col1, col2 = st.columns([3, 1])  # AI Assistant on the right side
    with col2:
        st.video(ASSISTANT_VIDEO_PATH)  # Play the AI Assistant Video

    # Play Audio
    st.audio(audio_file, format="audio/mp3")

def translate_text(text, target_lang):
    """Translate text using Google Translator"""
    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        save_translation(text, translated, "auto-detected", target_lang)
        return translated
    except Exception as e:
        st.error(f"❌ Translation Error: {e}")
        return None

# Streamlit UI
st.set_page_config(page_title="AI Translator with Talking Assistant", layout="centered")

st.title("🌍 AI Speech & Text Translator with Talking Assistant")
st.write("Translate text or speech into multiple languages with a talking AI assistant.")

# Sidebar for Translation History (Newest First)
with st.sidebar:
    if st.button("📜 Show Translation History"):
        history = load_translation_history()
        if history:
            st.write("\n".join(history[:5]))  # Show latest 5 translations
        else:
            st.write("No history available.")

# Translation Feature
st.subheader("🔠 Translation")
input_method = st.radio("Choose input method:", ["📝 Type Text", "🎤 Speak"])

text = None
if input_method == "📝 Type Text":
    text = st.text_area("Enter text to translate:")
    if text:
                target_lang = st.selectbox("Choose target language:", ["en", "hi", "kn"])
                
                if st.button("Translate & Speak"):
                    translated_text = translate_text(text, target_lang)
                    if translated_text:
                        st.success(f"✅ *Translated Text ({target_lang}):* {translated_text}")
                        text_to_speech(translated_text, target_lang)

elif input_method == "🎤 Speak":
    if st.button("Start Speaking"):
        recognized_text = speech_to_text()
        if recognized_text:
            st.session_state['recognized_text'] = recognized_text

    # Display recognized text if available
    if 'recognized_text' in st.session_state:
        text = st.session_state['recognized_text']
        st.write(f"📝 *Recognized Speech:* {text}")

        target_lang = st.selectbox("Choose target language:", ["en", "hi", "kn"])

        if st.button("Translate & Speak"):
            translated_text = translate_text(text, target_lang)
            if translated_text:
                st.success(f"✅ *Translated Text ({target_lang}):* {translated_text}")
                text_to_speech(translated_text, target_lang)

