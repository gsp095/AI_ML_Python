from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()
deployment_name_model = os.getenv("DEPLOYMENT_MODEL_NAME")

print(os.getenv("OPENAI_API_KEY"))
print(os.getenv("ENDPOINT_URL"))
print(os.getenv("DEPLOYMENT_MODEL_NAME"))
client = OpenAI(
    base_url=os.getenv("ENDPOINT_URL"),
    api_key=os.getenv("OPENAI_API_KEY"),
)

response = client.chat.completions.create(
    model=deployment_name_model,
     messages=[
        {"role": "system", "content": "You are user friendly chatboat to response user query with correct information. If don't know then response Simply no."},
        {"role": "user", "content": "what is capital of dhikoda?."},
    ],
)

print(f"answer: {response.choices[0].message.content}")
