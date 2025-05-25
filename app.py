import streamlit as st
import whisper
import tempfile

st.set_page_config(page_title="Whisper Transcriber", layout="centered")
st.title("🎙️ Transcrição de Áudio com Whisper")

uploaded_file = st.file_uploader("Envie um arquivo de áudio", type=["mp3", "wav", "m4a"])
language = st.selectbox("Escolha o idioma do áudio", ["pt", "en", "es", "fr", "de", "auto"])

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')

    if st.button("Transcrever"):
        with st.spinner("Transcrevendo com Whisper..."):
            model = whisper.load_model("base")

            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            options = {} if language == "auto" else {"language": language}
            result = model.transcribe(tmp_path, **options)
            st.success("Transcrição completa!")
            st.text_area("Texto transcrito:", result["text"], height=300)