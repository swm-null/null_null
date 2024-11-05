from operator import itemgetter
import textwrap
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from ai.memo._models import Tag
from ai.utils import llm4o_mini
from langchain_core.prompts import PromptTemplate


class _Get_existing_tag_chain_input(BaseModel):
    query: str
    tag_names: list[str]
    lang: str
    
class _Get_existing_tag_chain_output(BaseModel):
    tag_list: list[str]=Field(description="list of tag names")

_parser = PydanticOutputParser(pydantic_object=_Get_existing_tag_chain_output)

_existing_chain_prompt=PromptTemplate.from_template(textwrap.dedent("""
    You are an expert at organizing memos by assigning appropriate existing tags.

    ### Objective:
    - Determine which tag(s) from the provided list best categorize the new memo.  
    - If no suitable tag exists, select **none**.  
    - If multiple similar tags are appropriate, select **the most specific and detailed** ones.

    ### Instructions:
    1. **Handling Tags:**
    - **Select from the given list** only. Do **not create new tags** arbitrarily.
    - If multiple similar tags seem relevant, pick the **most specific and detailed**.
    - The chosen tags may belong under a broader tag structure.

    2. **Scenarios to Address:**
    - If no tag fits, select **none**.
    - If the input tag list is **empty**, select **none**.
    - If multiple tags apply, return a **list of tags**.

    3. **Expected Output:**
    - Generate the result based on the `input_json` below.
    - Return the appropriate tag(s) or `none` if no valid tags are suitable.

    {input_json}

    {format}
    """),
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

