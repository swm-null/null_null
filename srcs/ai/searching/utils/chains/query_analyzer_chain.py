from operator import itemgetter
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from ai.utils.llm import llm4o
from langchain_core.prompts import PromptTemplate
from ai.searching.models.query_type import Query_Type


class _query_analyzer_chain_output(BaseModel):
    type: Query_Type=Field("type of query")

_parser = PydanticOutputParser(pydantic_object=_query_analyzer_chain_output)

_query_analyzer_chain_prompt=PromptTemplate.from_template(
    """
    You need to analyze the sentence to figure out what the user wants.
    Analyze the sentence according to the following rules and print ONE correct answer.
    Apply the rules in the order they are written, and if any of them are correct, print them out.

    -- Rules -- 
    If the sentence is a request to find information that fits a specific pattern, print 'regex'.
    Else, print 'similarity'.

    Language: {lang}              
    Sentence: {query}

    {format}
    """,
    partial_variables={
        "format": _parser.get_format_instructions()
    }
)

query_analyzer_chain=(
    {
        "lang": itemgetter("lang"),
        "query": itemgetter("query"),
    }
    | _query_analyzer_chain_prompt
    | llm4o
    | _parser
)
