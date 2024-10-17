from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field
from ai.utils.llm import llm4o_mini
from langchain_core.prompts import PromptTemplate


_parser = StrOutputParser()

_text_summarizer_chain_prompt=PromptTemplate.from_template(
"""
This is the content of a web page.
Summarize this content in a reasonable length that I can write down in a note.
I want to be able to look at the notes later and know what's on this web page.

Summarize it in the user's language.

User's language: {lang}

{text}
"""
)

text_summarizer_chain=(
    {
        "text": itemgetter("text"),
        "lang": itemgetter("lang"),
    }
    | _text_summarizer_chain_prompt
    | llm4o_mini
    | _parser
)
