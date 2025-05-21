from transformers import pipeline
from langchain.llms import HuggingFacePipeline
from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory


hf_pipeline = pipeline(
    task="text2text-generation",
    model="google/flan-t5-base",
    tokenizer="google/flan-t5-base",
    max_length=256
)
def custom_greet(name:str)->str:
    return f"Hello {name} this is from custom greet"
    
greet_tool=Tool(
name="CustomGreeter",
func=custom_greet,
description="Use this tool when you need to greet by name"
)
llm = HuggingFacePipeline(pipeline=hf_pipeline)
memory = ConversationBufferMemory(memory_key="chat_history")
agent=initialize_agent(
tools=[greet_tool],
llm=llm,
agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
memory=memory,
verbose=True,
handle_parsing_errors=True
)
print(agent.run("Hi,my name is Shreya."))
print(agent.run("What is my name?"))

