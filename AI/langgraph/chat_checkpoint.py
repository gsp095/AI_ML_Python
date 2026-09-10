from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph,START,END
from openai import OpenAI
from dotenv import load_dotenv
import os
from langgraph.checkpoint.neo4j import Neo4jSaver

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
load_dotenv(
    os.path.join(os.path.dirname(__file__), "..", "memory_agent", ".env")
)
deployment_name_model = os.getenv("DEPLOYMENT_MODEL_NAME")
client = OpenAI(
    base_url=os.getenv("ENDPOINT_URL"),
    api_key=os.getenv("OPENAI_API_KEY"),
)

def call_llm(messages):
    openai_messages = [
        {
            "role": "user" if message.type == "human" else message.type,
            "content": message.content,
        }
        for message in messages
    ]
    response = client.chat.completions.create(
        model=deployment_name_model,
        messages=openai_messages,
    )
    print( response.choices[0].message.content)
    return response.choices[0].message.content

class State(TypedDict):
    messages: Annotated[list,add_messages]

def chatbot(state: State):
    response = call_llm(state["messages"])
    return {"messages": [response]}


graph_builder= StateGraph(State)

graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

#(START)-> chatbot-> samplenode-> END

NEO4J_URI = os.getenv("NEO4J_URI") or os.getenv("NEO4J_URL")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

if not all((NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)):
    raise RuntimeError(
        "Set NEO4J_URI (or NEO4J_URL), NEO4J_USERNAME, and NEO4J_PASSWORD"
    )

with Neo4jSaver.from_conn_string(
    NEO4J_URI,
    auth=(NEO4J_USERNAME, NEO4J_PASSWORD),
) as checkpointer:
    checkpointer.setup()
    graph_with_checkpointer = graph_builder.compile(checkpointer=checkpointer)
    config = {
        "configurable":{
            "thread_id": "govind"
        }
    }

    for message in ("what is 1+1+3-5","What is my name?",):
        updated_state = graph_with_checkpointer.invoke(
            {"messages": [message]},
            config,
        )
        updated_state["messages"][-1].pretty_print()