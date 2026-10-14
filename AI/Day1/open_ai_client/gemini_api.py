from google import genai
from dotenv import load_dotenv
import os
load_dotenv();

client= genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

respose= client.models.generate_content(
    model=os.getenv("GEMINI_DEPLOYMENT_MODEL_NAME"),
    contents="What is ML.net"
)

print("Response : ",respose.text) 