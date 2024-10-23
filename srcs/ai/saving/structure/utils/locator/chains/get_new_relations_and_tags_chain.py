from operator import itemgetter
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from ai.saving._models.tag import Tag
from ai.saving.structure._models.memo import Memo
from ai.utils.llm import llm4o
from langchain_core.prompts import PromptTemplate

class _Tag(BaseModel):
    name: str
    linked_memo: int
    
class _get_new_relations_and_tags_chain_input(BaseModel):
    lang: str=Field(description="user's language")
    new_tags: list[_Tag]=Field(description="new tags")
    memo_metadatas: dict[str, str]=Field(description="metadatas of target memos")
    current_tag_structures: dict[str, list[str]]=Field(description="adjacent list of tag structures")
        
class Relation_for_chain(BaseModel):
    parent_name: str
    child_name: str

class Get_new_relations_and_tags_chain_output(BaseModel):
    relations: list[Relation_for_chain]=Field(description="relations of new directory")
    new_directories: list[str]=Field(description="name of given directories and a newly created directory by you")

_parser = PydanticOutputParser(pydantic_object=Get_new_relations_and_tags_chain_output)

_get_new_relations_and_tags_chain_prompt=PromptTemplate.from_template(
"""
You're an expert at organizing memos.
Your memos are categorized using tags, and each tag can have subtags that belong to the tag.

The user is about to add a new memo.
You'll be given a new tag to categorize it.
The new tag is linked with the new memo the user added.
You need to look at the memo's description (metadata) and place the tags appropriately.

To do this, you can attach the new tag to a child of an existing tag.
However, you can also create a new tag in the middle, rather than attaching it directly to an existing tag.
For example, if you have a tag called “food” and the new tag to be created is “banana”, it would be unnatural to create a “food”-“banana” relationship right away.
Instead, you could create a tag called 'fruit', and then create the tag so that the relationship is 'food'-'fruit'-'banana'.

When creating new tags, consider the user's language and create them in that language.
However, don't create any new tags when the new_tags field in the json is empty.

Look at the json below, and generate the results.

{input_json}

{format}
""",
    partial_variables={
        "format": _parser.get_format_instructions()
    }
)

_get_new_relations_and_tags_chain=(
    { "input_json": itemgetter("input_json") }
    | _get_new_relations_and_tags_chain_prompt
    | llm4o
    | _parser
)

async def get_new_relations_and_tags(tags: list[Tag], memos: dict[int, Memo], lang: str, directories: dict[str, list[str]]):
    input_json_model=_get_new_relations_and_tags_chain_input(
        lang=lang,
        new_tags=[
            _Tag(
                name=tag.name,
                linked_memo=tag.connected_memo_id
            ) for tag in tags if tag.connected_memo_id
        ],
        memo_metadatas={str(idx): memo.metadata for idx, memo in memos.items()},
        current_tag_structures=directories,
    )
    
    return await _get_new_relations_and_tags_chain.ainvoke({"input_json": input_json_model.model_dump_json()})
