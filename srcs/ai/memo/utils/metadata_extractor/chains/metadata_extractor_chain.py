from operator import itemgetter
import textwrap
from langchain_core.output_parsers import StrOutputParser
from ai.utils.llm import llm4o_mini
from langchain_core.prompts import PromptTemplate


_parser = StrOutputParser()

_metadata_extractor_chain_prompt=PromptTemplate.from_template(textwrap.dedent("""
    I want to create description about memo so I can find them easily.

    Describe what this note is about, or what it contains, as best you can given the information you have.
    Write the description in the user's language as well.

    You might want to include "주민등록번호" in the metadata if it comes in as a string like "928173-2819811", like a Korean social security number,
    If the note is about a series of addresses, we don't know where, but we can add that this is a note about addresses.

    User's language: {lang}
    Memo's content: {content}
    """)
)

metadata_extractor_chain=(
    {
        "content": itemgetter("content"),
        "lang": itemgetter("lang"),
    }
    | _metadata_extractor_chain_prompt
    | llm4o_mini
    | _parser
)
