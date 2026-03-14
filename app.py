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

st.set_page_config(
    page_title="Forethought",
    layout="wide"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Montserrat', sans-serif !important;
    }
                      
    h1, h2, h3 {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700;
    }
     
    </style>
""", unsafe_allow_html=True)

st.sidebar.markdown("""<div style='text-align: center'>
        <h1>Forethought</h1>
        <p>Build your worldview from the ground up</p>
    </div>
""",unsafe_allow_html=True)