from datetime import datetime
from operator import itemgetter
import textwrap
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from ai.search._models.memo import Memo
from ai.utils.llm import llm4o_mini
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
You need to answer user questions based on the provided memos. Follow these guidelines carefully:
    ---

    ## **Instructions**:

    1. **Language and Memo Usage**:
    - Answer in the user’s language.
    - If you use a memo to generate the response, list its ID(s) in the used_memo_ids field.
    
    2. **Generate answer using memos**:
    - The information in the content field is the content of the memo entered by the user.
    - The information in the metadata field is a description of the content of this memo. There is various information such as what the content of the memo means, a description of the image attached to the memo, etc. 
    - Use the most of these two fields.
    
    3. **Handling Time-sensitive Queries**:
    - If a user asks a time-related question, such as next week's schedule, don't use “time-related expressions” in the memo's content.
    - Instead, use the converted “time-related expressions” in the memo's metadata to answer the question.
    - The converted time-related expressions are the result of converting the “time-related expressions” in the memo to a specific time based on when the memo was created.
    - As much as possible, try to analyze the user's intent in writing memos and the intent of the question so that you can provide the desired answer.
    - Users write memos based on when they write them without thinking, but when they hear the answer, they want it in the present.
    
    4. **Decision Logic for Answerable Status**:
        3.1. **If** a relevant memo matches the query based on content (such as time-based phrases), mark answerable = True.
            - Provide the answer using the memo’s information.
            - Include the memo ID(s) in the used_memo_ids.
        3.2. **If no memo** provides relevant content, mark answerable = False.
    
    ## **Current Time**: {current_time}

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
    | llm4o_mini
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
