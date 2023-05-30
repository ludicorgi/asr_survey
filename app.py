import streamlit as st
from pathlib import Path
import random, datetime

# import gspread
from pandas import DataFrame
from gspread_pandas import Spread,Client
from google.oauth2 import service_account

def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()

def get_test_preset(preset):
    # TODO: change path depending on preset, first preset is already correct
    p = {
        '1b2q': ['audio/base/1','audio/quant/2'], 
        '1q2s': ['audio/base/1','audio/quant/2'], 
        '1s2b': ['audio/base/1','audio/quant/2'], 
        '3b4q': ['audio/base/1','audio/quant/2'], 
        '3q4s': ['audio/base/1','audio/quant/2'], 
        '3s4b': ['audio/base/1','audio/quant/2']
    }
    return p.get(preset, ['audio/base/1','audio/quant/2'])

def disable():
    st.session_state.disabled = True

# Spreadsheet Functions 
@st.cache_data()
# Get our worksheet names
def worksheet_names():
    sheet_names = []   
    for sheet in worksheet_list:
        sheet_names.append(sheet.title)  
    return sheet_names

# Get the sheet as dataframe
def load_the_spreadsheet(spreadsheetname):
    worksheet = sh.worksheet(spreadsheetname)
    df = DataFrame(worksheet.get_all_records())
    return df

# Update to Sheet
def update_the_spreadsheet(spreadsheetname,dataframe):
    col = ['preset','timestamp', 'name', 'email',  'age', 'gender', 'first_lang', 'second_lang', 'audt', 'words', 'ratings']
    spread.df_to_sheet(dataframe[col],sheet = spreadsheetname,index = False)

def record_response(preset, name, email, age, gender, lang1, lang2, audt, words, ratings):
    ts = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    df = load_the_spreadsheet('responses')
    
    opt = {'preset': preset,
            'timestamp': ts,
            'name': name,
            'email': email,
            'age': age,
            'gender': gender,
            'first_lang': lang1,
            'second_lang': lang2,
            'audt': audt,
            'words': words,
            'ratings': ratings} 
    
    opt_df = DataFrame(opt, index=[0])
    new_df = df.append(opt_df,ignore_index=True)
    update_the_spreadsheet('responses',new_df)



# Disable certificate verification (Not necessary always)
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Create a Google Authentication connection object
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"], scopes = scope)
client = Client(scope=scope,creds=credentials)
spreadsheetname = "asr-res"
spread = Spread(spreadsheetname,client = client)

sh = client.open(spreadsheetname)
worksheet_list = sh.worksheets()

st.set_page_config(page_title="ASR Survey", page_icon=":loudspeaker:")
st.title("Audio Super Resolution Survey")

# define preset list
preset_list = ['1b2q', '1q2s', '1s2b', '3b4q', '3q4s', '3s4b']

# preset selection
preset = random.choice(preset_list)
# TODO: let user choose a preset
st.write('Survey code: ' + preset)

intro_markdown = read_markdown_file("intro.md")
st.markdown(intro_markdown, unsafe_allow_html=True)

consent = st.checkbox("I understand and consent to being a participant in the study (Proceed with the survey)")
st.markdown('___')

### Personal Information
if consent:
    with st.form("asr-form"):
        st.markdown('### Personal Information')
        name = st.text_input('Full Name', placeholder="Name")
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
        
        md = read_markdown_file("audt.md")
        st.markdown(md, unsafe_allow_html=True)

        at_yes = "I DO NOT show signs of hearing loss "
        at_no = "I DO show some signs of hearing loss "

        audt = st.radio(
            "Test result: ",
            (at_yes, at_no))

        st.markdown('___')
        st.write('Survey code: ' + preset)

        survey_markdown = read_markdown_file("survey.md")
        st.markdown(survey_markdown, unsafe_allow_html=True)

        # TODO: change sample audio clip
        audio_file = open('audio/input.wav', 'rb')
        audio_bytes = audio_file.read()

        st.audio(audio_bytes, format='audio/wav')

        st.text_input('Enter the words spoken in the audio clip:', 'Text here', disabled=True)
        st.slider('Rate the audio quality from 1 to 5 (highest) :', 1, 5, 3, disabled=True)
        st.markdown('___')

        ### Audio Eval Test

        audio_bytes = []
        base_path = Path(get_test_preset(preset)[0])
        for wav_file_path in base_path.glob("*.wav"):
            audio_file = open(wav_file_path, 'rb')
            audio_bytes.append(audio_file.read())

        base_path = Path(get_test_preset(preset)[1])
        for wav_file_path in base_path.glob("*.wav"):
            audio_file = open(wav_file_path, 'rb')
            audio_bytes.append(audio_file.read())

        random.Random(1).shuffle(audio_bytes)
        # random.shuffle(audio_bytes)

        words = []
        ratings = []
        for i in range(20):
            st.markdown('#### ' + str(i+1) + '.')
            st.audio(audio_bytes[i], format='audio/wav')
            words.append(st.text_input(str(i) + '. Enter the words spoken in the audio clip:', placeholder="..."))
            ratings.append(st.slider(str(i) + '. Rate the audio quality from 1 to 5 :', 1, 5, 3))
            st.markdown('___')

        # st.markdown('#### 1.')
        # st.audio(audio_bytes, format='audio/wav')
        # ae_t1 = st.text_input('1. Enter the words spoken in the audio clip:', '')
        # ae_r1 = st.slider('1. Rate the audio quality from 1 to 5 (highest) :', 1, 5, 3)
        # st.markdown('___')

        st.markdown('By clicking the submit button, you agree to having your data collected for analysis. Please wait for cofirmation that your response has been submitted before exiting.')

        if "disabled" not in st.session_state:
            st.session_state.disabled = False

        submit_button = st.form_submit_button("Submit", on_click=disable, disabled=st.session_state.disabled)

        #TODO: disable until everything is filled
        if submit_button:
            # Check the connection
            # st.write(spread.url)
            # print(words)
            words = ','.join(words)
            ratings = ','.join(map(str, ratings))
            record_response(preset, name, email, age, gender, lang1, lang2, audt, words, ratings)
            st.info('Your response has been submitted. Thank you for participating. If you wish to contribute an additional response, refresh the page.')