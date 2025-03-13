# Setting up

## Python environment
1. Install conda: `bash setup-conda.sh && source ~/.bashrc`
2. Create conda environment:
   If you run into error like `UnavailableInvalidChannel: HTTP 403 FORBIDDEN for channel <some channel>` on your EC2 instance, you can solve it by running `conda config --remove channels <some channel>`, and make sure you have the default channel by running `conda config --add channels defaults`.
```bash
conda create -n chat_bot_env python=3.13
conda activate chat_bot_env
pip install -r requirements.txt
pip install -e .
```
3. Make a .env and make sure to add your GROQ_API_KEY
