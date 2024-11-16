from datetime import datetime
from operator import itemgetter
import textwrap
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from ai.utils.llm import llm4o_mini
from langchain_core.prompts import PromptTemplate


class _Metadata_extractor_chain_input(BaseModel):
    users_language: str
    content: str
    timestamp: str
    
class Metadata_extractor_chain_output(BaseModel):
    description: str
    keywords: list[str]
    relative_time: dict[str, str]

_parser = PydanticOutputParser(pydantic_object=Metadata_extractor_chain_output)

_metadata_extractor_chain_prompt=PromptTemplate.from_template(textwrap.dedent("""
    You will be given a memo.
    Your job is to transform this memo so that it is easy to categorize and find later.

    There are so many different types of text that can be written in a memo.
    It could be a summary of what you studied, a schedule, someone's phone number, someone's birthday, or just random text.

    You need to guess what the memo is for, what it is meant to store.
    To do this, I will give you the language the user speaks, the content of the memo, and the time the user wrote the memo.

    Here is what you need to do:

    1. Write a description of the memo the user wrote.
    The user always writes a memo with some intention. You need to guess that intention and write a description of the memo.

    2. Extract keywords so that the user can search the memo.
    The user may need this memo to find some information later. Extract keywords for that purpose.
    Think about what keywords the user might use to find this memo.
    For example, if this memo is related to a schedule, you can select 'schedule' as a keyword.
    Extract keywords so that users can search for similar terms later. For example, so that 'to-do' can be found by searching for 'schedule'.

    3. Extract and convert words that indicate relative time.
    memos such as schedules may use words that indicate relative time, such as "next week." These should be converted based on the current time so that the user can find them later.
    I'll give you an example.
    If a user saved a memo that says "There's a competition next Sunday," "next Sunday" can be converted based on the time the memo was written.

    One thing to keep in mind is that all descriptions and keywords should be written in the language the user speaks so that the user can read them.
    Even when writing expressions related to relative time, you should use the language the user speaks.

    Here is information about the user's memo.
    
    {input_json}
    
    {format}
    """),
    partial_variables={
        "format": _parser.get_format_instructions()
    }
)

_metadata_extractor_chain=(
    { "input_json": itemgetter("input_json") }
    | _metadata_extractor_chain_prompt
    | llm4o_mini
    | _parser
)

async def metadata_extractor(content: str, lang: str) -> Metadata_extractor_chain_output:
    input_json_model=_Metadata_extractor_chain_input(
        content=content,
        users_language=lang,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    return await _metadata_extractor_chain.ainvoke({"input_json": input_json_model.model_dump_json()})
