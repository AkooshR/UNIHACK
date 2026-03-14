import functions as functions
import streamlit as st
import anthropic
from dotenv import load_dotenv
from pathlib import Path
import os
import pandas as pd
import json

system_prompt = """You are staging a formal debate between two real historical figures. 

Rules:
- Voice each speaker authentically, grounded in their documented writings and philosophy
- Each speaker must argue from their actual worldview — do not invent positions they never held
- Stay in character throughout. Do not break the fourth wall or explain what you are doing
- The debate should be intellectually rigorous but accessible
- Each speaker should directly challenge the other's points, not just monologue"""

# Sets three variables to store throughout the app's usage: the stage we are in, the dataframe outputted by claude, the topic that the user inputs.
# Three stages: "topic", "figure selection", "debate"
if "stage" not in st.session_state:
    st.session_state.stage = "topic"
if "df" not in st.session_state:
    st.session_state.df = None
if "topic" not in st.session_state:
    st.session_state.topic = ""

st.title("Forethought")
st.subheader("Build your worldview from the ground up. Study. Debate. Grow.")

if st.session_state.stage == "topic":
    st.write("Enter a contentious topic to explore ... ")
    topic_input = st.text_input("Topic", placeholder="E.g. Do people truly have free will, or is fate predetermined?")
    if st.button("Dive In"):
        if topic_input.strip() == "":
            st.warning("Please enter a topic first.")
        else:
            st.spinner("Finding the best thinkers ...")
            df = functions.get_call1(topic_input)
            st.dataframe(df)

            st.session_state.topic = topic_input
            st.session_state.df = df
            st.session_state.stage = "figure selection"