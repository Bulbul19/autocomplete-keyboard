import os
from groq import Groq

# Set your Groq API key here OR use environment variable GROQ_API_KEY
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)
