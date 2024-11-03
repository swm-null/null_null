from langchain_openai import ChatOpenAI
from openai import OpenAI


llm4o=ChatOpenAI(
    model="gpt-4o",
    temperature=0,
)

llm4o_mini=ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

openai_client=OpenAI()
