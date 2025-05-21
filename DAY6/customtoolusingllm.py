from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
from langchain.llms import OpenAI

def custom_greet(name:str)->str:
    return f"Hello {name} this is from custom greet"
    
greet_tool=Tool(
name="CustomGreeter",
func=custom_greet,
description="Use this tool when you need to greet by name"
)
llm=OpenAI(temperature=0)
agent=initialize_agent(
tools=[greet_tool],
llm=llm,
agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
verbose=True
)
response=agent.run("Say hello to Shreya")
print(response)

