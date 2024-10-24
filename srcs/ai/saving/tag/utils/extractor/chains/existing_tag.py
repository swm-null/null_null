from operator import itemgetter
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from ai.saving._models import Tag
from ai.utils import llm4o_mini
from langchain_core.prompts import PromptTemplate


class _Get_existing_tag_chain_input(BaseModel):
    query: str
    tag_names: list[str]
    lang: str
    
class _Get_existing_tag_chain_output(BaseModel):
    tag_list: list[str]=Field(description="list of tag names")

_parser = PydanticOutputParser(pydantic_object=_Get_existing_tag_chain_output)

_existing_chain_prompt=PromptTemplate.from_template(
"""
You're an expert at organizing memos.
Your memos are categorized using tags, and each tag can have subtags that belong to the tag.

The user is about to add a new memo.
You need to decide which of the existing tags to associate this memo under to categorize it.

If you don't think there's a suitable tag, you can select none of them.
Or, if you think multiple tags are appropriate, you can select multiple tags.
When choosing a tag, there may be multiple similar tags, so pick the most “specific” and “detailed” one. It's more likely to be under a broader tag.

Look at the json below, and generate the results.

{input_json}

{format}
""",
    partial_variables={
        "format": _parser.get_format_instructions()
    }
)

_get_existing_tag_chain=(
    { "input_json": itemgetter("input_json") }
    | _existing_chain_prompt
    | llm4o_mini
    | _parser
)

async def get_existing_tag(query: str, similar_tags: list[Tag], lang: str) -> _Get_existing_tag_chain_output:
    input_json_model=_Get_existing_tag_chain_input(
        query=query,
        tag_names=[tag.name for tag in similar_tags],
        lang=lang
    )
    
    return await _get_existing_tag_chain.ainvoke({"input_json": input_json_model.model_dump_json()})
