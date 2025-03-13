import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser

###########################################################################################################
########################### Function for generating an answer using the LLM ###############################
###########################################################################################################
def generate_answer(re_written_query, relevant_chunks):
    ######################################### Define the LLM parameters #########################################
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        st.error("GROQ_API_KEY not found in environment variables.")
        return None

    model_name = "llama-3.3-70b-versatile"
    llm = ChatGroq(temperature=0.5, groq_api_key=groq_api_key, model_name=model_name)

    ########################################## Fetch the chat history ##########################################
    history = "\n".join([f"{message['role']}: {message['content']}" for message in st.session_state.messages])

    ############ Define the prompt and prompt template using Chain of Thought prompting technique ##############
    template = """
    <Instructions>
    
    - You are a customer-friendly chatbot designed to assist car users
      with any questions they have about their car by referring to the
      Toyota User Manual.
    - Provide clear and consice answers, and if necessary, explain the
      steps or details mentioned in the manual in bullet points.
    - If you don't the answer, then please apologize to the user and ask
      the user to contact customer support.
    - Always reply in a polite manner.
    
    </Instructions>
    
    <ChainOfThought>
    
    Consider the user's question,
    the relevant history of the conversation, and the context provided
    by the user manual. Use this information to generate a logical,
    coherent, and detailed response.
    
    </ChainOfThought>
    
    <Examples>
    
    Example 1:
    <UserQuestion> How do I adjust the seatbelt height in my Toyota Highlander? </UserQuestion>
    <History> User previously asked about seatbelt safety. </History>
    <Context> The manual explains the steps for adjusting the seatbelt height, including safety warnings. </Context>
    <Answer> To adjust the seatbelt height in your Toyota Highlander, press the release button and move the seatbelt anchor up or down until it clicks into place. Ensure that the shoulder belt is positioned across the center of your shoulder to maximize safety... </Answer>
    
    Example 2:
    <UserQuestion> What does the warning light with an exclamation mark mean? </UserQuestion>
    <History> No prior related questions. </History>
    <Context> The manual indicates that a warning light with an exclamation mark is related to the tire pressure monitoring system or other critical alerts. </Context>
    <Answer> The warning light with an exclamation mark in your Toyota Highlander typically indicates a tire pressure issue or another critical alert. It’s recommended to check your tire pressure and ensure they are properly inflated. If the issue persists, refer to the vehicle status section of your manual for further instructions... </Answer>
    
    </Examples>
    
    <Prompt>
    
    <UserQuestion> {question} </UserQuestion>
    <History> {history} </History>
    <Context> {context} </Context>
    
    </Prompt>
    
    <Answer>
    """
    prompt = ChatPromptTemplate.from_template(template)

    ####################################### Define the chain constructor ########################################
    chain = (RunnableParallel(
        {"question": RunnablePassthrough(),
         "history": RunnablePassthrough(),
         "context": RunnablePassthrough(),
         })
             | prompt
             | llm
             | StrOutputParser()
             )
             
    #################################### Generator an output using the chain ####################################
    with st.container(border=True):
        with st.chat_message('assistant'):
            message_placeholder = st.empty()
            all_results = ''
            with st.spinner('Generating answer...'):
                for res in chain.stream({"question": re_written_query,
                                         "history": history,
                                         "context": relevant_chunks}):
                    all_results += res
                    message_placeholder.markdown(all_results)

    #################################### Save the output in the session state ####################################
    st.session_state.messages.append({"role": "assistant", "content": all_results})

    return all_results