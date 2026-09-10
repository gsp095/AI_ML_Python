from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
pdf_path= Path(__file__).parent/ "gsp.pdf"

#load  this file in python code

loader= PyPDFLoader(file_path=pdf_path)
print("PDF load Started")
docs=loader.load()
print("PDF load Completed")
# print(docs[3]) 


# split teh doc into smaller 
print("PDF Stliting/Chuck  Started")
text_spliter= RecursiveCharacterTextSplitter(
    chunk_size=1000,       # Target maximum size of each chunk
    chunk_overlap=400    # Overlapping characters between adjacent chunks
    )

chunks= text_spliter.split_documents(documents=docs)
print("PDF Stliting/Chuck Completed")

#Vector Embeding

print("ENDPOINT_URL",os.getenv("ENDPOINT_URL"))

print("Embding Started")
embeding_model = OpenAIEmbeddings(
    model="text-embedding-3-small",
    base_url=os.getenv("ENDPOINT_URL"),
    api_key=os.getenv("OPENAI_API_KEY"),
)

vector_store = QdrantVectorStore.from_documents(
    documents= chunks,
    embedding=embeding_model,
    url=os.getenv("QDRANT_URL", "http://localhost:6333"),
    collection_name="Learning_rag"
)
print("Embding Completed",vector_store)

print("Indexing the document.........")