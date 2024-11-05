from operator import itemgetter
import textwrap
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from ai.utils import llm4o_mini
from langchain_core.prompts import PromptTemplate


class _Get_new_tag_chain_input(BaseModel):
    query: str
    lang: str
    
class _Get_new_tag_chain_output(BaseModel):
    name: str

_parser = PydanticOutputParser(pydantic_object=_Get_new_tag_chain_output)

_get_new_tag_chain_prompt=PromptTemplate.from_template(textwrap.dedent("""
    You are an expert at organizing memos by suggesting appropriate tag names.

    ### Objective:
    - Recommend a concise and relevant **tag name** to categorize a new memo.
    - The tags you suggest will later be organized among existing tags, so avoid being overly specific.

    ### Instructions:
    1. **Naming Restrictions**:
    - Use only spaces (' ') between words—do not use underscores or other special characters.
    - Ensure all spaces are placed correctly and without spelling errors.

    2. **Language Requirement**:
    - Create tags in the **user's language** to ensure consistency.

    3. **Expected Output**:
    - Provide **one tag** per response that suits the memo's content from the `input_json` provided.
    - Output only the tag name—no additional formatting.

    {input_json}

    {format}
    """),
    partial_variables={
        "format": _parser.get_format_instructions()
    }
)

_get_new_tag_chain=(
    { "input_json": itemgetter("input_json") }
    | _get_new_tag_chain_prompt
    | llm4o_mini
    | _parser
)

async def get_new_tag(query: str, lang: str) -> _Get_new_tag_chain_output:
    input_json_model=_Get_new_tag_chain_input(
        query=query,
        lang=lang
    )
    
    return await _get_new_tag_chain.ainvoke({"input_json": input_json_model.model_dump_json()})
