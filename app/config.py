import os
from groq import Groq

# Set your Groq API key here OR use environment variable GROQ_API_KEY
API_KEY = os.environ.get("GROQ_API_KEY", "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")

client = Groq(api_key=API_KEY)
