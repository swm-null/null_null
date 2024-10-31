from datetime import datetime, timezone
from operator import itemgetter
import textwrap
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from ai.utils import llm4o_mini
from langchain_core.prompts import PromptTemplate


class _Keyword_query_generator_chain_input(BaseModel):
    raw_query: str
    users_lang: str

class Keyword_query_generator_chain_output(BaseModel):
    query: str
    start_time: datetime | None
    end_time: datetime | None

_parser = PydanticOutputParser(pydantic_object=Keyword_query_generator_chain_output)

_query_generator_chain_prompt=PromptTemplate.from_template(textwrap.dedent("""
    Transform a user’s natural language query into a structured keyword-based search query for MongoDB Atlas search. Follow the instructions below to ensure the query accurately captures the user's intent, language, and any specified time frame.

    ### Instructions:
    1. **Language Detection**:
    - Detect the **user's language** from the query and given field(users_lang).
    - Ensure the resulting keywords are suitable for searches in that language.

    2. **Keyword Extraction**:
    - Identify key terms that represent the query’s intent.
    - Convert these into focused keywords, emphasizing relevance and avoiding filler words.

    3. **Time Period Adjustment**:
    - If the query specifies a **time frame** (e.g., "first week of last month"), determine **start_time** and **end_time** using current time ({current_time}) for reference.
    - Include only start_time and end_time fields if a time frame is specified in the query.
    
    {input_json}

    {format}
    """),
    partial_variables={
        "format": _parser.get_format_instructions(),
        "current_time": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    }
)

_keyword_query_generator_chain=(
    { "input_json": itemgetter("input_json") }
    | _query_generator_chain_prompt
    | llm4o_mini
    | _parser
)

async def keyword_query_generator(query: str, lang: str) -> Keyword_query_generator_chain_output:
    input_json_model=_Keyword_query_generator_chain_input(
        raw_query=query,
        users_lang=lang
    )
    
    return await _keyword_query_generator_chain.ainvoke({"input_json": input_json_model.model_dump_json()})
