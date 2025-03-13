import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

##############################################################################################################
################################### Function for rewriting the user query ####################################
##############################################################################################################
def rewrite_user_query(user_query):

    ################################### Write down the original user query ###################################
    with st.container(border=True):
        st.markdown(user_query)

    ####################################### Define the LLM parameters #######################################
    # groq_api_key = "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"
    groq_api_key = os.getenv("GROQ_API_KEY")
    print(groq_api_key)
    model_name = "llama3-8b-8192"
    llm = ChatGroq(temperature=0.5, groq_api_key=groq_api_key, model_name=model_name)

    ######################## Define the re-writing query template with few shot examples ####################
    template = f"""Provide three better search queries for the web search engine to answer the given query.
    Strictly output the queries without anything else.
    
    Example:
    
    User query:
    I have a red light on my dashboard
    
    Answer:
    1. Red dashboard light meaning.
    2. Car dashboard red light symptoms.
    3. Red warning light on dashboard diagnosis

    
    {user_query}
    Answer:"""
    rewrite_prompt = ChatPromptTemplate.from_template(template)

    ######################################## Construct the LLM chain ########################################
    rewriter = rewrite_prompt | llm | StrOutputParser()
    ################################## Invoke the LLM with the user query ###################################
    with st.spinner('Generating queries...'):
        rewritten_query = rewriter.invoke({'user_query': user_query})
        print("rewritten query: ", rewritten_query)

    return rewritten_query