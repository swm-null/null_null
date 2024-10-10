import json
from typing import Union
from langchain.agents.output_parsers import ReActJsonSingleInputOutputParser
from langchain_core.output_parsers import PydanticOutputParser
from ai.searching.utils.agents.models.similarity_search_agent_output import Similarity_search_agent_output
from langchain.schema import AgentAction, AgentFinish


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
