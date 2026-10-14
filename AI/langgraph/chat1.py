from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph,START,END
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
deployment_name_model = os.getenv("DEPLOYMENT_MODEL_NAME")
client = OpenAI(
    base_url=os.getenv("ENDPOINT_URL"),
    api_key=os.getenv("OPENAI_API_KEY"),
)

def call_llm(user_query: str):
    response = client.chat.completions.create(
        model=deployment_name_model,
        messages=[
            {"role": "user", "content": user_query},
        ],
    )
    print( response.choices[0].message.content)
    return response.choices[0].message.content

class State(TypedDict):
    messages: Annotated[list,add_messages]

def chatbot(state: State):
    latest_message = state["messages"][-1]
    response = call_llm(latest_message.content)
    return {"messages": [response]}

def samplenode(state: State):
    return {"messages": ["Hi , Sample message Node"]}

graph_builder= StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("samplenode", samplenode)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "samplenode")
graph_builder.add_edge("samplenode", END)

#(START)-> chatbot-> samplenode-> END

graph= graph_builder.compile()

updated_state = graph.invoke(State({"messages": ["Hi My name is Govind"]}))

print("Updated state",updated_state)