from operator import itemgetter
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from ai.utils import llm4o
from langchain_core.prompts import PromptTemplate

class _Tag_name(BaseModel):
    name: str

_parser = PydanticOutputParser(pydantic_object=_Tag_name)

_new_tag_chain_prompt=PromptTemplate.from_template(
"""
You're an expert at categorizing documents.
Given a document, you create a category to encompass it.
Create based on how the average person categorizes notes.
Not just a category for this document, but a category for anything similar to this document. 
But I don't want the category to be so broad that it could contain too many documents.
Use ' ' and do not use '_'.

I'm attaching a document for you.
Create the category in the user's language.
Categories can be one or two words.
The document is given between ᝃ. Sometimes it can be empty.

User's language: {lang}
Document: ᝃ{query}ᝃ

{format}
""",
    partial_variables={
        "format": _parser.get_format_instructions()
    }
)

new_tag_chain=(
    {
        "query": itemgetter("query"),
        "lang": itemgetter("lang"),
    }
    | _new_tag_chain_prompt
    | llm4o
    | _parser
)
