import os
import streamlit as st
import pandas as np
import numpy as np
import vertexai
from youtube_transcript_api import YouTubeTranscriptApi
from vertexai.generative_models import GenerativeModel, Part
# from dotenv import load_dotenv

# load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\rk4li\Documents\GenAI Genesis\audio-response\audio-recognizer-418819-098598b73935.json"
is_found = False
status_msg = ""
#TODO store transcript into a txt file

#TODO complete function
def load_transcript(url: str) -> str:
    """Attempt to load the transcript of the video; returns true is found
    and false otherwise"""
    id = url.split("=")
    result = YouTubeTranscriptApi.get_transcript(id[1])
    text = ""
    for i in result:
        text += " " + i["text"]
    return text
def prompt(question: str, text: str) -> str:
    """Prompt the generative AI model with the question and return the response"""
    vertexai.init(project="audio-recognizer-418819")
    model = GenerativeModel("gemini-1.0-pro")
    prompt_message = """
    Answer the question only using the transcript of the video given:

    ## Question:
    {question}
    ## Video Transcript:
    {text}
""".format(question=question, text=text)
    response = model.generate_content(prompt_message)
    return response
    pass


st.title("Select your video")
url = st.text_input("YouTube URL")
if st.button(label="Submit URL"):
    text = load_transcript(url)
    st.session_state['text'] = text
    st.write("Status: " + text)

question = st.text_input("What's your question?")
if st.button(label="Submit Question"):
    answer = prompt(question, st.session_state['text'])
    print(answer)
    st.write("Status: " + answer.text)


st.write("Your Video: " + url)

#Find the video
# is_found = load_transcript(url)
# if is_found:
#     status_msg = "Found"
# else:
#     status_msg = "Not Found"



st.subheader("Response")

#response = prompt(question)
response = "insert response here"
st.write(response)



#TODO make it so multiple videos can be searched when AI searches for an answer to a question
# col1, col2, col3 = st.columns(3)
#
# with col1:
#     st.header("Video 1")
#
# with col2:
#     st.header("Video 2")