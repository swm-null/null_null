from typing import Any
from langchain.agents import create_react_agent, AgentExecutor
from pydantic import BaseModel
from ai.utils.llm import llm4o
from langchain_core.prompts import PromptTemplate
from ai.searching.utils.agents.similarity_search_agent_output_parser import Similarity_search_agent_output_parser
from ai.searching.utils.agents.tools.internet_search import duckduckgo_search


class _Similarity_search_agent_input(BaseModel):
    user_id: str
    lang: str
    question: str

tools = [
    # memo_answerer,
    duckduckgo_search
]

_parser=Similarity_search_agent_output_parser()

_similarity_agent_prompt=PromptTemplate.from_template(
"""
Answer the following questions as best you can. You have access to the following tools:
{tools}

If answerable, set Action field to NULL.
At the beginning of your final answer, please make sure to write that this is the result of an internet search for an answer that cannot be answered with a user's note, and that it may not be accurate.

Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action

... (this Thought/Action/Action Input/Observation can repeat N times)

Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

{input_json}
 
Thought: {agent_scratchpad}

{format}
""",
    partial_variables={
        "format": _parser.get_format_instructions()
    }
)

_similarity_search_agent = create_react_agent(
    tools=tools,
    llm=llm4o,
    prompt=_similarity_agent_prompt,
    output_parser=_parser,
)

similarity_search_executor=AgentExecutor(agent=_similarity_search_agent, tools=tools, verbose=True)

async def invoke_similarity_search_agent(user_id: str, query: str, lang: str) -> tuple[str, list[str]]:
    input_json_model=_Similarity_search_agent_input(
        user_id=user_id,
        question=query,
        lang=lang
    )
        
    agent_result: dict[str, Any]=await similarity_search_executor.ainvoke({"input_json": input_json_model.model_dump_json()})
    
    return agent_result["answer"], agent_result["used_memo_ids"]
