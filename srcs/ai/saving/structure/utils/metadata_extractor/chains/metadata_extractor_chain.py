from operator import itemgetter
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from ai.utils.llm import llm4o
from langchain_core.prompts import PromptTemplate


class metadata_extractor_chain_output(BaseModel):
    metadata: str=Field(description="metadata of memo")

_parser = PydanticOutputParser(pydantic_object=metadata_extractor_chain_output)

_metadata_extractor_chain_prompt=PromptTemplate.from_template(
    """
    I want to categorize these notes later, or create metadata about them so I can find them easily.

    Describe what this note is about, or what it contains, as best you can given the information you have.
    Write the metadata in the user's language as well.

    You might want to include "주민등록번호" in the metadata if it comes in as a string like "928173-2819811", like a Korean social security number,
    If the note is about a series of addresses, we don't know where, but we can add that this is a note about addresses.

    User's language: {lang}              
    Memo's content: {content}

    {format}
    """,
    partial_variables={
        "format": _parser.get_format_instructions()
    }
)

metadata_extractor_chain=(
    {
        "content": itemgetter("content"),
        "lang": itemgetter("lang"),
    }
    | _metadata_extractor_chain_prompt
    | llm4o
    | _parser
)
