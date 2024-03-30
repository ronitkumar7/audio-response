import streamlit as st
import pandas as np
import numpy as np

is_found = False
status_msg = ""
#TODO store transcript into a txt file

st.title("Select your video")
url = st.text_input("YouTube URL")

question = st.text_input("What's your question?")

st.write("Your Video: " + url)

#Find the video
# is_found = load_transcript(url)
if is_found:
    status_msg = "Found"
else:
    status_msg = "Not Found"

st.write("Status: " + status_msg)

st.subheader("Response")

#response = prompt(question)
response = "insert response here"
st.write(response)

#TODO complete function
def load_transcript(url: str) -> bool:
    """Attempt to load the transcript of the video; returns true is found
    and false otherwise"""
    pass

def prompt(question: str) -> str:
    """Prompt the generative AI model with the question and return the response"""
    pass

#TODO make it so multiple videos can be searched when AI searches for an answer to a question
# col1, col2, col3 = st.columns(3)
#
# with col1:
#     st.header("Video 1")
#
# with col2:
#     st.header("Video 2")