import streamlit as st
from src.load_file import load_file
from src.rewrite_query import rewrite_user_query
from src.retriever import build_vector_store, retrieve_chunks_from_vector_store, retrieve_history
from src.generator import generate_answer

# Load the user manual file
user_manual_content = load_file()

# If load is successful
if user_manual_content:
    try:
        ###################################### Display the title ######################################
        st.title(":rainbow[TOYOTA HIGHLANDER INTERACTIVE BOT]")
        st.write('')

        ####################### Set a clear conversation button on the side menu ######################
        clear_conversation = st.sidebar.button(label='Clear conversation',
                                               key='clear_conversation',
                                               use_container_width=True)

        if clear_conversation:
            st.session_state.messages = []

        ############################### Display the chatbot input space ###############################
        user_input = st.chat_input(
            'Ask me a question about the Toyota Highlander...',
            max_chars=1500,
            key='user_input')

        ######################### Build the vector store to store the vectors #########################
        vector_store = build_vector_store(user_manual_content)

        ######################### Check and display any previous chat history #########################
        history = retrieve_history()

        if user_input:
            ############################ Append the user input to the chat ############################
            st.session_state.messages.append({"role": "user", "content": user_input})

            #################### Rewrite the user query for better input to the LLM ###################
            re_written_query = rewrite_user_query(user_input)

            ###################### Retrieve the relevant chunks from the database #####################
            relevant_chunks = retrieve_chunks_from_vector_store(vector_store, re_written_query)

            ######################### Generate a final answer using the LLM ##########################
            answer = generate_answer(re_written_query, relevant_chunks)

            ##################### Display the answer with the relevant information ####################
            col_left, col_right = st.columns(2)

            with col_left:
                with st.expander(label='Re-written user query', expanded=False):
                    st.write(re_written_query)

            with col_right:
                with st.expander(label='Retrieved relevant text from the car user manual', expanded=False):
                    st.write(relevant_chunks)

    # Handle the exception if the user manual is not loaded
    except Exception as e:
        print(e)
        st.error("Sorry, an error occurred.")