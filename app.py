import streamlit as st

st.set_page_config(page_title="ASR Survey", page_icon=":loudspeaker:")
st.title("Audio Super Resolution Survey")
st.write("Developed by Raynier Chua, Ivan Lim and Paolo Lojo")

audio_file = open('audio/input.wav', 'rb')
audio_bytes = audio_file.read()

st.audio(audio_bytes, format='audio/wav')