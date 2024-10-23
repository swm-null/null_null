from operator import itemgetter
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from ai.utils import llm4o
from langchain_core.prompts import PromptTemplate


class _get_new_tag_chain_input(BaseModel):
    query: str
    lang: str
    
class _get_new_tag_chain_output(BaseModel):
    name: str

_parser = PydanticOutputParser(pydantic_object=_get_new_tag_chain_output)

_get_new_tag_chain_prompt=PromptTemplate.from_template(
"""
You're an expert at organizing memos.
Your memos are categorized using tags, and each tag can have subtags that belong to the tag.

The user is about to add a new memo.
Please suggest a tag name to categorize this note.
The tags you recommend will be automatically placed among existing tags later. Be careful not to name tags too specifically.

Use ' ' as a space, and don't use special characters like '_'.
Be careful not to misspell spaces.

Create tags in the language of your users.

{input_json}

{format}
""",
    partial_variables={
        "format": _parser.get_format_instructions()
    }
)

_get_new_tag_chain=(
    { "input_json": itemgetter("input_json") }
    | _get_new_tag_chain_prompt
    | llm4o
    | _parser
)

async def get_new_tag(query: str, lang: str):
    input_json_model=_get_new_tag_chain_input(
        query=query,
        lang=lang
    )
    
    return await _get_new_tag_chain.ainvoke({"input_json": input_json_model.model_dump_json()})
