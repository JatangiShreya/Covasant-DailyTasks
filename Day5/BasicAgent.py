from langchain_community.llms import Ollama
from langchain.agents import initialize_agent, load_tools
from langchain.agents.agent_types import AgentType
from langchain.tools import tool
llm = Ollama(model="llama3")
@tool
def math_tool(query: str) -> str:
    """
    This tool evaluates a mathematical expression passed as a string.
    Example: '7 * 5 + 34' will return '69'.
    """
    result = str(eval(query))
    return result
tools = [math_tool]  

agent = initialize_agent(
    tools=tools, 
    llm=llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

question = input("Ask your question: ")
response = agent.run(question)
print("Agent:", response)
