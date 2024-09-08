from operator import itemgetter
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from ai.saving.tag._models.tag import Tag
from ai.saving.tag.utils.tag_formatter import tag_formatter
from ai.utils.llm import llm4o
from langchain_core.prompts import PromptTemplate
from ai.saving.tag._configs import TAG_SELECTION_COUNT


class _selected_tag_output(BaseModel):
    tag_list: list[Tag] = Field(description="list of tags")

_parser = PydanticOutputParser(pydantic_object=_selected_tag_output)

_tag_selector_chain_prompt=PromptTemplate.from_template(
    """
    You're an expert at categorizing documents.
    Given a document and a set of categories, you choose which category this document can belong to.
    Pick up to '{selection_count}' of the most relevant categories that this article could belong to.
    You don't have to select all {selection_count} if you think they are less relevant.

    I'll attach the document and the categories for you.
    The document is given between ᝃ. Sometimes it can be empty.
    
    Language: {lang}
    Document: ᝃ{query}ᝃ
    List of categories: [{tag_list}]

    {format}
    """,
    partial_variables={
        "format": _parser.get_format_instructions(),
        "selection_count": TAG_SELECTION_COUNT,  
    }
)

tag_selector_chain=(
    {
        "query": itemgetter("query"),
        "tag_list": itemgetter("tag_list") | RunnableLambda(tag_formatter),
        "lang": itemgetter("lang"),
    }
    | _tag_selector_chain_prompt
    | llm4o
    | _parser
)
