import requests
import streamlit as st
import os
from tempfile import NamedTemporaryFile
from langchain_community.document_loaders import PyPDFLoader

####################### Function for loading and caching the content of the PDF file #######################
@st.cache_data
def load_pdf_content(user_manual_path):
    # Load the PDF content using PyPDFLoader
    pdf_loader = PyPDFLoader(user_manual_path)
    pdf_reader = pdf_loader.load()
    
    # Extract and format the content
    content = [(page.page_content.replace('\n', '\n\n')
                if page.page_content else '...') for page in pdf_reader]
    return content

###########################################################################################################
########################### Function for displaying the PDF file and the images ###########################
###########################################################################################################
def load_file():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    user_manual_path = os.path.normpath(os.path.join(current_dir, '../data/Toyota-Highlander-2024.pdf'))

    print("PDF path:", user_manual_path)
    
    with st.spinner('Loading PDF content. Please wait around a minute...'):
        content = load_pdf_content(user_manual_path)

    if content:
        with st.container(height=600, border=False):
            col_left, col_right = st.columns(2)

            ###################################### Display the images #####################################
            with col_left:
                image_path = os.path.normpath(os.path.join(current_dir, "../images/Toyota_3.jpg"))
                st.image(image_path, use_column_width=True)

                image_path = os.path.normpath(os.path.join(current_dir, "../images/Toyota_4.jpg"))
                st.image(image_path, use_column_width=True)

            with col_right:
                image_path = os.path.normpath(os.path.join(current_dir, "../images/Toyota_5.jpg"))
                st.image(image_path, use_column_width=True)

                image_path = os.path.normpath(os.path.join(current_dir, "../images/Toyota_6.jpg"))
                st.image(image_path, use_column_width=True)

        return content
    else:
        st.error('User Manual not found')
        return None