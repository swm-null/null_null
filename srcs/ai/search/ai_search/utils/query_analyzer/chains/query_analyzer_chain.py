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
    Analyze the provided sentence to determine the user's intent and output ONE correct answer.

    ### Objective:
    - Apply the rules **in sequence**, and print the result of the **first rule** that matches.

    ### Rules:
    1. Determine whether this question can be answered using a regular expression. 
    2. **If** the sentence requests information that fits a **specific pattern**(regular expression). print `'regex'`.
    3. **Otherwise**, print `'similarity'`.

    ### Expected Output:
    - Return only the word `'regex'` or `'similarity'`, based on the analysis.

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
