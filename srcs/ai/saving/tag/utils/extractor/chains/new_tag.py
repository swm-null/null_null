from operator import itemgetter
from langchain_core.output_parsers import PydanticOutputParser
from ai.saving._models import Tag
from ai.utils import llm4o
from langchain_core.prompts import PromptTemplate


_parser = PydanticOutputParser(pydantic_object=Tag)

_new_chain_prompt=PromptTemplate.from_template(
    """
    You're an expert at categorizing documents.
    Given a document, you create a category to encompass it.
    Create based on how the average person categorizes notes.
    Not just a category for this document, but a category for anything similar to this document. 
    But I don't want the category to be so broad that it could contain too many documents.

    I'm attaching a document for you.
    Create the category in the user's language.
    Categories can be one or two words.
    The document is given between ᝃ. Sometimes it can be empty.
    
    User's language: {lang}
    Document: ᝃ{query}ᝃ

    {format}
    Set new category's id to category's name.
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
    | _new_chain_prompt
    | llm4o
    | _parser
)
