import streamlit as st
from faster_whisper import WhisperModel
import tempfile

st.set_page_config(page_title="Whisper Transcriber", layout="centered")
st.title("🎙️ Transcrição de Áudio com Faster Whisper")

uploaded_file = st.file_uploader("Envie um arquivo de áudio", type=["mp3", "wav", "m4a"])
language = st.selectbox("Escolha o idioma do áudio", ["pt", "en", "es", "fr", "de", "auto"])

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')

    if st.button("Transcrever"):
        with st.spinner("Transcrevendo com Faster Whisper..."):
            # Salva o arquivo temporariamente
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                tmp_file.write(uploaded_file.read())
                audio_path = tmp_file.name

            # Carrega o modelo (use "base" ou "small" se quiser mais rápido)
            model = WhisperModel("base", compute_type="int8")

            segments, info = model.transcribe(audio_path, language=None if language == "auto" else language)

            # Junta os trechos transcritos
            full_text = " ".join([segment.text for segment in segments])

            st.success("Transcrição completa!")
            st.text_area("Texto transcrito:", full_text, height=300)
