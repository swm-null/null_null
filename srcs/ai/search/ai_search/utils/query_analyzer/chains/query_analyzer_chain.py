from operator import itemgetter
import textwrap
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from ai.utils import llm4o_mini
from langchain_core.prompts import PromptTemplate
from routers._models.search import Search_query_type


class _Query_analyzer_chain_input(BaseModel):
    query: str
    lang: str

class _Query_analyzer_chain_output(BaseModel):
    type: Search_query_type=Field("type of query")

_parser = PydanticOutputParser(pydantic_object=_Query_analyzer_chain_output)

_query_analyzer_chain_prompt=PromptTemplate.from_template(textwrap.dedent("""
    You need to analyze the sentence to figure out what the user wants.
    Analyze the sentence according to the following rules and print ONE correct answer.
    Apply the rules in the order they are written, and if any of them are correct, print them out.

    -- Rules -- 
    If the sentence is a request to find information that fits a specific pattern, print 'regex'.
    Else, print 'similarity'.

    {input_json}

    {format}
    """),
    partial_variables={
        "format": _parser.get_format_instructions()
    }
)

_query_analyzer_chain=(
    { "input_json": itemgetter("input_json") }
    | _query_analyzer_chain_prompt
    | llm4o_mini
    | _parser
)

async def query_analyzer_using_chain(query: str, lang: str) -> _Query_analyzer_chain_output:
    input_json_model=_Query_analyzer_chain_input(
        query=query,
        lang=lang
    )
    
    return await _query_analyzer_chain.ainvoke({"input_json": input_json_model.model_dump_json()})
