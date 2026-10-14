from langchain_openai import OpenAIEmbeddings
from openai import OpenAI
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
import os

load_dotenv()
deployment_name_model = os.getenv("DEPLOYMENT_MODEL_NAME")


embeding_model = OpenAIEmbeddings(
    model="text-embedding-3-small",
    base_url=os.getenv("ENDPOINT_URL"),
    api_key=os.getenv("OPENAI_API_KEY"),
)

vector_db= QdrantVectorStore.from_existing_collection( 
    embedding=embeding_model,
    url=os.getenv("QDRANT_URL", "http://localhost:6333"),
    collection_name="Learning_rag")

# take use query
while True:
    user_query= input("Ask something :>")

    search_result=vector_db.similarity_search(query= user_query)
    print("search_result",search_result)
    context ="\n\n\n".join([f"Page Content: {result.page_content}\n Page Number :{result.metadata['page_label']}\n File Location : {result.metadata['source']}"
    for result in search_result])

    SYSTEM_PROMPT=F"""
    You are a helpfull AI assistemt who ans query based on available context retrived from pdf file along with the page number

    Context: {context}
    """

    client = OpenAI(
        base_url=os.getenv("ENDPOINT_URL"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    response = client.chat.completions.create(
        model=deployment_name_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query},
        ],
    )

    print(f"🤖 :",response.choices[0].message.content)