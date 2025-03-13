import os
import requests
import streamlit as st
from tempfile import NamedTemporaryFile
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import SKLearnVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

# Suppress warnings
import warnings

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ["TOKENIZERS_PARALLELISM"] = "false"

##############################################################################################################
################################### Function for retrieving the vector store ###################################
##############################################################################################################
def build_vector_store(content):
    if content:
        # If the vector store is not already present in the session state
        if not st.session_state.vector_store:

            with st.spinner(text=":red[Please wait while we fetch the information...]"):

                ################################# Fetch the embedding file ##################################
                embeddings = HuggingFaceEmbeddings()
                text_splitter = RecursiveCharacterTextSplitter(
                                                            chunk_size=800,
                                                            chunk_overlap=20,
                                                            length_function=len,
                                                            is_separator_regex=False,
                                                        )
                documents = text_splitter.create_documents(content)
                vector_store = Chroma.from_documents(documents, embeddings)

                ######################### Save the vector store to the session state ########################
                st.session_state.vector_store = vector_store
                return vector_store

        else:
            # Load the vector store from the cache
            return st.session_state.vector_store

    else:
        st.error('No content was found...')

##############################################################################################################
###################### Function for retrieving the relevant chunks from the vector store #####################
##############################################################################################################
def retrieve_chunks_from_vector_store(vector_store, re_written_query):

    ########################### Perform a similarity search with relevance scores ############################
    with st.spinner(text=":red[Please wait while we fetch the relevant information...]"):
        relevant_documents = vector_store.similarity_search_with_score(query=re_written_query, k=5)
        return relevant_documents

##############################################################################################################
################################### Function for retrieving the chat history #################################
##############################################################################################################
def retrieve_history():
    ############################## Go through all the chat messages in the history ###########################
    for message in st.session_state.messages:
        with st.container(border=True):
            with st.chat_message(message['role']):
                st.markdown(message['content'])