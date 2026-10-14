from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv();

client= OpenAI(api_key=os.getenv("GEMINI_API_KEY"), base_url=os.getenv("GEMINI_ENDPOINT_URL"))

respose= client.chat.completions.create(
    model=os.getenv("GEMINI_DEPLOYMENT_MODEL_NAME"),
    messages=[
        {"role":"system", "content": "You are tutor for Programming language." },
        {"role":"user", "content": "What is Python"}
    ]
)

print("Response : ",respose.choices[0].message.content)  