import streamlit as st
from src.session_states import initialize_params

# Set the Streamlit page parameters
st.set_page_config(layout="wide",
                   initial_sidebar_state='expanded',
                   page_icon="👻",
                   page_title='GPT Document Analyzer')

##############################################################################################################
############################# Function for displaying the introduction page ##################################
##############################################################################################################
def display_intro():
    #################################### Section 1 => Text / Information #####################################
    col_left, col_right = st.columns(2)

    with col_left:
        st.title(":rainbow[TOYOTA USER MANUAL]")
        st.write('')
        st.subheader(":grey[Got questions about the Toyota Highlander?]")
        st.write(":grey[Interact with our chatbot by using the side menu...]")

    with col_right:
        image_path = "./images/toyota_logo.png"
        st.image(image_path, use_column_width=True)

    ###################################### Section 2 => Image and video #######################################
    col_left, col_right = st.columns([0.45, 0.55])

    with col_left:
        video_path = "https://www.youtube.com/watch?v=N-EQ_08Ptu4"
        st.video(video_path)

    with col_right:
        image_path = "./images/Toyota_1.jpg"
        st.image(image_path, use_column_width=True)

initialize_params()
display_intro()
