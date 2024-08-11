from openai import OpenAI
import os

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Retrieve the API key from the environment variables
api_key = os.getenv("OPENAI_API_KEY")
# print(api_key)
# Check if the API key was loaded correctly
if not api_key:
    raise ValueError("API key not found. Please check your .env file.")
else:
    print('The api key exists?\n')
    
client = OpenAI()

stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Say this is a test"}],
    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")