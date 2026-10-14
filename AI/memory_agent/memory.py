from mem0 import Memory
from dotenv import load_dotenv
import os
from openai import OpenAI
import json
load_dotenv()

client = OpenAI(base_url=os.getenv("ENDPOINT_URL"),
                api_key=os.getenv("OPENAI_API_KEY"))

model_text_embeding = "text-embedding-3-small"

deployment_name_model = os.getenv("DEPLOYMENT_MODEL_NAME")
config = {
    "version": "v1.1",
    "embedder": {
        "provider": "openai",
        "config": {
            "openai_base_url": os.getenv("ENDPOINT_URL"),
            "api_key": os.getenv("OPENAI_API_KEY"),
            "model": model_text_embeding
        }
    },
    "llm": {
        "provider": "openai",
        "config": {
            "openai_base_url": os.getenv("ENDPOINT_URL"),
            "api_key": os.getenv("OPENAI_API_KEY"),
            "model": deployment_name_model
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": "6333"

        }
    }
}

memory_client = Memory.from_config(config)
while True:
    user_query = input("How Can I help you? \n> ")
    search_memory = memory_client.search(query=user_query, filters={"user_id": "Govind"})
    memories = [
        f"Id:{mem.get("id")}\nMemory:{mem.get("memory")}" for mem in search_memory.get("results")
    ]
    print(memories)

    SYSTEM_PROMPT = f"""
    Here is the context about the user :
    {json.dumps(memories)} 
    """
    response = client.chat.completions.create(
        model=deployment_name_model,
        messages=[
            {"role": "user", "content": user_query},
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
    )
    ai_response = response.choices[0].message.content
    print("AI : ", ai_response)
    memory_client.add(
        user_id="Govind",
        messages=[
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": ai_response}
        ]
    )
    print("AI : memory has been saved")
