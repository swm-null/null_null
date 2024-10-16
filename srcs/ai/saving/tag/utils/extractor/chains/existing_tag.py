from operator import itemgetter
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from ai.saving.tag.utils.extractor.similar_tags_retriever import retrieve_similar_tags
from ai.saving._models import Tag
from ai.utils import llm4o
from langchain_core.prompts import PromptTemplate


class _existing_tag_output(BaseModel):
    tag_list: list[str]=Field(description="list of tag names")

_parser = PydanticOutputParser(pydantic_object=_existing_tag_output)

_existing_chain_prompt=PromptTemplate.from_template(
"""
You're an expert at categorizing documents.
Given a document, you choose the best categorization you think fits.
Choose based on how the average person categorizes notes.
You might not choose one if you don't think it's a good fit, or you might choose multiple if you think there are several that are very good fits.
If such a category does not exist, you don't have to select it.

I've attached the document and the categorizations for you.
The document is given between ᝃ. Sometimes it can be empty.

Language: {lang}
Document: ᝃ{query}ᝃ
List of categories: [{tag_names}]

{format}
""",
    partial_variables={
        "format": _parser.get_format_instructions()
    }
)

existing_tag_chain=(
    {
        "query": itemgetter("query"),
        "lang": itemgetter("lang"),
        "tag_names": itemgetter("tag_names")
    }
    | _existing_chain_prompt
    | llm4o
    | _parser
)
