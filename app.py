import functions as functions
import streamlit as st
import anthropic
from dotenv import load_dotenv
from pathlib import Path
import os
import pandas as pd
import json


# Sets three variables to store throughout the app's usage: the stage we are in, the dataframe outputted by claude, the topic that the user inputs.
# Three stages: "topic", "figure selection", "debate"
if "stage" not in st.session_state:
    st.session_state.stage = "topic"
if "df" not in st.session_state:
    st.session_state.df = None
if "topic" not in st.session_state:
    st.session_state.topic = ""
if "page" not in st.session_state:
    st.session_state.page = "Debate Room"
if "selected" not in st.session_state:
    st.session_state.selected = []
if "debate" not in st.session_state:
    st.session_state.debate = ""

# Configuring the page and sidebar

st.set_page_config(
    page_title="Forethought",
    layout="wide"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');
    @import url('https://fonts.googleapis.com/icon?family=Material+Icons');
    
    * {
        font-family: 'Montserrat', sans-serif !important;
    }
    
    [data-testid="stIconMaterial"] {
        font-family: 'Material Icons' !important;
    }
    
    h1, h2, h3 {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700;
        color: #C8A96E;
    }

    [data-testid="stSidebarContent"] .stButton > button {
        background: none !important;
        border: none !important;
        box-shadow: none !important;
    }

    [data-testid="stSidebarContent"] .stButton > button:focus {
        box-shadow: none !important;
        outline: none !important;
    }
    </style>
""", unsafe_allow_html=True)

st.sidebar.markdown("""<div style='text-align: center'>
        <h1>Forethought</h1>
    </div>
""",unsafe_allow_html=True)
st.sidebar.markdown("<div style='margin-bottom: 2rem'></div>", unsafe_allow_html=True)
st.sidebar.button("Debate Room", use_container_width = True)
st.sidebar.button("Essentials", use_container_width = True)

# Configure the Debate Room

def show_debate_room():
    st.markdown("<h1 style='text-align: center'>Debate Room</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 0.9rem'>Enter a contentious topic to explore</p>", unsafe_allow_html=True)
    
    topic_input = st.text_area("", placeholder="E.g. Do people truly have free will, or is fate predetermined?", height=120)
    col1, col2 = st.columns([1, 4])
    dive_in = col1.button("Dive In", use_container_width=True)
    if dive_in:
        if topic_input.strip() == "":
            st.warning("Please enter a topic first.")
        else:
            with st.spinner("Finding the best thinkers..."):
                df = functions.get_call1(topic_input)
                st.session_state.topic = topic_input
                st.session_state.df = df
                st.session_state.stage = "figure selection"
                st.rerun()

def show_figure_selection():
    st.markdown("<h1 style='text-align: center'>Debate Room</h1>", unsafe_allow_html=True)
    st.text_area("Topic",placeholder=st.session_state.topic, height="content", disabled=True)
    st.markdown("<p style='text-align: center; font-size: 1.0rem'>Contestants</p>", unsafe_allow_html=True)
    for i, row in st.session_state.df.iterrows():
        with st.expander(f'{i+1} {row['name']}'):
            st.markdown(f"**Era:** {row['era']}")
            st.markdown(f"**Stance:** {row['known_stance']}")
            st.checkbox('Select', key=i+1)
    debate_button = st.button("Start Debate")
    if debate_button:
        st.session_state.selected = [(i-1) for i in range(1,6) if st.session_state.get(i)]
        if len(st.session_state.selected) != 2:
            st.warning("Please select exactly 2 people.")
        else:
            with st.spinner("Generating debate..."):
                st.session_state.debate = functions.get_call2(st.session_state.selected[0],st.session_state.selected[1],st.session_state.topic,st.session_state.df)
                st.session_state.stage = "debate"
            st.rerun()
                
def show_debate():
    st.markdown("<h1 style='text-align: center'>Debate Room</h1>", unsafe_allow_html=True)
    st.text_area("Topic",placeholder=st.session_state.topic, height="content", disabled=True)
    st.markdown("<p style='text-align: center; font-size: 1.0rem'>Contestants</p>", unsafe_allow_html=True)
    for i in st.session_state.selected:
        with st.expander(st.session_state.df.loc[i,'name']):
            st.markdown(f"**Era:** {st.session_state.df.loc[i,'era']}")
            st.markdown(f"**Stance:** {st.session_state.df.loc[i,'known_stance']}")
    st.write(st.session_state.debate)

if st.session_state.page == "Debate Room" and st.session_state.stage == "topic":
    show_debate_room()
elif st.session_state.page == "Debate Room" and st.session_state.stage == "figure selection":
    show_figure_selection()
elif st.session_state.page == "Debate Room" and st.session_state.stage == "debate":
    show_debate()