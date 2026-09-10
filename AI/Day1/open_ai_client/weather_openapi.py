from openai import OpenAI
from dotenv import load_dotenv
import os
import requests
import requests
import json
from pydantic import BaseModel,Field
from typing import Optional

def get_weather(city: str):
    url = f"https://wttr.in/{city}?format=%c+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return f"Werather in {city} is {response.text}"
    return "Something went wrong!"


print(get_weather("Udaipur"))
available_tools = {
    "get_weather": get_weather
}

load_dotenv()
deployment_name_model = os.getenv("DEPLOYMENT_MODEL_NAME")
system_prompt = """
You're an expert AI assistent in resolving user queries
You work on START,PLAN, OBSERVE and OUTPUT steps.
You need to first PLAN what need to be done. The Plan can be multiple steps.
Once you think enough PLAN has been done, finally you can give an OUTPUT.
You can also call a tool if required from the list of available tools.
For every tool call wait ther observe step which is the output from called tools.

Rule :
- Strickly follow the given JSON output format
- Only run one step at a time
- The sequence of steps is START(Where use gives an input), PLAN (That can be multiple times) ,TOOLS(Call the tool for get extra info if required), OBSERVE(Observe the tool cal result ), OUTPUT(Finaly provide resut)

Output JSON Format :
{"step": "START" | "PLAN"| "TOOL" | "OBSERVE" | "OUTPUT", "content" : "string", "tool": "string", "input" : "string" }

Available Tools : 
- get_weather(city: str):  Takes city name as input string and return the weather info about the city.

Eaxample : 
    START: What is the weather of Udaipur?
    PLAN:  {"step": "PLAN" :CONTENT:  "Seems like user is interested in getting weather of Udaipur city"}
    PLAN:  {"step": "PLAN" :CONTENT:  "Let see if we have any tools available to get weather info."}
    PLAN:  {"step": "PLAN" :CONTENT:  "Great we have get_weather available for query."}
    PLAN:  {"step": "PLAN" :CONTENT:  "I need to call get_weather tool for Udaipur city"}
    PLAN:  {"step": "TOOL": "tool": "get_weather" : "input" :  "Udaipur"}
    PLAN:  {"step": "OBSERVE": "tool": "get_weather" : Output :  "There temp of udaipur is cloudy with 27C temp."}
    PLAN:  {"step": "OUTPUT": "tool": "CONTENT" :  "Current weather of udaipur in cloudy with 27C temp."}
"""
class OututFOrmat(BaseModel):
    step: str= Field(..., description="Thid of the step. Example :PLAN,TOOL etc. ")
    content: Optional[str]=Field(None, description="The optional string content")
    tool: Optional[str]=Field(None, description="The tool info,")
    input: Optional[str]=Field(None, description="The input param for the tools,")

client = OpenAI(
    base_url=os.getenv("ENDPOINT_URL"),
    api_key=os.getenv("OPENAI_API_KEY"),
)
while True:
    user_query = input("👤🔡>")
    message_history = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ]
    

    def main():
        while True:
            response = client.chat.completions.parse(
                model="gpt-4o",   
                #OututFOrmat= OututFOrmat,
                messages=message_history)

            raw_result = response.choices[0].message.content
            message_history.append({"role": "assistant", "content": raw_result})
            parsed_result = json.loads(raw_result)
            if parsed_result.get("step") == "START":
                print("", parsed_result.get("content"))
                continue
            if parsed_result.get("step") == "TOOL":
                tool_to_call = parsed_result.get("tool")
                tool_to_input = parsed_result.get("input")
                tool_response = available_tools[tool_to_call](tool_to_input)
                print(f"🔨📞: {tool_to_call} ({tool_to_input}) = {tool_response}")
                message_history.append({"role": "developer", "content": json.dumps(
                    {"step": "OBSERVE", "tool": tool_to_call, "input": tool_to_input, "output": tool_response})})
                continue
            if parsed_result.get("step") == "PLAN":
                print("🧠🤯:", parsed_result.get("content"))
                continue
            if parsed_result.get("step") == "OUTPUT":
                print("OUTPUT ☺️:", parsed_result.get("content"))
                break

            print(f"🤖 : {response.choices[0].message.content}")


    main()
