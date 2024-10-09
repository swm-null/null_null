from operator import itemgetter
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from ai.utils.llm import llm4o
from langchain_core.prompts import PromptTemplate
from ai.saving.tag._configs import TAG_SELECTION_COUNT
from ai.saving.tag.utils.selector.chains.utils.tag_formater_with_is_new import format_tags_with_is_new


class _selected_tag_output(BaseModel):
    tag_names: list[str] = Field(description="selected tag names")

_parser = PydanticOutputParser(pydantic_object=_selected_tag_output)

_tag_selector_chain_prompt=PromptTemplate.from_template(
"""
You're an expert at categorizing documents.
Given a document and a set of categories, you choose which category this document can belong to.
Pick up to '{selection_count}' of the most relevant categories that this article could belong to.
You don't have to select all {selection_count} categories if you think they are less relevant.
Dismiss new tags that is very similar to existing tag like "짧은 질문" and "짧은질문".

I'll attach the document and the categories for you.
The document is given between ᝃ. Sometimes it can be empty.

Language: {lang}
Document: ᝃ{query}ᝃ
List of categories: [{tags}]

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
        "tags": itemgetter("tags") | RunnableLambda(format_tags_with_is_new),
        "lang": itemgetter("lang"),
    }
    | _tag_selector_chain_prompt
    | llm4o
    | _parser
)
