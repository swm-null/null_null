from operator import itemgetter
import textwrap
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from ai.memo._models.tag import Tag
from ai.memo.structure.deprecated.processor._models.memo import Memo
from ai.utils.llm import llm4o
from langchain_core.prompts import PromptTemplate


class _Tag(BaseModel):
    name: str
    linked_memo: int
    
class _Get_new_relations_and_tags_chain_input(BaseModel):
    lang: str=Field(description="user's language")
    new_tags: list[_Tag]=Field(description="new tags")
    memo_metadatas: dict[str, str]=Field(description="metadatas of target memos")
    current_tag_structures: dict[str, list[str]]=Field(description="adjacent list of tag structures")
        
class Relation_for_chain(BaseModel):
    parent_name: str
    child_name: str

class Get_new_relations_and_tags_chain_output(BaseModel):
    relations: list[Relation_for_chain]=Field(description="relations of new directory")
    new_tags: list[str]=Field(description="name of given new_tags and newly created intermediate tags by you")

_parser = PydanticOutputParser(pydantic_object=Get_new_relations_and_tags_chain_output)

_get_new_relations_and_tags_chain_prompt=PromptTemplate.from_template(textwrap.dedent("""
    You are an expert at organizing memos by creating and structuring appropriate tags.

    ### Objective:
    - Use the **metadata in the memo description** to categorize the memo correctly by placing its **new tag** within the existing tag structure.
    - If necessary, **create intermediate tags** to maintain a logical tag hierarchy.

    ### Instructions:

    1. **Handling Tags and Hierarchy**:
    - **Root Tag**: The tag named `'@'` is the **root** of the tag structure. 
    - The Root Tag is always exists.
    - You can **attach the new tag** directly to an existing tag, or **create intermediate tags** when appropriate.
        - Example: If you have a tag called `"food"` and the new tag is `"banana"`, it would be more logical to first create `"fruit"` as an intermediate tag.  
        Result: `"food"` → `"fruit"` → `"banana"`.

    2. **Tag Naming Rules**:
    - Use **spaces** (' ') between words—**do not use special characters** like underscores ('_').
    - Ensure all **spaces are correctly placed** to avoid spelling mistakes.
    - **Use the user's language** for creating any new tags.

    3. **New Tag Creation Constraints**:
    - If the **new_tags** field in the provided JSON is **empty**, do not create any new tags.

    4. **Expected Output**:
    - Look at the **JSON metadata** below and generate the appropriate tags and relationships.
    - 

    {input_json}

    {format}
    """),
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

async def get_new_relations_and_tags(tags: list[Tag], memos: dict[int, Memo], lang: str, directories: dict[str, list[str]]) -> Get_new_relations_and_tags_chain_output:
    input_json_model=_Get_new_relations_and_tags_chain_input(
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
