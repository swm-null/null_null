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

finetunned_for_tag=ChatOpenAI(
    model="ft:gpt-4o-mini-2024-07-18:oatnote:tags:AQygLx3p",
    temperature=0
)

openai_client=OpenAI()
