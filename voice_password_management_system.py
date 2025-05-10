import streamlit as st
import speech_recognition as sr

st.title("🔐 Voice Password Management System")

if "voice_password" not in st.session_state:
    st.session_state.voice_password = None
if "password_set" not in st.session_state:
    st.session_state.password_set = False
if "message" not in st.session_state:
    st.session_state.message = ""

def record_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🎧 Adjusting for background noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        st.write("🎤 Recording... Speak now.")
        audio = recognizer.listen(source, phrase_time_limit=5)
        st.write("📝 Transcribing...")
        try:
            return recognizer.recognize_google(audio).lower().strip()
        except sr.UnknownValueError:
            st.warning("⚠️ Could not understand the audio.")
            return None
        except sr.RequestError:
            st.error("❌ Could not connect to recognition service.")
            return None

if not st.session_state.password_set:
    if st.button("Set Password"):
        st.write("🔐 Speak your new password...")
        text = record_voice()
        if text:
            st.session_state.voice_password = text
            st.session_state.password_set = True
            st.success("✅ Password set successfully.")
            st.session_state.message = f"Saved Password: '{text}'"  # for demo

if st.session_state.password_set:
    if st.button("Change Password"):
        st.write("🔑 Please speak your current password...")
        current = record_voice()
        if current and current == st.session_state.voice_password:
            st.success("🔓 Verified. Now speak your new password...")
            new_pass = record_voice()
            if new_pass:
                st.session_state.voice_password = new_pass
                st.success("✅ Password changed successfully.")
                st.session_state.message = f"New Password: '{new_pass}'"
        else:
            st.error("❌ Incorrect password. Access denied.")

if st.session_state.password_set:
    if st.button("Forgot Password"):
        st.session_state.voice_password = None
        st.session_state.password_set = False
        st.success("🔁 Password reset. Please set a new password.")
        st.session_state.message = "Password has been reset."
