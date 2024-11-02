from operator import itemgetter
import textwrap
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from ai.memo._models.tag import Tag
from ai.utils.llm import llm4o_mini
from langchain_core.prompts import PromptTemplate
from ai.memo.tag._configs import TAG_SELECTION_COUNT


class _Tag(BaseModel):
    name: str
    is_new: bool

class _Select_tags_chain_input(BaseModel):
    memo: str
    candidate_tags: list[_Tag]
    lang: str

class _Select_tags_chain_output(BaseModel):
    tag_names: list[str] = Field(description="selected tag names")

_parser = PydanticOutputParser(pydantic_object=_Select_tags_chain_output)

_select_tags_chain_prompt=PromptTemplate.from_template(textwrap.dedent("""
    You are an expert at organizing memos by selecting the most appropriate tags from a given list.

    ### Objective:
    - Choose the **most relevant tags** that accurately represent the memo's content, based on the provided options.

    ### Instructions:

    1. **Tag Selection Rules**:
    - **Minimum Selection**: You must select **at least one tag**.
    - **Maximum Selection**: You may select **up to {selection_count} tags**.
        - If the memo’s content aligns with fewer than {selection_count} tags, select only the most relevant ones.

    2. **Exclusion Rules**:
    - **Do not select the root tag** (`'@'`), as it serves only as a placeholder for the tag structure.
    - **New vs. Existing Tags**:  
        - If an **existing tag** is **virtually identical** to a **new tag** (i.e., `is_new = true`), choose the **existing tag** to maintain consistency.

    3. **Expected Output**:
    - Based on the **memo content and the available tags** from the `input_json`, return only the selected tag(s).
    - Ensure your selection **best captures the key meaning** of the memo's content.

    {input_json}

    {format}
    """),
    partial_variables={
        "format": _parser.get_format_instructions(),
        "selection_count": TAG_SELECTION_COUNT,  
    }
)

_select_tags_chain=(
    { "input_json": itemgetter("input_json") }
    | _select_tags_chain_prompt
    | llm4o_mini
    | _parser
)

async def select_tag(memo_content: str, candidate_tags: list[Tag], lang: str) -> _Select_tags_chain_output:
    input_json_model=_Select_tags_chain_input(
        memo=memo_content,
        candidate_tags=[
            _Tag(
                name=tag.name,
                is_new=tag.is_new
            ) for tag in candidate_tags
        ],
        lang=lang
    )
    
    return await _select_tags_chain.ainvoke({"input_json": input_json_model.model_dump_json()})
