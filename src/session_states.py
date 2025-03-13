import streamlit as st

##############################################################################################################
############################ Function for initializing the session states ####################################
##############################################################################################################
def initialize_params():
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    if 'vector_store' not in st.session_state:
        st.session_state.vector_store = None