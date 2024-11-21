from datetime import datetime, timezone
from operator import itemgetter
import textwrap
from fastapi import HTTPException
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from ai.utils import llm4o
from langchain_core.prompts import PromptTemplate


class _Keyword_query_generator_chain_input(BaseModel):
    raw_query: str
    users_lang: str
    current_time: str

class Keyword_query_generator_chain_output(BaseModel):
    query: str
    start_time: datetime | None
    end_time: datetime | None

_parser = PydanticOutputParser(pydantic_object=Keyword_query_generator_chain_output)

_query_generator_chain_prompt=PromptTemplate.from_template(textwrap.dedent("""
    You are a smart AI that analyzes how to search for a question in the DB to find a note with specific content when a user asks a question.

    Users ask questions with various intentions. Users want to find specific information in a note.

    However, since questions are in natural language, whether declarative or interrogative, they cannot be searched in the DB as is.

    For example, when a user asks a question like "Show me the notes I wrote last week," even if you search the DB for "notes I wrote last week," you will not get the results the user wants. You have to search all notes whose date of creation was last week to get the results.

    However, if a user asks a question like "Collect my schedule for next month", keep in mind that the user wants to know about the schedule for next month written in the notes, not the notes written about the schedule for next month.
    Also, when organizing schedules, etc., sort them in chronological order.
    
    You are an AI that recognizes the user's intention, analyzes what to search for in the DB, and produces results by finding out which period the notes were created in. If the user doesn't seem to want notes written during a specific period, just send start_time and end_time as null.

    Since the user writes notes in their own language, we need to search in the DB in their own language. So, create a query in their own language.

    Below, I'll give you the language the user uses, what the user asked, and the current time.
    Create a query that analyzes the user's intent as much as possible and can search!
    
    {input_json}

    {format}
    """),
    partial_variables={
        "format": _parser.get_format_instructions()
    }
)

_keyword_query_generator_chain=(
    { "input_json": itemgetter("input_json") }
    | _query_generator_chain_prompt
    | llm4o
    | _parser
)

async def keyword_query_generator(query: str, lang: str) -> Keyword_query_generator_chain_output:
    input_json_model=_Keyword_query_generator_chain_input(
        raw_query=query,
        users_lang=lang,
        current_time=datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    )
    
    for _ in range(3):
        try:
            return await _keyword_query_generator_chain.ainvoke({"input_json": input_json_model.model_dump_json()})
        except:
            pass
    
    raise HTTPException(status_code=500, headers={"keyword_query_generator]": "failed"})
