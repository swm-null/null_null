from operator import itemgetter
import textwrap
from langchain_core.output_parsers import PydanticOutputParser
from openai import BaseModel
from pydantic import Field
from ai.utils.llm import llm4o_mini
from langchain_core.prompts import PromptTemplate


class _Text_summarizer_chain_input(BaseModel):
    text: str
    users_language: str
    
class Text_summarizer_chain_output(BaseModel):
    summary: str=Field(description="summary of text")
    simple_description: str=Field(description="Simple text to be provided with a preview. So that users know what this website is about. Words rather than sentences.")

_parser = PydanticOutputParser(pydantic_object=Text_summarizer_chain_output)

_text_summarizer_chain_prompt=PromptTemplate.from_template(textwrap.dedent("""
    The text you receive is the content crawled from a website.
    You need to summarize the text you receive.

    The summary should contain information about what this website contains, and should contain a description of the given text. I think the length of the description should be about a half of the length of the given text.

    Summarize it in detail so that you can find the information you want from the content of this site by just looking at this summary later. However, unnecessary information does not have to be included in the summary.
    And summarize it in the language that the user uses.

    {input_json}
    
    {format}
    """),
        partial_variables={
        "format": _parser.get_format_instructions()
    }
)

text_summarizer_chain=(
    { "input_json": itemgetter("input_json") }
    | _text_summarizer_chain_prompt
    | llm4o_mini
    | _parser
)

async def text_summarizer(text: str, lang: str) -> Text_summarizer_chain_output:
    input_json_model=_Text_summarizer_chain_input(
        text=text,
        users_language=lang
    )
    
    return await text_summarizer_chain.ainvoke({"input_json": input_json_model.model_dump_json()})
