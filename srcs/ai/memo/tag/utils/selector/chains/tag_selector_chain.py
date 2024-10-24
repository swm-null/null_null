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
    You're an expert at organizing memos.
    Your memos are categorized using tags, and each tag can have subtags that belong to the tag.

    The user is about to add a new memo.
    You need to pick out some of the selected tags.

    Given the content of a note and a set of selected tags, choose which of those tags this note belongs to.
    You can choose up to {selection_count} tags, and you don't have to choose {selection_count} tags if the right tag is a relief.

    Instead, if a new tag exists that is very similar to an already existing tag (is_new field is false), don't pick that new tag (is_new field is true).
    For example, if there are virtually identical tags that differ only in spacing, such as “짧은 질문” and “짧은질문”, ignore the new tag.
    If you have virtually identical tags, such as “항공사 마일리지” and “항공 마일리지”, ignore the new tag.

    Look at the json below, and generate the results.

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
