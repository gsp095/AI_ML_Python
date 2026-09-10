from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph,START,END
try:
    from src.states import AgentState
    from src.nodes import generate_code_node,write_file_node,validate_code_node
except ModuleNotFoundError as error:
    if error.name != "src":
        raise
    from states import AgentState
    from nodes import generate_code_node,write_file_node,validate_code_node

def routing_condition(state: AgentState):
    """Branching path configuration depending on structural exection success"""
    if state['success']:
        return "END"
    if state['iterations']>=3:
         print("--- MAX ITERATIONS REACHED. TERMINATING AGENT ---")
         return "END"
    return "RETRY"


builder= StateGraph(AgentState)

builder.add_node("generator", generate_code_node)
builder.add_node("writer", write_file_node)
builder.add_node("verifier", validate_code_node)

builder.add_edge(START, "generator")
builder.add_edge("generator", "writer")
builder.add_edge("writer", "verifier")

builder.add_conditional_edges(
    "verifier",
    routing_condition,
    {
        "END": END,
        "RETRY": "generator"
    })

app = builder.compile()

if __name__== "__main__":
     initial_input = {
        "task": "Can please me to write .net core C# minimal API for crud operation using MS SQL database take example of create employee data.",
        "file_path": "output/Program.cs",
        "iterations": 0,
        "language": ".net",
        "success": False,
        "error": None,
        "generated_code": None
    }

     for event in app.stream(initial_input):
          print(event)
