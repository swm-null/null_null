from datetime import datetime
from operator import itemgetter
import textwrap
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from ai.search._models.memo import Memo
from ai.utils.llm import llm4o
from langchain_core.prompts import PromptTemplate


class _Memo(BaseModel):
    id: str
    content: str
    metadata: str
    timestamp: datetime
    
class _Similarity_result_with_memo_chain_input(BaseModel):
    question: str
    memos: list[_Memo]
    lang: str

class Similarity_result_with_memo_chain_output(BaseModel):
    answerable: bool
    answer: str=Field(description="answer to the user's question", default=[""])
    used_memo_ids: list[str]=Field(description="used memo ids", default=[[]])

_parser = PydanticOutputParser(pydantic_object=Similarity_result_with_memo_chain_output)

_similarity_result_with_memo_chain_prompt=PromptTemplate.from_template(textwrap.dedent("""
    You need to answer user questions.
    Answer in the user's language.
    If you use a memo to answer, write the ID of the memo in used_memo_ids.

    I'm attaching some pre-written notes from the user that might help you answer this question.
    If a user asks a time-related question, consider the current time and the time the note was written.
    Current time: {current_time}

    1. Determine if you can answer the user's question with the information provided.

    2-1. If you can, set the field answerable True and create an answer to the user's question using the information provided and end this prompt. 
    2-2. If you can't, set the field answerable False and exit.

    {input_json}

    {format}
    """),
    partial_variables={
        "format": _parser.get_format_instructions(),
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
)

_similarity_result_with_memo_chain=(
    { "input_json": itemgetter("input_json") }
    | _similarity_result_with_memo_chain_prompt
    | llm4o
    | _parser
)

def similarity_result_with_memo(question: str, memos: list[Memo], lang: str) -> Similarity_result_with_memo_chain_output:
    input_json_model=_Similarity_result_with_memo_chain_input(
        question=question,
        memos=[
            _Memo(
                id=memo.id,
                content=memo.content,
                metadata=memo.metadata,
                timestamp=memo.timestamp
            ) for memo in memos
        ],
        lang=lang
    )
    
    return _similarity_result_with_memo_chain.invoke({"input_json": input_json_model.model_dump_json()})

async def asimilarity_result_with_memo(question: str, memos: list[Memo], lang: str) -> Similarity_result_with_memo_chain_output:
    input_json_model=_Similarity_result_with_memo_chain_input(
        question=question,
        memos=[
            _Memo(
                id=memo.id,
                content=memo.content,
                metadata=memo.metadata,
                timestamp=memo.timestamp
            ) for memo in memos
        ],
        lang=lang
    )
    
    return await _similarity_result_with_memo_chain.ainvoke({"input_json": input_json_model.model_dump_json()})
