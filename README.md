# Another RAG ChatBot 

## Summary

This application is a Retrieval-Augmented Generation (RAG) chatbot that reads a PDF document, specifically a Toyota user manual. It processes the content, and enables natural language queries about the information contained within this manual.

### Features & Capabilities

* PDF document processing: Load and convert PDF documents into text format for analysis and retrieval
* Semantic search capability: Build and query vector stores for accurate information retrieval
* Query rewriting: Improve search accuracy by reformulating user queries to better match document content
* Context-aware responses: Generate responses based on the most relevant document sections
* Inference: Uses Groq and Llama 3 for response generation
* Simple web interface: Built with Streamlit for intuitive user interaction
* Deployable on localhost: Intended as a playground for personal use 

## Setting up

### Python environment
1. Install conda: `bash setup-conda.sh && source ~/.bashrc`
2. Create conda environment:
```bash
conda create -n chat_bot_env python=3.13
conda activate chat_bot_env
pip install -r requirements.txt
```
3. Make a .env with your GROQ_API_KEY

4. Run locally as: ```streamlit run app.py```
