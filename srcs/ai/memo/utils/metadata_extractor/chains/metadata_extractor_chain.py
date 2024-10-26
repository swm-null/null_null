from datetime import datetime
from operator import itemgetter
import textwrap
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from ai.utils.llm import llm4o_mini
from langchain_core.prompts import PromptTemplate


class _Metadata_extractor_chain_input(BaseModel):
    lang: str
    content: str
    
class Metadata_extractor_chain_output(BaseModel):
    content_description: str
    time_related_expressions: dict[str, str]

_parser = PydanticOutputParser(pydantic_object=Metadata_extractor_chain_output)

_metadata_extractor_chain_prompt=PromptTemplate.from_template(textwrap.dedent("""
    You will receive a memo, and your task is to summarize it briefly in the same language as the original memo. Your summary should capture the essence of the content while considering the following:

    1. **Formatting Details**:
    If the memo contains specific elements like a social security number or phone number, identify the relevant country (based on the memo's language or content) and adapt the format to match the conventions used in that country.
    
    2. **Time-Related Expressions**:
    Replace time-sensitive references like “next Saturday” with the precise date that matches the context, based on today's date.
    Ensure the summary reflects the adjusted time reference accurately to avoid confusion when reviewed later.
    Write down the original text and the time so that I can find the note later.

    Current time: {current_time}
    
    {input_json}
    
    {format}
    """),
    partial_variables={
        "format": _parser.get_format_instructions(),
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
)

_metadata_extractor_chain=(
    { "input_json": itemgetter("input_json") }
    | _metadata_extractor_chain_prompt
    | llm4o_mini
    | _parser
)

async def metadata_extractor(content: str, lang: str) -> str:
    input_json_model=_Metadata_extractor_chain_input(
        content=content,
        lang=lang
    )

    return await _metadata_extractor_chain.ainvoke({"input_json": input_json_model.model_dump_json()})
