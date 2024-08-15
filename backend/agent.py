import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import tool

load_dotenv('../.env.local')


@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers.

    Args:
        a (float): The first number
        b (float): The second number

    Returns:
        float: The result of multiplying
    """
    return a * b


def create_agent():
    llm = ChatOpenAI(
        model='gpt-4o-mini', temperature=0, api_key=os.getenv('OPENAI_API_KEY')
    )

    # Get the prompt to use - you can modify this!
    prompt = hub.pull('hwchase17/openai-functions-agent')
    prompt.messages
    prompt.messages[0].prompt.template = """
    You are a helpful assistant. But you are not good at calculate math.
    If you are asked to calculate math, you **must** use the tools that are available to you.
    Do not try to calculate math on your own.
    """
    tools = [multiply]
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor
