import streamlit as st
from pathlib import Path

def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()

st.set_page_config(page_title="ASR Survey", page_icon=":loudspeaker:")
st.title("Audio Super Resolution Survey")

intro_markdown = read_markdown_file("intro.md")
st.markdown(intro_markdown, unsafe_allow_html=True)

at_yes = "I DO NOT show signs of hearing loss "
at_no = "I DO show some signs of hearing loss "

at_result = st.radio(
    "Test result: ",
    (at_yes, at_no))

st.markdown('### Personal Information')

age = st.number_input('Age', value=18, step=1)

gender = st.selectbox(
    'Gender',
    ('Male', 'Female', 'Other'))

st.markdown('If you are exposed to multiple languages at a young age, list your First language as the one you feel more proficient in.')

lang1 = st.selectbox(
    'First language',
    ('English', 'Tagalog', 'Other'))

lang2 = st.selectbox(
    'Second language',
    ('Tagalog', 'English', 'Other'))

survey_markdown = read_markdown_file("survey.md")
st.markdown(survey_markdown, unsafe_allow_html=True)

audio_file = open('audio/input.wav', 'rb')
audio_bytes = audio_file.read()

st.audio(audio_bytes, format='audio/wav')

st.text_input('Enter the words spoken in the audio clip:', 'Text here', disabled=True)
st.slider('Rate the audio quality:', 1, 5, 3)
st.markdown('___')