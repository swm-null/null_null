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
    timestamp: datetime
    content: str
    
class _Similarity_result_with_memo_chain_input(BaseModel):
    question: str
    languages_of_user: str
    memos: list[_Memo]

class Similarity_result_with_memo_chain_output(BaseModel):
    answerable: bool
    answer: str=Field(description="answer to the user's question", default=[""])
    used_memo_ids: list[str]=Field(description="used memo ids", default=[[]])

_parser = PydanticOutputParser(pydantic_object=Similarity_result_with_memo_chain_output)

_similarity_result_with_memo_chain_prompt=PromptTemplate.from_template(textwrap.dedent("""
    You have to answer the user's question.
    The user wants to find specific information in the notes he or she wrote.
    This information can be inferred from the content of the notes, or you can simply find notes that contain specific keywords.
    There may even be cases where the answer cannot be found in the notes the user wrote.

    Find the intent in the user's question and create an answer to that question.

    To do this, you will be provided with the following information:
    The user's question, the language the user uses, and the user's notes.
    The user's notes consist of the note's ID, the time the note was written, the content of the note, and a description of the content.

    There are a few things to keep in mind when answering the user's question.

    1. Recognize exactly what the user asked and answer.
    The notes given may not be related to the user's question.
    If they seem unrelated to the question, do not try to use the notes. 
    Understand the intent of the question and do not include information unrelated to the question in your answer.
    If a user asks a question about a specific category, you might be able to answer it using notes from the user's notes about things that fall into that specific category.
    Create an answer using only the notes that can answer the user's question.
    
    When creating a result, you should utilize all the information in the memo. The metadata of the memo contains additional information about the memo. Actively utilize this information to create an answer.
    But don't give users information like the ID of the note. This is information that is only used in the database.

    2. The user may not use time-related expressions properly. 
    Even if the user uses the expression "next week" in the memo, this "next week" means "next week from the time the memo was written", not "next week from now, when the question is answered". Therefore, create an answer considering the current time when the question is answered and the time when the user wrote the memo.
    The current time for this is as follows.
    Current Time: {current_time}

    For this, the memo description can have a field called "relative_time".
    This is the result of converting the relative time expression written in the memo to an absolute time based on the time of writing at the time of writing the memo.
    This result may or may not be accurate. You should judge for yourself whether the result is accurate, and if it is, use this field as well.

    3. Even if the content cannot be answered, the user should receive an answer.
    The given memo may not provide the information the user wants. In addition, the user may not be asking a 'question'.
    Even so, the result you created will be shown to the user. The user cannot receive an empty answer.
    Even if it is not a question that can be answered, please write an appropriate message that you cannot answer in the "answer" field of the output.

    4. Organize the memos used in the answer.
    When the user receives an answer, he or she may want to know which information was used to create the answer. Therefore, please select the memos used to create the answer and put them in the "used_memo_ids" field of the output.

    The answer must be created based on the language used by the user.

    Now, I will attach the question and memos below. Please take care.

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
                content=memo.metadata,
                timestamp=memo.timestamp
            ) for memo in memos
        ],
        languages_of_user=lang
    )
    
    return _similarity_result_with_memo_chain.invoke({"input_json": input_json_model.model_dump_json()})

async def asimilarity_result_with_memo(question: str, memos: list[Memo], lang: str) -> Similarity_result_with_memo_chain_output:
    input_json_model=_Similarity_result_with_memo_chain_input(
        question=question,
        memos=[
            _Memo(
                id=memo.id,
                content=memo.metadata,
                timestamp=memo.timestamp
            ) for memo in memos
        ],
        languages_of_user=lang
    )
    
    return await _similarity_result_with_memo_chain.ainvoke({"input_json": input_json_model.model_dump_json()})
