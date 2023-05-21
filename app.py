import streamlit as st
from pathlib import Path
import random
import gspread
from google.oauth2 import service_account

def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()

def get_test_preset():
    # TODO: logic for selecting random test preset
    pass

def disable():
    st.session_state.disabled = True

st.set_page_config(page_title="ASR Survey", page_icon=":loudspeaker:")
st.title("Audio Super Resolution Survey")

intro_markdown = read_markdown_file("intro.md")
st.markdown(intro_markdown, unsafe_allow_html=True)

consent = st.checkbox("I understand and consent to being a participant in the study")

if consent:
    md = read_markdown_file("audt.md")
    st.markdown(md, unsafe_allow_html=True)

    at_yes = "I DO NOT show signs of hearing loss "
    at_no = "I DO show some signs of hearing loss "

    at_result = st.radio(
        "Test result: ",
        (at_yes, at_no))

    ### Personal Information
    st.markdown('### Personal Information')

    name = st.text_input('Name', placeholder="Name")
    email = st.text_input('Email', placeholder='example@gmail.com')
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
    st.slider('Rate the audio quality from 1 to 5 (highest) :', 1, 5, 3)
    st.markdown('___')

    ### Audio Eval Test

    # preset selection
    audio_bytes = []
    base_path = Path("audio/base/preset1")
    for wav_file_path in base_path.glob("*.wav"):
        audio_file = open(wav_file_path, 'rb')
        audio_bytes.append(audio_file.read())

    base_path = Path("audio/quant/preset1")
    for wav_file_path in base_path.glob("*.wav"):
        audio_file = open(wav_file_path, 'rb')
        audio_bytes.append(audio_file.read())

    random.Random(1).shuffle(audio_bytes)
    # random.shuffle(audio_bytes)

    for i in range(20):
        # TODO: variables to record participant answers
        st.markdown('#### ' + str(i+1) + '.')
        st.audio(audio_bytes[i], format='audio/wav')
        st.text_input(str(i) + '. Enter the words spoken in the audio clip:', placeholder="...")
        st.slider(str(i) + '. Rate the audio quality from 1 to 5 :', 1, 5, 3)
        st.markdown('___')

    # st.markdown('#### 1.')
    # st.audio(audio_bytes, format='audio/wav')
    # ae_t1 = st.text_input('1. Enter the words spoken in the audio clip:', '')
    # ae_r1 = st.slider('1. Rate the audio quality from 1 to 5 (highest) :', 1, 5, 3)
    # st.markdown('___')

    st.markdown('By clicking the submit button, you agree to having your data collected for analysis')

    if "disabled" not in st.session_state:
        st.session_state.disabled = False

    submit_button = st.button("Submit", on_click=disable, disabled=st.session_state.disabled)

    if submit_button:
        st.info('Your response has been submitted. Thank you for participating.')