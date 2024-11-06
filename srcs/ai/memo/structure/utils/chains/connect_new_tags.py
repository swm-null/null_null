from operator import itemgetter
import textwrap
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from ai.utils.llm import llm4o
from langchain_core.prompts import PromptTemplate
from routers._models.memo._models import Memo_processed_memo


class _Tag(BaseModel):
    name: str
    linked_memos: list[int]
    
class _Memo(BaseModel):
    id: int
    memo: str
    
class _Connect_new_tags_input(BaseModel):
    new_tags: list[_Tag]
    memos: list[_Memo]
    current_tag_structures: dict[str, list[str]]=Field(description="adjacent list of tag structures")
    users_language: str=Field(description="user's language")
        
class Relation_created_by_llm(BaseModel):
    parent_name: str
    child_name: str

class Connect_new_tags_output(BaseModel):
    relations: list[Relation_created_by_llm]=Field(description="newly added relations of tag", default=[[]])
    new_tags: list[str]=Field(description="newly created intermediate tags by you", default=[[]])

_parser = PydanticOutputParser(pydantic_object=Connect_new_tags_output)

_connect_new_tags_prompt=PromptTemplate.from_template(textwrap.dedent("""
    You are the one who organizes the tags that contain the notes.
    Given new tags and notes that will be contained in these tags, you decide how these tags should be organized in the current tag structure.

    People use tags to find notes. Each tag forms a hierarchy between parents and children.
    People can see memos stored in child tags even when they are browsing the parent tag of a tag, so organize them considering this.

    The root of the tag structure is '@'.
    Tags form a hierarchy, and tags that belong to the same hierarchy have similar inclusiveness.
    It should be noted that, unlike the general folder structure, a tag can have multiple parents and multiple children.

    You will be given tags that need to be newly added, notes that will be contained in each tag, and the current tag structure.
    For each newly added tag, you will look at the notes that will be contained in this tag and decide where and how this tag will be placed in the tag structure.

    Memos can contain not only text (content), but also pictures, audio files, links, etc., so if the memo contains these, a brief summary of them will be provided.

    Sometimes, a given new tag contains too much detail to be placed directly below an existing tag.

    In this case, you should create an intermediate tag and place the new tag appropriately.

    Example: If you have a tag called `"food"` and the new tag is `"banana"`, it would be more logical to first create `"fruit"` as an intermediate tag.

    Result: `"food"` → `"fruit"` → `"banana"`.

    When creating a new tag, use only what is in the content. However, use description only when you cannot create a tag with only what is in the content.
    When creating a tag name, make it equal or less than two words, and make it in the user's language.

    There are two things to be careful of:

    First, I'll explain the rules for tags that exist as children of the root tag.
    The children of the root tag are divided into large units such as "schedule" (contains notes about things to do, or notes about someone's birthday party, etc.), "study" (contains notes related to what user studied), and "memos" (contains notes that user need to check later, such as birthdays and phone numbers).
    And tags with detailed information should be created under each of these tags.
    When creating such tags, remember to name them in the language your users will use.

    Second, when a new tag is created, you need to check if there are multiple things that can be the tag's parents.
    I mentioned earlier that a tag can have multiple parents. Therefore, if you determine that a new tag I provided or an intermediate tag you created can have multiple parents, connect the parents.

    All tags except the root tag should have at least one parent.
    All of the given tags must be included in the results, without any omissions and with their names unchanged.

    Here is the information about the tag and notes you need to work with.
    
    {input_json}

    {format}
    """),
    partial_variables={
        "format": _parser.get_format_instructions()
    }
)

_connect_new_tags=(
    { "input_json": itemgetter("input_json") }
    | _connect_new_tags_prompt
    | llm4o
    | _parser
)

async def connect_new_tags_chain(preprocessed_memos: list[Memo_processed_memo], current_structure: dict[str, list[str]], lang: str) -> Connect_new_tags_output:
    memo_idx=0
    new_tags: dict[str, _Tag]={}
    memos: list[_Memo]=[]
    
    for memo in preprocessed_memos:
        used=False
        if memo.temporal_tags:
            for tag in memo.temporal_tags:
                if tag.name not in new_tags:
                    new_tags[tag.name]=_Tag(name=tag.name, linked_memos=[])
                used=True
                new_tags[tag.name].linked_memos.append(memo_idx)
        if used:
            memos.append(_Memo(id=memo_idx, memo=memo.metadata))
            memo_idx+=1
                
    input_json_model=_Connect_new_tags_input(
        new_tags=list(new_tags.values()),
        memos=memos,
        current_tag_structures=current_structure,
        users_language=lang
    )
    
    if new_tags and memos:
        return await _connect_new_tags.ainvoke({"input_json": input_json_model.model_dump_json()})
    else:
        return Connect_new_tags_output()
