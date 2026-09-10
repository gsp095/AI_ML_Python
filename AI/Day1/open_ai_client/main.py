from openai import AzureOpenAI
from  dotenv import load_dotenv
import os

load_dotenv()
print(os.getenv("OPENAI_API_KEY"))
client = AzureOpenAI(base_url="https://ai-learning-gsp.openai.azure.com/openai/v1", 
                     api_key=os.getenv("OPENAI_API_KEY"),
                     api_version = "2024-06-01"   )

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "What is the capital of India?"}
    ]
)

print(response.choices[0].message.content) 