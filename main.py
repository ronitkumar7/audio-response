import os
import time
import streamlit as st
import vertexai
from youtube_transcript_api import YouTubeTranscriptApi
from vertexai.generative_models import GenerativeModel, Part
from voice_code.tts import Generate
# from dotenv import load_dotenv

EASY = 0
HARD = 1

# load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./audio-recognizer-418819-098598b73935.json"
status_msg = ""

def start():
    #initialize variables for the first time
    if st.session_state.get("submit_pressed") is None:
        st.session_state["submit_pressed"] = False

    #Title and formatting

    #Credit: https://stackoverflow.com/questions/77377439/how-to-change-font-size-in-streamlit
    titlename = "Your personal professor"
    st.markdown("""
    <style>
    .big-font {
        font-size:100px;
        font-weight: 500;
        font-family: sans-serif, serif;
        line-height: 100%
    }
    </style>
    """, unsafe_allow_html=True)

    st.sidebar.title("")
    st.sidebar.title("")
    st.sidebar.title("")
    st.sidebar.markdown(f'<p class="big-font">{titlename}</p>'.format(titlename), unsafe_allow_html=True)

    st.title("")
    st.title("")
    st.title("")

    # submit the URL that the user inputs into the text field
    st.session_state["url"] = st.text_input("YouTube URL")
    if st.button(label="Submit URL"):

        st.session_state["url_is_valid"] = submit_url(st.session_state["url"])
        if st.session_state["url_is_valid"]:
            st.write("URL is valid")
        else:
            st.write("URL is invalid")

    # generate the textual response to the question the user asked and display it
    question = st.text_input("What's your question?")

    # difficulty setting for explanation
    level = st.radio("explain it like ...", ["I'm an expert", "I'm five"], horizontal=True)

    if st.button(label="Submit Question"):
        if st.session_state.get("submit_pressed") is False and st.session_state.get("url_is_valid") is not None:
            st.session_state["submit_pressed"] = True

            if level == "I'm an expert":
                st.session_state["level"] = HARD
            else:
                st.session_state["level"] = EASY

            answer = prompt(question, st.session_state.get('transcript'), st.session_state["level"])

            # Generate the voice version of the response and display it
            display_voice(answer)
        else:
            print("No answer generated since URL is invalid")
    st.session_state["submit_pressed"] = False


def load_transcript(url: str) -> str:
    """Attempt to load the transcript of the video; returns the transcript if found
    and None otherwise"""
    split_url = url.split("=", 1)

    #error: invalid URL
    if len(split_url) < 2:
        print("Error: Invalid URL")
        return None
    else:
        script_segments = YouTubeTranscriptApi.get_transcript(split_url[1])
        print(split_url)

        #build and return the transcript
        transcript = ""
        for segment in script_segments:
            transcript += " " + segment['text']
        return transcript


def prompt(question: str, transcript: str, level: int) -> str:
    """Prompt the generative AI model with the question and return the response"""
    vertexai.init(project="audio-recognizer-418819")
    model = GenerativeModel("gemini-1.0-pro")

    #Enable/disable the 'explain it like I'm 5' prompt
    if level == EASY:
        easy_prompt = "The first thing you say should always be an analogy of the problem in " \
                      "terms of situations or objects encountered in everyday life. " \
                      "Explain it to me in simple terms without mentioning that you are "\
                      "explaining it to me in simple terms"
    else:
        easy_prompt = ""

    #create the prompt
    prompt_message = """
    You are the speaker in this video. Answer the question below only using the transcript of 
    the video given. {easy_prompt}. Respond to me as if you are the person speaking in the video:

    ## Question:
    {question}
    ## Video Transcript:
    {transcript}
    """.format(easy_prompt=easy_prompt, question=question, transcript=transcript)

    #generate and return the response to the prompt
    try:
        response = model.generate_content(prompt_message)
        return response.text
    except:
        print("Too many requests")


def submit_url(url: str):
    """Return True if a valid URL has been submitted, and false otherwise"""
    # Error handling: Invalid URL
    try:
        transcript = load_transcript(url)
        # Error handling: no "=" character or otherwise empty transcript
        print(transcript)
        if transcript is None:
            print("Error: No transcript loaded")
            return False
        else:
            st.session_state['transcript'] = transcript
            return True
    except:
        print("Error: No transcript found")
        return False


#TODO implement
def vocalize(file_path: str):
    """Play the voice of the speaker in the video answering the
    quesiton posed by the user"""

    # play the audio file
    if os.path.isfile(file_path):
        print("file exists")
        audio_file = open(file_path, "rb")
        audio_bytes = audio_file.read()

        st.audio(audio_bytes, format="audio/wav")
    else:
        print("Error: file at " + file_path + " is not a file")

def display_voice(answer):
    """Generate the voice component on screen"""
    if st.session_state.get('transcript') is not None:
        vocal_filename = Generate(st.session_state["url"], answer)
        st.subheader("Response")
        st.write(answer)
        vocalize(vocal_filename)
    else:
        print("Error: Transcript has not been loaded")


# start the program
start()
