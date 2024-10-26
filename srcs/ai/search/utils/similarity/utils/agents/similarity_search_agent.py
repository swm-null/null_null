import json
from typing import Any, Optional
from langchain.agents import create_react_agent, AgentExecutor
from pydantic import BaseModel, Field
from ai.utils.llm import llm4o
from langchain_core.prompts import PromptTemplate
from typing import Union
from langchain.agents.output_parsers import ReActJsonSingleInputOutputParser
from langchain_core.output_parsers import PydanticOutputParser
from langchain.schema import AgentAction, AgentFinish
from ai.search.utils.similarity.utils.agents.tools import duckduckgo_search


class _Similarity_search_agent_input(BaseModel):
    user_id: str
    lang: str
    question: str

class Similarity_search_agent_output(BaseModel):
    action: Optional[str]=None
    action_input: Optional[dict[str, str]]=None
    final_answer: Optional[str]=Field(description="answer to the user's question")
    used_memo_ids: list[str]=Field(description="used memo ids", default=[])

tools = [
    # memo_answerer,
    duckduckgo_search
]

class Similarity_search_agent_output_parser(ReActJsonSingleInputOutputParser):
    _pydantic_parser=PydanticOutputParser(pydantic_object=Similarity_search_agent_output)            
        
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        try:
            parsed_output=self._pydantic_parser.parse(llm_output)
            if parsed_output.action and parsed_output.action_input:
                return AgentAction(parsed_output.action, parsed_output.action_input, llm_output)
            else:
                return AgentFinish(
                    return_values={
                        "answer": parsed_output.final_answer,
                        "used_memo_ids": parsed_output.used_memo_ids
                    },
                    log=llm_output,
                )
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON output: {llm_output}")
        except ValueError as e:
            raise ValueError(f"Invalid output format: {str(e)}")

    def get_format_instructions(self) -> str:
        return self._pydantic_parser.get_format_instructions()

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
