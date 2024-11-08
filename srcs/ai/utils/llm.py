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

finetunned_for_tags=ChatOpenAI(
    model="ft:gpt-4o-mini-2024-07-18:oatnote::AR9sfEIQ"
)

finetunned_for_structures=ChatOpenAI(
    model="ft:gpt-4o-2024-08-06:oatnote::AR9p5xxL"
)

finetunned_for_structures_mini=ChatOpenAI(
    model="ft:gpt-4o-mini-2024-07-18:oatnote:structures:AR1iRuz3"
)

openai_client=OpenAI()
