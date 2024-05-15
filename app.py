import streamlit as st
from chatbot import run_app
from auth import authenticate

st.set_page_config(layout="wide", page_title="chatbot")

authenticate(run_app)