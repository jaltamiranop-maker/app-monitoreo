import streamlit as st

def init_state():
    if "resultado" not in st.session_state:
        st.session_state.resultado = None