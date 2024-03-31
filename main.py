import os
import time
import streamlit as st
import vertexai
from youtube_transcript_api import YouTubeTranscriptApi
from vertexai.generative_models import GenerativeModel, Part
from tts import Generate
# from dotenv import load_dotenv

# load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./audio-recognizer-418819-098598b73935.json"
status_msg = ""

def start():
    st.title("Select your video")

    # submit the URL that the user inputs into the text field
    st.session_state["url"] = st.text_input("YouTube URL")
    if st.button(label="Submit URL"):

        st.session_state["url_is_valid"] = submit_url(st.session_state["url"])
        if st.session_state["url_is_valid"]:
            st.write("URL is valid")
        else:
            st.write("URL is invalid")

    # generate the response to the question the user asked and display it
    question = st.text_input("What's your question?")

    if st.button(label="Submit Question"):
        if st.session_state.get("url_is_valid") is not None:
            answer = prompt(question, st.session_state['transcript'])
            vocal_filename = Generate(st.session_state["url"], answer)
            # st.audio()
            st.subheader("Response")
            st.write(answer)
        else:
            print("No answer generated since URL is invalid")

    vocalize(vocal_filename)

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


def prompt(question: str, transcript: str) -> str:
    """Prompt the generative AI model with the question and return the response"""
    vertexai.init(project="audio-recognizer-418819")
    model = GenerativeModel("gemini-1.0-pro")

    #create the prompt
    prompt_message = """
    Answer the question only using the transcript of the video given:

    ## Question:
    {question}
    ## Video Transcript:
    {transcript}
    """.format(question=question, transcript=transcript)

    #generate and return the response to the prompt
    response = model.generate_content(prompt_message)
    return response.text


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


# start the program
start()
