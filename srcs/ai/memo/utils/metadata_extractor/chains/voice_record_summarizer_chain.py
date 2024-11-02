from operator import itemgetter
import textwrap
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from ai.utils.llm import llm4o_mini
from langchain_core.prompts import PromptTemplate


class _Voice_record_summarizer_chain_input(BaseModel):
    raw_transcript: str
    users_language: str
    
class Voice_record_summarizer_chain_output(BaseModel):
    record_transcription: str
    transcription_summary: str

_parser = PydanticOutputParser(pydantic_object=Voice_record_summarizer_chain_output)

_record_summarizer_chain_prompt=PromptTemplate.from_template(textwrap.dedent("""
    You will receive a transcription of a recorded file. Your task is to proofread the transcription for accuracy and then summarize it concisely in the user's language.

    ### Instructions:

    1. **Proofreading**:
    - Carefully review the transcription for any grammatical, spelling, or formatting errors.
    - Correct any errors to ensure clarity and accuracy.

    2. **Summarization**:
    - Briefly explain what this voice script is.
    - Summarize the corrected transcription in **concise language**.
    - Ensure the summary is in the **user's specified language** for consistency.

    3. **Expected Output**:
        a. the **corrected transcription**.
        b. the **summary** of the corrected transciptions in user's language.
    
    {input_json}
    
    {format}
    """),
    partial_variables={
        "format": _parser.get_format_instructions()
    }
)

_record_summarizer_chain=(
    { "input_json": itemgetter("input_json") }
    | _record_summarizer_chain_prompt
    | llm4o_mini
    | _parser
)

async def voice_record_summarizer(raw_transcript: str, lang: str) -> Voice_record_summarizer_chain_output:
    input_json_model=_Voice_record_summarizer_chain_input(
        raw_transcript=raw_transcript,
        users_language=lang
    )

    return await _record_summarizer_chain.ainvoke({"input_json": input_json_model.model_dump_json()})
