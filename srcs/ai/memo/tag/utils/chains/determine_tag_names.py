from operator import itemgetter
import textwrap
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from ai.utils import finetunned_for_tags
from langchain_core.prompts import PromptTemplate
from ai.memo.tag._configs import TAG_SELECTION_COUNT


class _Determine_tag_names_chain_input(BaseModel):
    memo_infomation: str
    current_tag_structure: dict[str, list[str]]
    language_of_user: str
    
class Determine_tag_names_chain_output(BaseModel):
    selected_tag_names: list[str]=Field(description="Tag names selected as being associated with a memo in the current tag structure")
    new_tag_names: list[str]=Field(description="Tags that are not in the current tag structure but should be added to organize this memo")

_parser = PydanticOutputParser(pydantic_object=Determine_tag_names_chain_output)

_determine_tag_names_chain_prompt=PromptTemplate.from_template(textwrap.dedent("""
    You are the one who sorts the memos.

    Given a memo, you decide how this memo can be organized among the currently organized memos.

    Memos are stored in each 'tag'.
    The root of the tag structure is '@'.
    People can see memos stored in child tags even when they are browsing the parent tag of a tag, so organize them considering this.

    You will be provided with information about the memo written by the user and the current tag structure.
    Memos can contain not only text (content), but also pictures, audio files, links, etc., so if the memo contain these, a brief summary of them will be provided.

    In the "selected_tag_names" field, enter the names of tags that you think this memo should be sorted among the existing tags.
    You can select multiple tags if you think it can belong to more than one tag.
    When selecting multiple tags, if the relationship between two tags is a parent or grandparent relationship, select only the tag at the bottom.
    
    You just need to create a tag that belongs to the lowest tag in the classification.
    Then it will automatically be appropriately linked from the root to the tag you created.
    
    If it seems difficult to identify this memo with only existing tags, write the name of the tag that should be newly created.
    In the "selected_tag_names" field, enter the names of tags that you created.
    When creating a new tag, use only what is in the content. However, use description only when you cannot create a tag with only what is in the content.
    It doesn't have to be too detailed, but it should be enough for a person to think that this memo can be stored in this tag.
    When creating a tag name, make it equal or less than two words, and make it in the user's language.
    Do not create a tag that is similar to an existing tag.

    If it is a memo that cannot be classified, classify it in a tag that means that it cannot be classified.

    Descriptions are just additional information. Put the most emphasis on content.
    Focus on the "main content" of the memo. Don't worry about the tone of the note, such as whether the content is in the form of a question.
    
    Select up to {selection_count} new tags and a combination of existing tags.
    Do not create more than two new tags.
    
    Here is the information.

    {input_json}

    {format}
    """),
    partial_variables={
        "format": _parser.get_format_instructions(),
        "selection_count": TAG_SELECTION_COUNT
    }
)

_determine_tag_names_chain=(
    { "input_json": itemgetter("input_json") }
    | _determine_tag_names_chain_prompt
    | finetunned_for_tags
    | _parser
)

async def determine_tag_names_chain(content: str, current_tag_structure: dict[str, list[str]], lang: str) -> Determine_tag_names_chain_output:
    input_json_model=_Determine_tag_names_chain_input(
        memo_infomation=content,
        current_tag_structure=current_tag_structure,
        language_of_user=lang
    )
    
    return await _determine_tag_names_chain.ainvoke({"input_json": input_json_model.model_dump_json()})
